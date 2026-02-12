import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import sqlite3

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def preprocess_cea_data(df):
    data = df.copy()
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date').reset_index(drop=True)
    
    for col in ['daily_total_volume(tons)', 'daily_total_transaction_volume(RMB)']:
        if col in data.columns and data[col].dtype == 'object':
            data[col] = data[col].astype(str).str.replace(',', '').astype(float)
    
    if 'upper(percent)' in data.columns and data['upper(percent)'].dtype == 'object':
        data['upper(percent)'] = data['upper(percent)'].astype(str).str.replace('%', '').astype(float) / 100
    
    return data

class CEAPricePredictor:
    def __init__(self, data):
        """
        初始化CEA价格预测器
        
        Parameters:
        -----------
        data : DataFrame
            包含日期(date)和收盘价(close(RMB/ton))的数据框
        """
        self.data = data.copy()
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.last_date = self.data['date'].iloc[-1]
        self.last_price = self.data['close(RMB/ton)'].iloc[-1]
        
    def calculate_technical_indicators(self, price_series):
        """计算技术指标"""
        prices = price_series.values
        
        # 移动平均线
        if len(prices) >= 5:
            ma5 = np.mean(prices[-5:])
        else:
            ma5 = prices[-1]
            
        if len(prices) >= 10:
            ma10 = np.mean(prices[-10:])
        else:
            ma10 = ma5
            
        if len(prices) >= 20:
            ma20 = np.mean(prices[-20:])
        else:
            ma20 = ma10
        
        # RSI计算
        if len(prices) >= 14:
            deltas = np.diff(prices[-14:])
            gains = deltas[deltas > 0].sum() / 14 if len(deltas[deltas > 0]) > 0 else 0
            losses = -deltas[deltas < 0].sum() / 14 if len(deltas[deltas < 0]) > 0 else 0
            if losses == 0:
                rsi = 100
            else:
                rs = gains / losses
                rsi = 100 - (100 / (1 + rs))
        else:
            rsi = 50
        
        return {
            'ma5': ma5,
            'ma10': ma10,
            'ma20': ma20,
            'rsi': rsi
        }
    
    def original_prediction(self, steps=5):
        """原预测方法（简单趋势外推）"""
        price_series = self.data['close(RMB/ton)'].values
        
        # 计算近期趋势
        if len(price_series) >= 5:
            recent_trend = (price_series[-1] / price_series[-5]) ** (1/5) - 1
        else:
            recent_trend = 0
        
        predictions = []
        dates = []
        
        for i in range(1, steps + 1):
            pred_price = self.last_price * (1 + recent_trend) ** i
            predictions.append(pred_price)
            dates.append(self.last_date + timedelta(days=i))
            
        return predictions, dates
    
    def improved_prediction_v1(self, steps=5):
        """
        改进版本1：优化趋势权重和计算
        """
        price_series = self.data['close(RMB/ton)'].values
        predictions = []
        dates = []
        
        # 改进的趋势计算
        trends = []
        weights = []
        
        # 短期趋势（5天） - 降低权重
        if len(price_series) >= 5:
            short_trend = (price_series[-1] / price_series[-5]) ** (1/5) - 1
            trends.append(short_trend)
            weights.append(0.3)
        
        # 中期趋势（10天） - 主要权重
        if len(price_series) >= 10:
            mid_trend = (price_series[-1] / price_series[-10]) ** (1/10) - 1
            trends.append(mid_trend)
            weights.append(0.5)
        
        # 长期趋势（20天） - 稳定权重
        if len(price_series) >= 20:
            long_trend = (price_series[-1] / price_series[-20]) ** (1/20) - 1
            trends.append(long_trend)
            weights.append(0.4)
        
        # 添加均值回归趋势
        if len(price_series) >= 30:
            historical_mean = np.mean(price_series)
            mean_reversion_trend = (historical_mean - price_series[-1]) / price_series[-1] * 0.1
            trends.append(mean_reversion_trend)
            weights.append(0.3)
        
        # 加权平均趋势
        if trends:
            avg_trend = np.average(trends, weights=weights[:len(trends)])
        else:
            avg_trend = 0.001
        
        # 确保趋势不过于负面
        avg_trend = max(avg_trend, -0.005)
        
        # 计算历史波动率
        returns = np.diff(price_series) / price_series[:-1]
        hist_volatility = np.std(returns) if len(returns) > 0 else 0.01
        
        # 生成预测
        current_price = self.last_price
        
        for i in range(1, steps + 1):
            # 基础趋势（随时间衰减影响）
            trend_decay = max(0.3, 1.0 - (i * 0.15))
            base_pred = current_price * (1 + avg_trend * trend_decay)
            
            # 添加随机波动（随时间衰减）
            volatility_decay = max(0.3, 1.0 - (i * 0.2))
            volatility = hist_volatility * volatility_decay * 0.3
            noise = np.random.normal(0, volatility)
            
            # 最终预测
            final_pred = base_pred * (1 + noise)
            
            # 确保不过度偏离
            max_deviation = 0.015
            if abs(final_pred - current_price) / current_price > max_deviation:
                direction = 1 if final_pred > current_price else -1
                final_pred = current_price * (1 + direction * max_deviation)
            
            predictions.append(final_pred)
            dates.append(self.last_date + timedelta(days=i))
            current_price = final_pred
        
        return predictions, dates
    
    def improved_prediction_v2(self, steps=5):
        """
        改进版本2：加入技术指标
        """
        price_series = self.data['close(RMB/ton)'].values
        predictions = []
        dates = []
        
        # 计算技术指标
        tech_indicators = self.calculate_technical_indicators(pd.Series(price_series))
        
        # 基于技术指标调整趋势
        base_trend = 0.001
        
        # RSI判断超买超卖
        if tech_indicators['rsi'] < 30:
            rsi_adjustment = 0.003
        elif tech_indicators['rsi'] > 70:
            rsi_adjustment = -0.002
        else:
            rsi_adjustment = 0.001
        
        # 移动平均线判断趋势
        if self.last_price > tech_indicators['ma20']:
            ma_adjustment = 0.002
        else:
            ma_adjustment = -0.001
        
        # 组合调整
        avg_trend = base_trend + rsi_adjustment + ma_adjustment
        
        # 限制趋势范围
        avg_trend = max(min(avg_trend, 0.008), -0.004)
        
        # 生成预测
        current_price = self.last_price
        
        for i in range(1, steps + 1):
            # 趋势随时间线性衰减
            remaining_days = steps - i + 1
            trend_strength = remaining_days / steps
            
            predicted_price = current_price * (1 + avg_trend * trend_strength * 0.5)
            
            # 添加小幅随机波动
            small_noise = np.random.normal(0, 0.005)
            predicted_price *= (1 + small_noise)
            
            predictions.append(predicted_price)
            dates.append(self.last_date + timedelta(days=i))
            current_price = predicted_price
        
        return predictions, dates
    
    def improved_prediction_v3(self, steps=5):
        """
        改进版本3：针对CEA价格的改进预测模型
        """
        price_series = self.data['close(RMB/ton)'].values
        predictions = []
        dates = []
        
        # 计算历史统计指标
        hist_mean = np.mean(price_series)
        hist_std = np.std(price_series)
        hist_min = np.min(price_series)
        hist_max = np.max(price_series)
        
        # 判断当前位置
        is_low_position = self.last_price < hist_mean
        is_near_support = (self.last_price - hist_min) / (hist_max - hist_min) < 0.3
        
        # 计算近期趋势（加权，更重视近期数据）
        trend_windows = [3, 5, 8]
        trends = []
        weights = []
        
        for window in trend_windows:
            if len(price_series) >= window:
                trend = (price_series[-1] / price_series[-window]) - 1
                # 应用sigmoid函数压缩趋势值
                compressed_trend = 2 / (1 + np.exp(-5 * trend)) - 1
                trends.append(compressed_trend * 0.01)
                weights.append(window)
        
        # 计算均值回归力度
        if is_low_position:
            mean_reversion_strength = min(0.5, (hist_mean - self.last_price) / hist_mean * 0.5)
        else:
            mean_reversion_strength = (hist_mean - self.last_price) / hist_mean * 0.3
        
        # 计算支撑位效应
        support_effect = 0
        if is_near_support:
            distance_to_support = (self.last_price - hist_min) / hist_mean
            support_effect = max(0, 0.02 - distance_to_support * 0.1)
        
        # 组合趋势
        if trends:
            weighted_trend = np.average(trends, weights=weights)
        else:
            weighted_trend = 0
        
        # 生成预测
        current_price = self.last_price
        
        for i in range(1, steps + 1):
            # 趋势部分（随时间衰减）
            trend_component = weighted_trend * np.exp(-0.3 * i)
            
            # 均值回归部分（随时间增强）
            mr_component = mean_reversion_strength * (1 - np.exp(-0.2 * i)) * 0.1
            
            # 支撑位效应（随时间衰减）
            support_component = support_effect * np.exp(-0.4 * i)
            
            # 随机波动（随时间增大）
            volatility = hist_std / hist_mean * 0.1 * (1 + 0.1 * i)
            random_component = np.random.normal(0, volatility)
            
            # 组合所有因素
            daily_change = trend_component + mr_component + support_component + random_component
            
            # 限制单日涨跌幅
            daily_change = max(min(daily_change, 0.03), -0.03)
            
            # 计算新价格
            new_price = current_price * (1 + daily_change)
            
            predictions.append(new_price)
            dates.append(self.last_date + timedelta(days=i))
            current_price = new_price
        
        return predictions, dates
    
    def combined_prediction(self, steps=5):
        """
        组合方法：结合三种改进方法
        """
        # 获取三种方法的预测
        pred1, dates1 = self.improved_prediction_v1(steps)
        pred2, dates2 = self.improved_prediction_v2(steps)
        pred3, dates3 = self.improved_prediction_v3(steps)
        
        # 组合预测
        combined_predictions = []
        for i in range(steps):
            # 动态权重：v3（均值回归）权重随时间增加
            w1 = 0.4 - i * 0.05  # v1权重递减
            w2 = 0.3  # v2权重固定
            w3 = 0.3 + i * 0.05  # v3权重递增
            
            combined = (pred1[i] * w1 + pred2[i] * w2 + pred3[i] * w3)
            combined_predictions.append(combined)
        
        return combined_predictions, dates1
    
    def seasonal_adjustment(self, predictions, current_month=12):
        """
        添加季节性调整
        """
        # 假设12月有轻微的年末效应
        seasonal_factors = {
            1: 1.002, 2: 0.998, 3: 1.005, 4: 1.003,
            5: 0.997, 6: 0.995, 7: 0.993, 8: 0.998,
            9: 1.002, 10: 1.004, 11: 1.003, 12: 1.001
        }
        
        factor = seasonal_factors.get(current_month, 1.0)
        adjusted_predictions = [p * factor for p in predictions]
        
        return adjusted_predictions
    
    def smooth_predictions(self, predictions, sigma=0.8):
        """平滑预测结果"""
        from scipy.ndimage import gaussian_filter1d
        return gaussian_filter1d(predictions, sigma=sigma)
    
    def get_predictions(self, steps=5, method='combined'):
        """
        获取预测结果
        
        Parameters:
        -----------
        steps : int
            预测天数
        method : str
            预测方法: 'original', 'v1', 'v2', 'v3', 'combined'
            
        Returns:
        --------
        results : list
            包含每天预测结果的字典列表
        """
        # 根据方法选择预测函数
        if method == 'original':
            predictions, dates = self.original_prediction(steps)
        elif method == 'v1':
            predictions, dates = self.improved_prediction_v1(steps)
        elif method == 'v2':
            predictions, dates = self.improved_prediction_v2(steps)
        elif method == 'v3':
            predictions, dates = self.improved_prediction_v3(steps)
        else:  # combined
            predictions, dates = self.combined_prediction(steps)
        
        # 季节性调整
        current_month = self.last_date.month
        predictions = self.seasonal_adjustment(predictions, current_month)
        
        # 平滑处理
        try:
            from scipy.ndimage import gaussian_filter1d
            predictions = gaussian_filter1d(predictions, sigma=0.8)
        except ImportError:
            # 如果没有scipy，使用简单移动平均
            smoothed = []
            for i in range(len(predictions)):
                if i == 0:
                    smoothed.append(predictions[i] * 0.7 + predictions[i+1] * 0.3 if i+1 < len(predictions) else predictions[i])
                elif i == len(predictions) - 1:
                    smoothed.append(predictions[i-1] * 0.3 + predictions[i] * 0.7)
                else:
                    smoothed.append(predictions[i-1] * 0.2 + predictions[i] * 0.6 + predictions[i+1] * 0.2)
            predictions = smoothed
        
        # 确保预测的合理性
        hist_mean = np.mean(self.data['close(RMB/ton)'].values)
        hist_std = np.std(self.data['close(RMB/ton)'].values)
        
        for i in range(len(predictions)):
            lower_bound = hist_mean - 1.5 * hist_std
            upper_bound = hist_mean + 1.5 * hist_std
            predictions[i] = max(min(predictions[i], upper_bound), lower_bound)
        
        # 格式化结果
        results = []
        for i, (pred, date) in enumerate(zip(predictions, dates), 1):
            if i == 1:
                daily_change = (pred - self.last_price) / self.last_price * 100
            else:
                daily_change = (pred - predictions[i-2]) / predictions[i-2] * 100
            
            cumulative_change = (pred - self.last_price) / self.last_price * 100
            
            results.append({
                'date': date.strftime('%Y-%m-%d'),
                'day': f"第{i}天({date.strftime('%Y-%m-%d')})",
                'price': round(pred, 2),
                'cumulative_change': round(cumulative_change, 2),
                'daily_change': round(daily_change, 2)
            })
        
        return results

