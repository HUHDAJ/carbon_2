import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
import argparse
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class CarbonFactorPredictor:
    def __init__(self, model_type='lstm', seq_length=30,
                 start_date='2025-12-28', end_date='2026-09-23'):
        """
        参数:
            model_type : 'lstm' (推荐), 'dlinear', 'transformer'
            seq_length : 输入历史天数
            start_date : 输出起始日期
            end_date   : 输出结束日期
        """
        self.model_type = model_type.lower()
        self.seq_length = seq_length
        self.start_date = start_date
        self.end_date = end_date
        self.model = None
        self.scaler_X = StandardScaler()   # 标准化序列值
        self.scaler_y = StandardScaler()   # 标准化目标值（可选）
        self.feature_scaler = StandardScaler()  # 标准化日期特征
        self.results_dir = 'data/results/predict/CEP'
        os.makedirs(self.results_dir, exist_ok=True)

    def load_data(self):
        """加载数据并仅保留2022-2024年用于训练"""
        filepath = 'data/results/carbon_factors/daily_carbon_factors_all.csv'
        print(f"加载数据: {filepath}")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {os.path.abspath(filepath)}")

        df = pd.read_csv(filepath, encoding='utf-8')
        date_col = next((c for c in df.columns if '日期' in c or 'date' in c.lower()), None)
        carbon_col = next((c for c in df.columns if '碳因子' in c or 'carbon' in c.lower()), None)

        if date_col is None or carbon_col is None:
            raise ValueError("未找到日期列或碳因子列")

        df = df.rename(columns={date_col: 'date', carbon_col: 'carbon_factor'})
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')[['carbon_factor']].sort_index()

        # 仅保留2022-2024年数据用于训练
        mask = (df.index >= '2022-01-01') & (df.index <= '2024-12-31')
        df_train = df.loc[mask].copy()
        print(f"训练数据: {len(df_train)} 天 (2022-01-01 ~ 2024-12-31)")
        print(f"碳因子统计: min={df_train['carbon_factor'].min():.4f}, "
              f"max={df_train['carbon_factor'].max():.4f}, mean={df_train['carbon_factor'].mean():.4f}")
        return df_train

    def add_date_features(self, dates):
        """
        为日期列表生成丰富的时间特征
        返回DataFrame，索引为dates，列为特征
        """
        df_feat = pd.DataFrame(index=dates)
        df_feat['month'] = df_feat.index.month
        df_feat['day_of_week'] = df_feat.index.dayofweek
        df_feat['day_of_year'] = df_feat.index.dayofyear
        df_feat['quarter'] = df_feat.index.quarter
        df_feat['is_weekend'] = (df_feat['day_of_week'] >= 5).astype(int)

        # 周期编码（sin/cos）使模型理解循环连续性
        df_feat['month_sin'] = np.sin(2 * np.pi * df_feat['month'] / 12)
        df_feat['month_cos'] = np.cos(2 * np.pi * df_feat['month'] / 12)
        df_feat['doy_sin'] = np.sin(2 * np.pi * df_feat['day_of_year'] / 365)
        df_feat['doy_cos'] = np.cos(2 * np.pi * df_feat['day_of_year'] / 365)
        df_feat['dow_sin'] = np.sin(2 * np.pi * df_feat['day_of_week'] / 7)
        df_feat['dow_cos'] = np.cos(2 * np.pi * df_feat['day_of_week'] / 7)

        # 删除原始整数特征（可选，避免冗余）
        df_feat.drop(['month', 'day_of_week', 'day_of_year', 'quarter'], axis=1, inplace=True)
        return df_feat

    def prepare_data(self):
        """准备训练数据：序列X + 日期特征F，目标y"""
        print("\n准备训练数据...")
        df = self.load_data()

        # 1. 碳因子归一化
        values = df['carbon_factor'].values.reshape(-1, 1)
        scaled_values = self.scaler_X.fit_transform(values).flatten()
        df['carbon_factor_scaled'] = scaled_values

        # 2. 生成日期特征（用于每个样本的目标日期）
        date_features = self.add_date_features(df.index)
        # 对特征进行标准化
        feat_cols = date_features.columns
        feat_scaled = self.feature_scaler.fit_transform(date_features)
        df_feat_scaled = pd.DataFrame(feat_scaled, index=df.index, columns=feat_cols)
        df = df.join(df_feat_scaled)

        print(f"特征维度: {len(feat_cols)}")
        print(f"特征列: {list(feat_cols)}")
        return df

    def create_sequences(self, data):
        """
        创建监督学习序列：
        X_seq: 过去seq_length天的碳因子值 (序列输入)
        X_feat: 当前预测日的日期特征 (特征输入)
        y: 当前预测日的碳因子值 (目标)
        """
        X_seq, X_feat, y, target_dates = [], [], [], []
        series = data['carbon_factor_scaled'].values
        # 特征矩阵（已标准化）
        feat_matrix = data[[c for c in data.columns if c not in ['carbon_factor', 'carbon_factor_scaled']]].values

        for i in range(self.seq_length, len(series)):
            X_seq.append(series[i - self.seq_length:i])
            X_feat.append(feat_matrix[i])      # 第i天的特征
            y.append(series[i])
            target_dates.append(data.index[i])

        X_seq = np.array(X_seq, dtype=np.float32).reshape(-1, self.seq_length, 1)
        X_feat = np.array(X_feat, dtype=np.float32).reshape(-1, len(feat_matrix[0]))
        y = np.array(y, dtype=np.float32).reshape(-1, 1)

        print(f"序列创建完成: X_seq.shape={X_seq.shape}, X_feat.shape={X_feat.shape}, y.shape={y.shape}")
        return X_seq, X_feat, y, target_dates

    def build_lstm_model(self, feature_dim):
        """LSTM模型：序列输入 + 特征输入 -> 拼接 -> Dense输出"""
        print("构建 LSTM 模型...")
        # 序列输入分支
        seq_input = tf.keras.Input(shape=(self.seq_length, 1), name='seq_input')
        lstm1 = tf.keras.layers.LSTM(64, return_sequences=True)(seq_input)
        lstm1 = tf.keras.layers.Dropout(0.2)(lstm1)
        lstm2 = tf.keras.layers.LSTM(32, return_sequences=False)(lstm1)
        lstm2 = tf.keras.layers.Dropout(0.2)(lstm2)

        # 特征输入分支
        feat_input = tf.keras.Input(shape=(feature_dim,), name='feat_input')
        feat_dense = tf.keras.layers.Dense(16, activation='relu')(feat_input)

        # 拼接
        concat = tf.keras.layers.Concatenate()([lstm2, feat_dense])
        dense1 = tf.keras.layers.Dense(32, activation='relu')(concat)
        dense1 = tf.keras.layers.Dropout(0.2)(dense1)
        output = tf.keras.layers.Dense(1, name='output')(dense1)

        model = tf.keras.Model(inputs=[seq_input, feat_input], outputs=output)
        model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss='mse', metrics=['mae'])
        return model

    def build_dlinear_model(self):
        """原DLinear（MLP）保持单输入，兼容无特征场景"""
        print("构建 DLinear 模型 (单输入序列)...")
        inputs = tf.keras.Input(shape=(self.seq_length, 1))
        x = tf.keras.layers.Flatten()(inputs)
        x = tf.keras.layers.Dense(128, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        x = tf.keras.layers.Dense(64, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        x = tf.keras.layers.Dense(32, activation='relu')(x)
        outputs = tf.keras.layers.Dense(1)(x)
        model = tf.keras.Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=tf.keras.optimizers.Adam(0.001), loss='mse', metrics=['mae'])
        return model

    def build_transformer_model(self):
        """原Transformer简化版（全局池化）"""
        print("构建 Transformer 模型 (单输入序列)...")
        inputs = tf.keras.Input(shape=(self.seq_length, 1))
        x = tf.keras.layers.Dense(64)(inputs)
        x = tf.keras.layers.MultiHeadAttention(num_heads=4, key_dim=16)(x, x)
        x = tf.keras.layers.LayerNormalization()(x)
        x = tf.keras.layers.Dense(128, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        x = tf.keras.layers.Dense(64)(x)
        x = tf.keras.layers.GlobalAveragePooling1D()(x)
        outputs = tf.keras.layers.Dense(1)(x)
        model = tf.keras.Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=tf.keras.optimizers.Adam(0.0001), loss='mse', metrics=['mae'])
        return model

    def train(self, X_seq_train, X_feat_train, y_train,
              X_seq_val, X_feat_val, y_val, epochs=100, batch_size=32):
        print(f"\n开始训练 {self.model_type} 模型...")
        if self.model_type == 'lstm':
            feature_dim = X_feat_train.shape[1]
            self.model = self.build_lstm_model(feature_dim)
            train_inputs = {'seq_input': X_seq_train, 'feat_input': X_feat_train}
            val_inputs = {'seq_input': X_seq_val, 'feat_input': X_feat_val}
        else:  # dlinear 或 transformer
            if self.model_type == 'dlinear':
                self.model = self.build_dlinear_model()
            else:
                self.model = self.build_transformer_model()
            train_inputs = X_seq_train
            val_inputs = X_seq_val

        callbacks = [
            tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
            tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
        ]

        history = self.model.fit(
            train_inputs, y_train,
            validation_data=(val_inputs, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        return history

    def predict_future(self, last_seq_values, future_dates):
        """
        滚动预测未来每一天
        last_seq_values: 形状 (seq_length,) 的最后已知碳因子值（已归一化）
        future_dates   : 需要预测的日期列表（DatetimeIndex）
        返回: 预测值（原始尺度）
        """
        predictions_scaled = []
        # 初始序列
        current_seq = last_seq_values.copy().reshape(1, self.seq_length, 1)

        for date in future_dates:
            # 获取该日期的特征（标准化）
            feat_df = self.add_date_features(pd.DatetimeIndex([date]))
            feat_scaled = self.feature_scaler.transform(feat_df).reshape(1, -1)

            if self.model_type == 'lstm':
                pred_scaled = self.model.predict({'seq_input': current_seq, 'feat_input': feat_scaled}, verbose=0)
            else:
                pred_scaled = self.model.predict(current_seq, verbose=0)

            pred_scaled = pred_scaled[0, 0]
            predictions_scaled.append(pred_scaled)

            # 滚动更新序列
            current_seq = np.roll(current_seq, -1, axis=1)
            current_seq[0, -1, 0] = pred_scaled

        # 反标准化
        predictions = self.scaler_X.inverse_transform(np.array(predictions_scaled).reshape(-1, 1)).flatten()
        return predictions

    def run_pipeline(self, epochs=100, batch_size=32):
        """
        完整流程：
        1. 用2022-2024数据训练模型
        2. 从2025-01-01滚动预测至self.end_date
        3. 截取 [self.start_date, self.end_date] 并计算日变化/累计变化
        4. 保存结果
        """
        print("=" * 70)
        print("碳因子预测系统 (改进版) - LSTM + 日期特征")
        print("=" * 70)

        # 1. 准备数据
        data = self.prepare_data()
        X_seq, X_feat, y, _ = self.create_sequences(data)
        print(f"总样本数: {len(X_seq)}")

        # 2. 时间顺序划分
        train_size = int(len(X_seq) * 0.8)
        val_size = int(len(X_seq) * 0.1)
        X_seq_train, X_seq_val, X_seq_test = X_seq[:train_size], X_seq[train_size:train_size+val_size], X_seq[train_size+val_size:]
        X_feat_train, X_feat_val, X_feat_test = X_feat[:train_size], X_feat[train_size:train_size+val_size], X_feat[train_size+val_size:]
        y_train, y_val, y_test = y[:train_size], y[train_size:train_size+val_size], y[train_size+val_size:]

        print(f"数据划分: 训练={len(X_seq_train)}, 验证={len(X_seq_val)}, 测试={len(X_seq_test)}")

        # 3. 训练模型
        self.train(X_seq_train, X_feat_train, y_train,
                   X_seq_val, X_feat_val, y_val,
                   epochs=epochs, batch_size=batch_size)

        # 4. 测试集评估
        if self.model_type == 'lstm':
            y_pred_scaled = self.model.predict({'seq_input': X_seq_test, 'feat_input': X_feat_test}, verbose=0)
        else:
            y_pred_scaled = self.model.predict(X_seq_test, verbose=0)

        y_test_inv = self.scaler_X.inverse_transform(y_test.reshape(-1, 1)).flatten()
        y_pred_inv = self.scaler_X.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()

        mae = mean_absolute_error(y_test_inv, y_pred_inv)
        rmse = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
        r2 = r2_score(y_test_inv, y_pred_inv)

        metrics = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
        print("\n测试集评估:")
        print(f"  MAE: {mae:.6f}")
        print(f"  RMSE: {rmse:.6f}")
        print(f"  R²: {r2:.6f}")

        # 5. 滚动预测：从2025-01-01开始
        predict_start_full = '2025-01-01'
        predict_end_full = self.end_date
        days_full = (pd.to_datetime(predict_end_full) - pd.to_datetime(predict_start_full)).days + 1
        full_dates = pd.date_range(start=predict_start_full, periods=days_full)
        print(f"\n滚动预测起始: {predict_start_full}, 结束: {predict_end_full}, 总天数: {days_full}")

        # 提取最后seq_length天的历史值（2024年底）
        last_seq_values = data['carbon_factor_scaled'].values[-self.seq_length:]

        # 执行滚动预测
        full_predictions = self.predict_future(last_seq_values, full_dates)

        # 6. 截取目标区间
        start_dt = pd.to_datetime(self.start_date)
        end_dt = pd.to_datetime(self.end_date)
        mask = (full_dates >= start_dt) & (full_dates <= end_dt)
        target_dates = full_dates[mask]
        target_predictions = full_predictions[mask]

        # 7. 计算日变化和累计变化（基准日为起始前一天）
        base_date = start_dt - timedelta(days=1)
        if base_date in full_dates:
            base_value = full_predictions[full_dates == base_date][0]
        else:
            # 若基准日不在预测范围内（如2025-12-27在范围内，因为从2025-01-01开始）
            base_value = target_predictions[0]

        daily_changes = np.zeros_like(target_predictions)
        cumulative_changes = np.zeros_like(target_predictions)
        for i, val in enumerate(target_predictions):
            cumulative_changes[i] = val - base_value
            daily_changes[i] = val - target_predictions[i-1] if i > 0 else val - base_value

        # 8. 保存结果（保留6位小数）
        csv_path = self.save_forecast_style(
            dates=target_dates,
            predictions=target_predictions,
            daily_changes=daily_changes,
            cumulative_changes=cumulative_changes,
            metrics=metrics
        )
        print(f"\n✅ 预测完成！结果已保存至:\n   {csv_path}")

        # 9. 预览
        print("\n预测结果预览（前10天）:")
        for i in range(min(10, len(target_predictions))):
            print(f"  {target_dates[i].strftime('%Y-%m-%d')}: {target_predictions[i]:.6f}")

        return {
            'metrics': metrics,
            'predictions': target_predictions,
            'dates': target_dates.strftime('%Y-%m-%d').tolist(),
            'csv_file': csv_path
        }

    def save_forecast_style(self, dates, predictions, daily_changes, cumulative_changes, metrics):
        """保存为forecast.csv格式，保留6位小数"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        start_str = dates[0].strftime('%Y%m%d')
        end_str = dates[-1].strftime('%Y%m%d')
        filename = f"carbon_forecast_{start_str}_{end_str}_{timestamp}.csv"
        filepath = os.path.join(self.results_dir, filename)

        df = pd.DataFrame({
            'id': [''] * len(dates),
            'date': [d.strftime('%Y-%m-%d') for d in dates],
            'price': predictions,
            'cumulative_change': cumulative_changes,
            'daily_change': daily_changes
        })

        # 改为6位小数，避免0.69掩盖波动
        df['price'] = df['price'].map(lambda x: f"{x:.6f}")
        df['cumulative_change'] = df['cumulative_change'].map(lambda x: f"{x:.6f}")
        df['daily_change'] = df['daily_change'].map(lambda x: f"{x:.6f}")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# 碳因子预测结果 (改进版 LSTM+特征)\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 模型类型: {self.model_type}\n")
            f.write(f"# 历史天数: {self.seq_length}\n")
            f.write(f"# 预测区间: {dates[0].strftime('%Y-%m-%d')} 至 {dates[-1].strftime('%Y-%m-%d')}\n")
            f.write(f"# 预测总天数: {len(dates)}\n")
            f.write("#\n# 评估指标:\n")
            f.write(f"# MAE: {metrics['MAE']:.6f}\n")
            f.write(f"# RMSE: {metrics['RMSE']:.6f}\n")
            f.write(f"# R²: {metrics['R2']:.6f}\n")
            f.write("#\n")

        df.to_csv(filepath, mode='a', index=False, encoding='utf-8')
        return os.path.abspath(filepath)


def main():
    parser = argparse.ArgumentParser(description='碳因子预测 - 改进版(LSTM+日期特征)')
    parser.add_argument('--model', type=str, default='lstm',
                        choices=['lstm', 'dlinear', 'transformer'],
                        help='模型类型 (推荐lstm)')
    parser.add_argument('--history', type=int, default=30,
                        help='历史天数 (默认30)')
    parser.add_argument('--epochs', type=int, default=100,
                        help='训练轮次 (默认100)')
    parser.add_argument('--batch', type=int, default=32,
                        help='批次大小 (默认32)')
    parser.add_argument('--start', type=str, default='2025-12-28',
                        help='输出起始日期 (默认2025-12-28)')
    parser.add_argument('--end', type=str, default='2026-09-23',
                        help='输出结束日期 (默认2026-09-23)')
    args = parser.parse_args()

    predictor = CarbonFactorPredictor(
        model_type=args.model,
        seq_length=args.history,
        start_date=args.start,
        end_date=args.end
    )

    predictor.run_pipeline(
        epochs=args.epochs,
        batch_size=args.batch
    )


if __name__ == "__main__":
    main()