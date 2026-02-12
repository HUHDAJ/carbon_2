import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# 数据预处理
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

# 改进的预测函数
def improved_future_predict(data, steps=5):
    """
    改进的未来预测函数
    """
    last_price = data['close(RMB/ton)'].iloc[-1]
    last_date = data['date'].iloc[-1]
    
    # 计算多种趋势指标
    trends = []
    
    # 短期趋势（5天）
    if len(data) >= 5:
        short_trend = data['close(RMB/ton)'].iloc[-1] / data['close(RMB/ton)'].iloc[-5] - 1
        trends.append(short_trend*0.4)
    
    # 中期趋势（10天）
    if len(data) >= 10:
        mid_trend = data['close(RMB/ton)'].iloc[-1] / data['close(RMB/ton)'].iloc[-10] - 1
        trends.append(mid_trend * 0.5)  # 赋予较低权重
    
    # 长期趋势（20天）
    if len(data) >= 20:
        long_trend = data['close(RMB/ton)'].iloc[-1] / data['close(RMB/ton)'].iloc[-20] - 1
        trends.append(long_trend * 0.8)  # 赋予更低权重
    
    # 计算平均趋势
    avg_trend = np.mean(trends) if trends else -0.001
    
    # 计算历史波动率
    returns = data['close(RMB/ton)'].pct_change().dropna()
    hist_volatility = returns.std() if len(returns) > 0 else 0.01
    
    # 生成预测
    predictions = [last_price]  # 第0天是最后已知价格
    
    for i in range(1, steps + 1):
        # 基础趋势
        base_pred = predictions[-1] * (1 + avg_trend)
        
        # 添加随机波动（随时间衰减）
        decay = max(0.5, 1.0 - (i * 0.1))
        volatility = hist_volatility * decay * 0.5
        noise = np.random.normal(0, volatility)
        
        # 最终预测
        final_pred = base_pred * (1 + noise)
        
        # 确保不过度偏离
        max_deviation = 0.02  # 单日最大偏离2%
        prev_pred = predictions[-1]
        if abs(final_pred - prev_pred) / prev_pred > max_deviation:
            direction = 1 if final_pred > prev_pred else -1
            final_pred = prev_pred * (1 + direction * max_deviation)
        
        predictions.append(final_pred)
    
    # 返回未来steps天的预测（不包括第0天）
    future_predictions = predictions[1:]
    
    # 生成预测日期
    prediction_dates = [last_date + timedelta(days=i) for i in range(1, steps + 1)]
    
    return future_predictions, prediction_dates, last_price, last_date

# 主程序
def main_improved_prediction():
    print("="*80)
    print("CEA价格预测")
    print("="*80)
    
    # 读取数据
    df = pd.read_csv('./CEA_original_data_v1.0.csv')
    
    # 预处理
    data = preprocess_cea_data(df)
    
    # 划分训练测试集
    split_idx = int(len(data) * 0.8)
    train_data = data.iloc[:split_idx]
    test_data = data.iloc[split_idx:]
    
    # 在测试集上评估改进方法
    test_predictions = []
    test_actuals = []
    
    for i in range(20, len(test_data)):
        # 使用前20天数据预测下一天
        window_data = test_data.iloc[max(0, i-20):i]
        if len(window_data) >= 5:  # 至少有5天数据
            preds, _, _, _ = improved_future_predict(window_data, steps=1)
            if preds:
                test_predictions.append(preds[0])
                test_actuals.append(test_data.iloc[i]['close(RMB/ton)'])
    
    # 计算评估指标
    if test_predictions and test_actuals:
        mae = mean_absolute_error(test_actuals, test_predictions)
        rmse = np.sqrt(mean_squared_error(test_actuals, test_predictions))
        mape = np.mean(np.abs((np.array(test_actuals) - np.array(test_predictions)) / np.array(test_actuals))) * 100
        
        print(f"\n改进方法在测试集上的性能:")
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"MAPE: {mape:.2f}%")
    
    # 预测未来5天
    print(f"\n预测未来5天价格...")
    
    # 使用最后60天数据
    lookback = max(20, len(data))
    latest_data = data.iloc[-lookback:]
    
    predictions, pred_dates, last_price, last_date = improved_future_predict(latest_data, steps=18)
    
    print(f"最后已知: {last_date.date()}, 价格: {last_price:.2f}")
    print(f"\n未来5天预测结果:")
    
    for i, (date, price) in enumerate(zip(pred_dates, predictions), 1):
        change = (price - last_price) / last_price * 100
        daily_change = 0 if i == 1 else (price - predictions[i-2]) / predictions[i-2] * 100
        print(f"  第{i}天 ({date.date()}): {price:.2f} (累计{change:+.2f}%, 日变化{daily_change:+.2f}%)")
    
    # 绘制图表
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    plt.figure(figsize=(14, 6))
    
    # 历史最后20天
    history_days = 20
    hist_data = data.iloc[-history_days:]
    plt.plot(hist_data['date'], hist_data['close(RMB/ton)'], 'b-', 
             label='历史价格', linewidth=2, marker='o', markersize=4)
    
    # 未来预测
    plt.plot(pred_dates, predictions, 'r-', 
             label='未来预测', linewidth=2.5, marker='s', markersize=6)
    
    # 连接点
    plt.plot([hist_data['date'].iloc[-1], pred_dates[0]], 
             [hist_data['close(RMB/ton)'].iloc[-1], predictions[0]], 
             'k--', alpha=0.3, linewidth=1)
    
    plt.title('CEA价格预测', fontsize=16)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('价格 (RMB/ton)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    return predictions, pred_dates

if __name__ == "__main__":
    predictions, dates = main_improved_prediction()