def load_sample_data():
    """加载示例数据（模拟数据）"""
    # 创建示例数据
    dates = pd.date_range(start='2025-11-01', end='2025-12-08', freq='D')
    np.random.seed(42)
    
    # 模拟价格数据：先涨后跌的趋势
    base_price = 58.0
    prices = []
    
    for i in range(len(dates)):
        if i < 20:  # 11月上涨
            price = base_price + i * 0.1 + np.random.normal(0, 0.5)
        else:  # 12月初下跌
            price = 60.0 - (i-20) * 0.15 + np.random.normal(0, 0.3)
        prices.append(price)
    
    data = pd.DataFrame({
        'date': dates,
        'close(RMB/ton)': prices
    })
    
    return data

def plot_single_method(historical_data, predictions, method_name="V3预测", title="CEA价格预测 - V3方法"):
    """
    绘制单个预测方法的图表
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 历史价格
    ax.plot(historical_data['date'], historical_data['close(RMB/ton)'], 
            'b-', label='历史价格', linewidth=2)
    
    # 预测价格
    pred_dates = [pd.to_datetime(p['date']) for p in predictions]
    pred_prices = [p['price'] for p in predictions]
    
    ax.plot(pred_dates, pred_prices, 'r--', 
            label=f'{method_name}', linewidth=2, markersize=8)
    
    # 连接点
    last_hist_date = historical_data['date'].iloc[-1]
    last_hist_price = historical_data['close(RMB/ton)'].iloc[-1]
    ax.plot([last_hist_date, pred_dates[0]], 
            [last_hist_price, pred_prices[0]], 
            'r--', linewidth=1, alpha=0.5)
    
    ax.set_title(title)
    ax.set_xlabel('日期')
    ax.set_ylabel('价格 (元/吨)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

def print_single_method_results(results, last_price, method_name="V3"):
    """打印单个方法的结果表格"""
    print("=" * 80)
    print(f"{method_name}方法预测结果")
    print("=" * 80)
    print(f"{'日期':<12} {'价格':<10} {'累计变化':<12} {'日变化':<10}")
    print("-" * 80)
    
    for result in results:
        cumulative_sign = "+" if result['cumulative_change'] >= 0 else ""
        daily_sign = "+" if result['daily_change'] >= 0 else ""
        
        print(f"{result['date']:<12} {result['price']:<10.2f} "
              f"{cumulative_sign}{result['cumulative_change']:<10.2f}% "
              f"{daily_sign}{result['daily_change']:<8.2f}%")
    
    print("=" * 80)
    print(f"当前价格: {last_price:.2f}")
    print("=" * 80)

def main():
    """主函数"""
    print("CEA价格预测系统 - V3方法")
    print("=" * 50)
    
    # 1. 加载数据
    print("正在加载数据...")
    conn = sqlite3.connect("../datas_for_CBAM/cbam_database.db")
    df= pd.read_sql_query('SELECT * FROM CEA_datas',conn)
    data = preprocess_cea_data(df)
    print(f"数据时间范围: {data['date'].iloc[0].strftime('%Y-%m-%d')} 到 {data['date'].iloc[-1].strftime('%Y-%m-%d')}")
    print(f"数据量: {len(data)} 条")
    print(f"最新价格: {data['close(RMB/ton)'].iloc[-1]:.2f}")
    
    # 2. 初始化预测器
    predictor = CEAPricePredictor(data)
    
    # 3. 只使用V3方法进行预测
    print("\n正在进行V3方法价格预测...")
    try:
        results = predictor.get_predictions(steps=30, method='v3')
        results_dict = {'v3': results}
    except Exception as e:
        print(f"V3方法预测失败: {e}")
        return None, None
    
    # 4. 打印结果
    
    print_single_method_results(results, predictor.last_price, "V3")
    
    # 5. 绘制图表
    print("\n生成V3预测图表...")
    try:
        plot_single_method(data, results, "V3预测", "CEA价格预测 - V3方法")
    except Exception as e:
        print(f"绘图失败: {e}")
    
    # 6. 预测分析总结
    print("\n" + "=" * 50)
    print("V3方法预测分析总结:")
    print("=" * 50)
    
    # 分析预测趋势
    changes = [r['cumulative_change'] for r in results]
    avg_change = np.mean(changes)
    volatility = np.std(changes)
    
    print(f"平均累计变化: {avg_change:.2f}%")
    print(f"预测波动性: {volatility:.2f}%")
    print()
    
    print("V3方法预测结果:")
    for result in results[:10]:  # 只显示前10天结果
        change_sign = "+" if result['cumulative_change'] >= 0 else ""
        daily_sign = "+" if result['daily_change'] >= 0 else ""
        print(f"  {result['day']}: {result['price']:.2f} "
              f"(累计{change_sign}{result['cumulative_change']:.2f}%, "
              f"日变化{daily_sign}{result['daily_change']:.2f}%)")
    
    if len(results) > 10:
        print(f"  ... (共{len(results)}天预测)")
    
    return predictor, results_dict

def plot_simple_comparison(historical_data, predictions_dict):
    """简化的对比图（备用方案）"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 历史价格
    ax.plot(historical_data['date'], historical_data['close(RMB/ton)'], 
            'b-', label='历史价格', linewidth=2)
    
    # 不同方法的预测价格
    colors = ['r--', 'g--', 'b--', 'm--', 'c--', 'y--']
    
    for idx, (method, predictions) in enumerate(predictions_dict.items()):
        pred_dates = [pd.to_datetime(p['date']) for p in predictions]
        pred_prices = [p['price'] for p in predictions]
        
        ax.plot(pred_dates, pred_prices, colors[idx % len(colors)], 
                label=f'{method}预测', linewidth=2, markersize=8)
        
        # 连接点
        last_hist_date = historical_data['date'].iloc[-1]
        last_hist_price = historical_data['close(RMB/ton)'].iloc[-1]
        ax.plot([last_hist_date, pred_dates[0]], 
                [last_hist_price, pred_prices[0]], 
                colors[idx % len(colors)], linewidth=1, alpha=0.5)
    
    ax.set_title('CEA价格预测对比')
    ax.set_xlabel('日期')
    ax.set_ylabel('价格 (元/吨)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 运行主程序
    predictor, all_results = main()
    
    # # 用户可以使用自己的数据
    # print("\n" + "=" * 50)
    # print("使用自己的数据:")
    # print("=" * 50)
    # print("""
    # 1. 准备数据框，包含两列: 'date' 和 'close(RMB/ton)'
    # 2. 创建预测器: predictor = CEAPricePredictor(your_data)
    # 3. 获取V3预测: results = predictor.get_predictions(steps=5, method='v3')
    # 4. 查看结果: for r in results: print(r)
    # """)