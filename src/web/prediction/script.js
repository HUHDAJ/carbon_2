// ====================== 全局常量（日期配置）======================
const DEFAULT_CARBON_START = "2025-12-28";
const DEFAULT_CARBON_END   = "2026-01-28";
const DEFAULT_CARBON_DAYS  = 32;  // 2025-12-28 到 2026-01-28 包含两端共32天

const DEFAULT_CBAM_START   = "2025-12-28";
const DEFAULT_CBAM_END     = "2026-01-28";
const DEFAULT_CBAM_DAYS    = 32;

// ====================== 静态预测数据（直接从CSV嵌入）======================
//电碳因子
const carbonFactorStaticData = [
    { date: "2025-12-28", price: 0.722887, cumulative_change: -0.000355, daily_change: -0.000355 },
    { date: "2025-12-29", price: 0.724050, cumulative_change: 0.000808, daily_change: 0.001163 },
    { date: "2025-12-30", price: 0.724228, cumulative_change: 0.000986, daily_change: 0.000178 },
    { date: "2025-12-31", price: 0.727015, cumulative_change: 0.003772, daily_change: 0.002787 },
    { date: "2026-01-01", price: 0.724272, cumulative_change: 0.001029, daily_change: -0.002743 },
    { date: "2026-01-02", price: 0.721410, cumulative_change: -0.001833, daily_change: -0.002862 },
    { date: "2026-01-03", price: 0.722985, cumulative_change: -0.000257, daily_change: 0.001576 },
    { date: "2026-01-04", price: 0.721022, cumulative_change: -0.002221, daily_change: -0.001964 },
    { date: "2026-01-05", price: 0.717849, cumulative_change: -0.005394, daily_change: -0.003173 },
    { date: "2026-01-06", price: 0.717405, cumulative_change: -0.005838, daily_change: -0.000444 },
    { date: "2026-01-07", price: 0.718438, cumulative_change: -0.004805, daily_change: 0.001033 },
    { date: "2026-01-08", price: 0.719306, cumulative_change: -0.003937, daily_change: 0.000868 },
    { date: "2026-01-09", price: 0.715710, cumulative_change: -0.007533, daily_change: -0.003596 },
    { date: "2026-01-10", price: 0.717678, cumulative_change: -0.005565, daily_change: 0.001968 },
    { date: "2026-01-11", price: 0.715616, cumulative_change: -0.007627, daily_change: -0.002062 },
    { date: "2026-01-12", price: 0.712765, cumulative_change: -0.010477, daily_change: -0.002851 },
    { date: "2026-01-13", price: 0.712817, cumulative_change: -0.010426, daily_change: 0.000052 },
    { date: "2026-01-14", price: 0.713868, cumulative_change: -0.009375, daily_change: 0.001051 },
    { date: "2026-01-15", price: 0.715020, cumulative_change: -0.008223, daily_change: 0.001152 },
    { date: "2026-01-16", price: 0.711480, cumulative_change: -0.011763, daily_change: -0.003540 },
    { date: "2026-01-17", price: 0.714182, cumulative_change: -0.009061, daily_change: 0.002702 },
    { date: "2026-01-18", price: 0.712644, cumulative_change: -0.010599, daily_change: -0.001538 },
    { date: "2026-01-19", price: 0.710340, cumulative_change: -0.012903, daily_change: -0.002304 },
    { date: "2026-01-20", price: 0.710999, cumulative_change: -0.012243, daily_change: 0.000660 },
    { date: "2026-01-21", price: 0.711757, cumulative_change: -0.011486, daily_change: 0.000757 },
    { date: "2026-01-22", price: 0.713256, cumulative_change: -0.009987, daily_change: 0.001499 },
    { date: "2026-01-23", price: 0.709675, cumulative_change: -0.013568, daily_change: -0.003581 },
    { date: "2026-01-24", price: 0.712928, cumulative_change: -0.010314, daily_change: 0.003254 },
    { date: "2026-01-25", price: 0.711612, cumulative_change: -0.011631, daily_change: -0.001316 },
    { date: "2026-01-26", price: 0.709722, cumulative_change: -0.013521, daily_change: -0.001890 },
    { date: "2026-01-27", price: 0.711062, cumulative_change: -0.012180, daily_change: 0.001340 },
    { date: "2026-01-28", price: 0.711444, cumulative_change: -0.011798, daily_change: 0.000382 },
    { date: "2026-01-29", price: 0.713054, cumulative_change: -0.010189, daily_change: 0.001609 },
    { date: "2026-01-30", price: 0.709288, cumulative_change: -0.013955, daily_change: -0.003766 },
    { date: "2026-01-31", price: 0.712886, cumulative_change: -0.010356, daily_change: 0.003599 },
    // 后续数据省略，仅保留到2026-01-28
];

// CBAM税负预测数据
const cbamStaticData = [
    { date: "2025-12-28", price: 59.72, cumulative_change: 1.39, daily_change: 1.39 },
    { date: "2025-12-29", price: 59.72, cumulative_change: 1.39, daily_change: 0.0 },
    { date: "2025-12-30", price: 59.72, cumulative_change: 1.39, daily_change: 0.0 },
    { date: "2025-12-31", price: 59.72, cumulative_change: 1.39, daily_change: 0.0 },
    { date: "2026-01-01", price: 59.72, cumulative_change: 1.39, daily_change: 0.0 },
    { date: "2026-01-02", price: 59.72, cumulative_change: 1.39, daily_change: 0.0 },
    { date: "2026-01-03", price: 59.72, cumulative_change: 1.39, daily_change: 0.0 },
    { date: "2026-01-04", price: 60.05, cumulative_change: 1.96, daily_change: 0.56 },
    { date: "2026-01-05", price: 59.96, cumulative_change: 1.8, daily_change: -0.15 },
    { date: "2026-01-06", price: 60.1, cumulative_change: 2.03, daily_change: 0.22 },
    { date: "2026-01-07", price: 61.08, cumulative_change: 3.69, daily_change: 1.63 },
    { date: "2026-01-08", price: 61.86, cumulative_change: 5.02, daily_change: 1.28 },
    { date: "2026-01-09", price: 61.54, cumulative_change: 4.48, daily_change: -0.51 },
    { date: "2026-01-10", price: 61.91, cumulative_change: 5.11, daily_change: 0.6 },
    { date: "2026-01-11", price: 63.35, cumulative_change: 7.56, daily_change: 2.33 },
    { date: "2026-01-12", price: 64.64, cumulative_change: 9.74, daily_change: 2.02 },
    { date: "2026-01-13", price: 64.78, cumulative_change: 9.99, daily_change: 0.23 },
    { date: "2026-01-14", price: 64.06, cumulative_change: 8.76, daily_change: -1.12 },
    { date: "2026-01-15", price: 62.58, cumulative_change: 6.25, daily_change: -2.31 },
    { date: "2026-01-16", price: 61.3, cumulative_change: 4.08, daily_change: -2.05 },
    { date: "2026-01-17", price: 60.98, cumulative_change: 3.54, daily_change: -0.52 },
    { date: "2026-01-18", price: 61.19, cumulative_change: 3.88, daily_change: 0.33 },
    { date: "2026-01-19", price: 62.42, cumulative_change: 5.98, daily_change: 2.02 },
    { date: "2026-01-20", price: 64.23, cumulative_change: 9.05, daily_change: 2.9 },
    { date: "2026-01-21", price: 66.06, cumulative_change: 12.15, daily_change: 2.84 },
    { date: "2026-01-22", price: 67.24, cumulative_change: 14.16, daily_change: 1.78 },
    { date: "2026-01-23", price: 67.59, cumulative_change: 14.76, daily_change: 0.53 },
    { date: "2026-01-24", price: 68.71, cumulative_change: 16.66, daily_change: 1.66 },
    { date: "2026-01-25", price: 70.25, cumulative_change: 19.27, daily_change: 2.24 },
    { date: "2026-01-26", price: 71.11, cumulative_change: 20.73, daily_change: 1.23 },
    { date: "2026-01-27", price: 70.11, cumulative_change: 19.03, daily_change: -1.41 },
    { date: "2026-01-28", price: 69.12, cumulative_change: 17.36, daily_change: -1.41 }
    // 后续数据省略，仅保留到2026-01-28
];

document.addEventListener('DOMContentLoaded', function() {
    // 初始化预测类型选择
    const typeCards = document.querySelectorAll('.type-card');
    const predictionSections = document.querySelectorAll('.list-section');
    
    window.selectPredictionType = function(type) {
        console.log('切换预测类型:', type);
        typeCards.forEach(c => c.classList.remove('active'));
        document.querySelector(`.type-card[data-type="${type}"]`).classList.add('active');
        predictionSections.forEach(section => section.classList.remove('active'));
        document.getElementById(`${type}-prediction`).classList.add('active');
        
        if (type === 'carbon-factor') {
            initializeCarbonFactorPrediction();
        } else {
            initializeCBAMTaxPrediction();
        }
    };
    
    setDefaultDates();
    initializeCarbonFactorPrediction();
    
    // Chart.js 全局设置
    Chart.defaults.font.family = "'Microsoft YaHei', 'Segoe UI', Arial, sans-serif";
    Chart.defaults.font.size = 14;
    Chart.defaults.color = '#333';
    Chart.defaults.elements.line.tension = 0.3;
    Chart.defaults.elements.point.radius = 4;
    Chart.defaults.elements.point.hoverRadius = 6;

    // 日期变更自动计算天数
    const carbonStart = document.getElementById('forecast-start-date');
    const carbonEnd   = document.getElementById('forecast-end-date');
    if (carbonStart && carbonEnd) {
        carbonStart.addEventListener('change', calcCarbonDays);
        carbonEnd.addEventListener('change', calcCarbonDays);
    }

    const cbamStart = document.getElementById('cbam-start-date');
    const cbamEnd   = document.getElementById('cbam-end-date');
    if (cbamStart && cbamEnd) {
        cbamStart.addEventListener('change', calcCBAMDays);
        cbamEnd.addEventListener('change', calcCBAMDays);
    }

    calcCarbonDays();
    calcCBAMDays();
});

// ----------------------------- 天数计算函数 -----------------------------
function calcCarbonDays() {
    const startInput = document.getElementById('forecast-start-date');
    const endInput = document.getElementById('forecast-end-date');
    const daysInput = document.getElementById('forecast-days');
    const summaryDays = document.getElementById('carbon-days');

    if (!startInput || !endInput || !daysInput) return;

    const start = new Date(startInput.value);
    const end = new Date(endInput.value);
    if (start && end && start <= end) {
        const diffTime = Math.abs(end - start);
        const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
        daysInput.value = days;
        if (summaryDays) summaryDays.textContent = days;
    }
}

function calcCBAMDays() {
    const startInput = document.getElementById('cbam-start-date');
    const endInput = document.getElementById('cbam-end-date');
    const daysInput = document.getElementById('cbam-days');
    const summaryDays = document.getElementById('tax-days');

    if (!startInput || !endInput || !daysInput) return;

    const start = new Date(startInput.value);
    const end = new Date(endInput.value);
    if (start && end && start <= end) {
        const diffTime = Math.abs(end - start);
        const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
        daysInput.value = days;
        if (summaryDays) summaryDays.textContent = days;
    }
}

// ----------------------------- 设置默认日期 -----------------------------
function setDefaultDates() {
    console.log('设置默认日期：2025-12-28 至 2026-01-28');

    // 电碳因子预测
    const carbonStart = document.getElementById('forecast-start-date');
    const carbonEnd = document.getElementById('forecast-end-date');
    const carbonDaysInput = document.getElementById('forecast-days');
    if (carbonStart) carbonStart.value = DEFAULT_CARBON_START;
    if (carbonEnd) carbonEnd.value = DEFAULT_CARBON_END;
    if (carbonDaysInput) carbonDaysInput.value = DEFAULT_CARBON_DAYS;

    // CBAM预测
    const cbamStart = document.getElementById('cbam-start-date');
    const cbamEnd = document.getElementById('cbam-end-date');
    const cbamDaysInput = document.getElementById('cbam-days');
    if (cbamStart) cbamStart.value = DEFAULT_CBAM_START;
    if (cbamEnd) cbamEnd.value = DEFAULT_CBAM_END;
    if (cbamDaysInput) cbamDaysInput.value = DEFAULT_CBAM_DAYS;
}

// ----------------------------- 工具函数 -----------------------------
function calculateDaysBetween(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
}

function fixCanvasBlur(canvas) {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return ctx;
}

function showLoading(message) {
    let loadingDiv = document.getElementById('loading-indicator');
    if (!loadingDiv) {
        loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading-indicator';
        loadingDiv.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.7);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            color: white;
            font-size: 18px;
        `;
        document.body.appendChild(loadingDiv);
    }
    loadingDiv.innerHTML = `
        <div class="spinner" style="border: 5px solid rgba(255,255,255,0.3); border-top: 5px solid #4caf50; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite;"></div>
        <p style="margin-top: 25px; font-size: 18px; font-weight: bold;">${message}</p>
        <p style="margin-top: 10px; font-size: 14px; opacity: 0.8;">请稍候...</p>
    `;
    loadingDiv.style.display = 'flex';
}

function hideLoading() {
    const loadingDiv = document.getElementById('loading-indicator');
    if (loadingDiv) loadingDiv.style.display = 'none';
}

function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    const notification = document.createElement('div');
    notification.className = `notification ${type === 'error' ? 'error' : ''}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#ff4444' : '#2196f3'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        font-size: 14px;
    `;
    notification.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function formatDate(gmtStr) {
    const date = new Date(gmtStr);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// ----------------------------- 图表通用配置 -----------------------------
function getChartOptions(yAxisTitle, chartTitle) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: true, position: 'top', labels: { font: { size: 14 } } },
            title: { display: true, text: chartTitle, font: { size: 16 } },
            tooltip: { mode: 'index', intersect: false }
        },
        scales: {
            x: {
                title: { display: true, text: '日期', font: { size: 14 } },
                ticks: { font: { size: 12 }, maxTicksLimit: 10 }
            },
            y: {
                title: { display: true, text: yAxisTitle, font: { size: 14 } },
                beginAtZero: false,
                ticks: { font: { size: 12 } }
            }
        }
    };
}

// ----------------------------- 电碳因子预测（使用静态数据）-----------------------------
window.runCarbonFactorPrediction = async function() {
    console.log('运行电碳因子预测（静态数据）');
    const startDate = document.getElementById('forecast-start-date').value;
    const endDate = document.getElementById('forecast-end-date').value;
    if (!startDate || !endDate || new Date(endDate) <= new Date(startDate)) {
        showNotification('请选择正确的日期范围', 'error');
        return;
    }
    const days = calculateDaysBetween(startDate, endDate);
    showLoading('正在加载电碳因子预测数据...');
    
    try {
        // 从静态数据中筛选日期范围
        const filtered = carbonFactorStaticData.filter(item => 
            item.date >= startDate && item.date <= endDate
        );
        
        if (filtered.length === 0) {
            throw new Error('所选日期范围内无预测数据');
        }

        const predictionData = {
            dates: filtered.map(d => d.date),
            values: filtered.map(d => d.price),
            cumulative: filtered.map(d => d.cumulative_change),
            daily: filtered.map(d => d.daily_change),
            raw: filtered
        };

        updateCarbonFactorChart(predictionData, startDate, endDate);
        updateCarbonFactorSummary(startDate, endDate, days, predictionData);
        updateCarbonFactorInsights(predictionData);
        fillCarbonDataTable(predictionData.raw);
        
        showNotification(`电碳因子预测完成！共 ${filtered.length} 天数据`, 'success');
    } catch (error) {
        console.error('预测失败:', error);
        showNotification(`预测失败: ${error.message}`, 'error');
        document.getElementById('carbon-insights').innerHTML = `
            <div class="insight-item">
                <h4><i class="fas fa-exclamation-triangle"></i> 错误</h4>
                <p>${error.message}</p>
                <small>请检查预测数据是否包含所选日期范围</small>
            </div>
        `;
    } finally {
        hideLoading();
    }
};

function initializeCarbonFactorPrediction() {
    console.log('初始化电碳因子预测');
    resetCarbonFactorDisplay();
    const btn = document.querySelector('#carbon-factor-prediction .btn-primary');
    if (btn) btn.onclick = runCarbonFactorPrediction;
}

function resetCarbonFactorDisplay() {
    const canvas = document.getElementById('carbon-factor-forecast-chart');
    if (!canvas) return;
    if (window.carbonFactorChart) window.carbonFactorChart.destroy();
    fixCanvasBlur(canvas);
    window.carbonFactorChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: { labels: [], datasets: [{
            label: '电碳因子预测',
            data: [],
            borderColor: '#4caf50',
            backgroundColor: 'rgba(76,175,80,0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.3
        }]},
        options: getChartOptions('电碳因子 (kgCO₂/kWh)', '电碳因子预测')
    });
    updateCarbonFactorSummaryDisplay(DEFAULT_CARBON_START, DEFAULT_CARBON_END, DEFAULT_CARBON_DAYS);
    document.getElementById('carbon-insights').innerHTML = `
        <div class="insight-item">
            <h4><i class="fas fa-info-circle"></i> 提示</h4>
            <p>请先设置预测日期并运行预测以获取数据</p>
            <small>点击"运行预测"按钮开始分析</small>
        </div>
    `;
    // 清空表格
    const tableBody = document.querySelector('#carbon-data-table tbody');
    if (tableBody) tableBody.innerHTML = '<tr><td colspan="4" class="empty-tip">请先运行预测</td></tr>';
}

function updateCarbonFactorChart(data, startDate, endDate) {
    const canvas = document.getElementById('carbon-factor-forecast-chart');
    if (!canvas) return;
    fixCanvasBlur(canvas);
    if (window.carbonFactorChart) window.carbonFactorChart.destroy();
    window.carbonFactorChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: '电碳因子预测',
                data: data.values,
                borderColor: '#4caf50',
                backgroundColor: 'rgba(76,175,80,0.1)',
                borderWidth: 3,
                pointBackgroundColor: '#4caf50',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
                fill: true,
                tension: 0.3
            }]
        },
        options: getChartOptions('电碳因子 (kgCO₂/kWh)', '电碳因子预测结果')
    });
}

function updateCarbonFactorSummary(startDate, endDate, days, data) {
    document.getElementById('carbon-start-date').textContent = startDate;
    document.getElementById('carbon-end-date').textContent = endDate;
    document.getElementById('carbon-days').textContent = data.values.length;
    const summaryGrid = document.querySelector('#carbon-factor-prediction .summary-grid');
    let startValElem = document.getElementById('carbon-start-value');
    if (!startValElem) {
        startValElem = document.createElement('div');
        startValElem.className = 'summary-item';
        startValElem.id = 'carbon-start-value';
        summaryGrid.appendChild(startValElem);
    }
    startValElem.innerHTML = `
        <div class="summary-label">预测起始值</div>
        <div class="summary-value">${data.values[0].toFixed(4)} kgCO₂/kWh</div>
    `;
}

function updateCarbonFactorSummaryDisplay(startDate, endDate, days) {
    document.getElementById('carbon-start-date').textContent = startDate;
    document.getElementById('carbon-end-date').textContent = endDate;
    document.getElementById('carbon-days').textContent = days;
}

function updateCarbonFactorInsights(data) {
    const insightsDiv = document.getElementById('carbon-insights');
    if (!data || !data.values || data.values.length === 0) {
        insightsDiv.innerHTML = `<div class="insight-item"><h4>提示</h4><p>无预测数据</p></div>`;
        return;
    }
    const firstVal = data.values[0];
    const lastVal = data.values[data.values.length - 1];
    const changePercent = ((lastVal - firstVal) / firstVal * 100).toFixed(2);
    const avgVal = data.values.reduce((a,b)=>a+b,0)/data.values.length;
    const maxVal = Math.max(...data.values);
    const minVal = Math.min(...data.values);
    
    let trendDesc = '平稳';
    let advice = '';
    let color = '#2196f3';
    if (lastVal > firstVal) {
        trendDesc = '上升';
        color = '#ff9800';
        advice = '建议考虑清洁能源采购或能效提升项目';
    } else if (lastVal < firstVal) {
        trendDesc = '下降';
        color = '#4caf50';
        advice = '当前能源结构良好，可维持现有策略';
    }
    
    insightsDiv.innerHTML = `
        <div class="insight-item">
            <h4><i class="fas fa-chart-line"></i> 趋势分析</h4>
            <p>预测期内电碳因子将<span style="color: ${color}; font-weight: bold;">${changePercent >= 0 ? '上升' : '下降'} ${Math.abs(changePercent)}%</span></p>
            <small>整体趋势：${trendDesc}</small>
            <small>${advice}</small>
        </div>
        <div class="insight-item">
            <h4><i class="fas fa-chart-bar"></i> 统计概览</h4>
            <p>平均电碳因子: <strong>${avgVal.toFixed(4)} kgCO₂/kWh</strong></p>
            <small>最高: ${maxVal.toFixed(4)} | 最低: ${minVal.toFixed(4)}</small>
        </div>
        <div class="insight-item">
            <h4><i class="fas fa-lightbulb"></i> 运营建议</h4>
            <p>${changePercent >= 0 ? '建议考虑清洁能源采购或能效提升项目' : '当前能源结构良好，可维持现有策略'}</p>
            <small>${changePercent >= 0 ? '可考虑安装光伏系统或购买绿证' : '继续保持节能减排措施'}</small>
        </div>
    `;
}

// 填充电碳因子数据明细表格
function fillCarbonDataTable(rows) {
    const tbody = document.querySelector('#carbon-data-table tbody');
    if (!tbody) return;
    if (!rows || rows.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-tip">无数据</td></tr>';
        return;
    }
    let html = '';
    rows.forEach(row => {
        html += `<tr>
            <td>${row.date}</td>
            <td>${row.price.toFixed(4)}</td>
            <td>${row.cumulative_change.toFixed(2)}</td>
            <td>${row.daily_change.toFixed(2)}</td>
        </tr>`;
    });
    tbody.innerHTML = html;
}

// ----------------------------- CBAM税负预测（使用静态数据）-----------------------------
window.runCBAMTaxPrediction = async function() {
    console.log('运行CBAM税负预测（静态数据）');
    
    const startDate = document.getElementById('cbam-start-date').value;
    const endDate = document.getElementById('cbam-end-date').value;

    if (!startDate || !endDate || new Date(endDate) <= new Date(startDate)) {
        showNotification('请选择正确的日期范围（结束日期 > 开始日期）', 'error');
        return;
    }

    const days = calculateDaysBetween(startDate, endDate);
    showLoading('正在加载CBAM预测数据...');

    try {
        // 从静态数据中筛选日期范围
        const filtered = cbamStaticData.filter(item => 
            item.date >= startDate && item.date <= endDate
        );

        if (filtered.length === 0) {
            throw new Error('所选日期范围内无CBAM预测数据');
        }

        const predictionData = {
            dates: filtered.map(d => d.date),
            values: filtered.map(d => d.price),
            cumulative: filtered.map(d => d.cumulative_change),
            daily: filtered.map(d => d.daily_change),
            raw: filtered
        };

        updateCBAMTaxChart(predictionData, startDate, endDate);
        updateCBAMTaxSummary(startDate, endDate, days, predictionData);
        updateCBAMTaxInsights(predictionData);
        fillCBAMDataTable(predictionData.raw);

        showNotification(`CBAM税负预测完成！共 ${filtered.length} 条数据`, 'success');
    } catch (error) {
        console.error('CBAM预测失败:', error);
        showNotification(`CBAM预测失败: ${error.message}`, 'error');
        const insightsDiv = document.getElementById('tax-insights');
        if (insightsDiv) {
            insightsDiv.innerHTML = `
                <div class="insight-item">
                    <h4><i class="fas fa-exclamation-triangle"></i> 数据提示</h4>
                    <p>${error.message}</p>
                    <small>当前CBAM预测数据起始日期为2025-12-28</small>
                </div>
            `;
        }
    } finally {
        hideLoading();
    }
};

function initializeCBAMTaxPrediction() {
    console.log('初始化CBAM税负预测');
    resetCBAMTaxDisplay();
    const btn = document.querySelector('#cbam-tax-prediction .btn-primary');
    if (btn) btn.onclick = runCBAMTaxPrediction;
}

function resetCBAMTaxDisplay() {
    const canvas = document.getElementById('cbam-tax-forecast-chart');
    if (!canvas) return;
    if (window.cbamTaxChart) window.cbamTaxChart.destroy();
    fixCanvasBlur(canvas);
    window.cbamTaxChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: { labels: [], datasets: [{
            label: 'CBAM税负预测',
            data: [],
            borderColor: '#2196f3',
            backgroundColor: 'rgba(33,150,243,0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.3
        }]},
        options: getChartOptions('CBAM税负 (元)', 'CBAM税负预测')
    });
    document.getElementById('tax-start-date-display').textContent = DEFAULT_CBAM_START;
    document.getElementById('tax-end-date-display').textContent = DEFAULT_CBAM_END;
    document.getElementById('tax-days').textContent = DEFAULT_CBAM_DAYS;
    document.getElementById('tax-insights').innerHTML = `
        <div class="insight-item">
            <h4><i class="fas fa-info-circle"></i> 提示</h4>
            <p>请先设置预测日期并运行预测以获取数据</p>
            <small>点击"运行预测"按钮开始分析</small>
        </div>
    `;
    // 清空表格
    const tbody = document.querySelector('#cbam-data-table tbody');
    if (tbody) tbody.innerHTML = '<tr><td colspan="4" class="empty-tip">请先运行预测</td></tr>';
}

function updateCBAMTaxChart(data, startDate, endDate) {
    const canvas = document.getElementById('cbam-tax-forecast-chart');
    if (!canvas) return;
    fixCanvasBlur(canvas);
    if (window.cbamTaxChart) window.cbamTaxChart.destroy();
    window.cbamTaxChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'CBAM税负预测',
                data: data.values,
                borderColor: '#2196f3',
                backgroundColor: 'rgba(33,150,243,0.1)',
                borderWidth: 3,
                pointBackgroundColor: '#2196f3',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
                fill: true,
                tension: 0.3
            }]
        },
        options: getChartOptions('CBAM税负 (元)', 'CBAM税负预测结果')
    });
}

function updateCBAMTaxSummary(startDate, endDate, days, data) {
    document.getElementById('tax-start-date-display').textContent = startDate;
    document.getElementById('tax-end-date-display').textContent = endDate;
    document.getElementById('tax-days').textContent = data.values.length;
    const summaryGrid = document.querySelector('#cbam-tax-prediction .summary-grid');
    let startValElem = document.getElementById('tax-start-value');
    if (!startValElem) {
        startValElem = document.createElement('div');
        startValElem.className = 'summary-item';
        startValElem.id = 'tax-start-value';
        summaryGrid.appendChild(startValElem);
    }
    startValElem.innerHTML = `
        <div class="summary-label">预测起始税负</div>
        <div class="summary-value">${data.values[0].toFixed(2)} 元</div>
    `;
}

function updateCBAMTaxInsights(data) {
    const insightsDiv = document.getElementById('tax-insights');
    if (!data || !data.values || data.values.length === 0) {
        insightsDiv.innerHTML = `<div class="insight-item"><h4>提示</h4><p>无预测数据</p></div>`;
        return;
    }
    const firstVal = data.values[0];
    const lastVal = data.values[data.values.length - 1];
    const changePercent = ((lastVal - firstVal) / firstVal * 100).toFixed(2);
    const avgVal = data.values.reduce((a,b)=>a+b,0)/data.values.length;
    const total = data.values.reduce((a,b)=>a+b,0);
    const monthlyAvg = total / (data.values.length / 30);
    
    let trendDesc = '平稳';
    let advice = '';
    let color = '#2196f3';
    if (lastVal > firstVal) {
        trendDesc = '上升';
        color = '#ff9800';
        advice = '建议提前进行税务规划，考虑碳减排投资';
    } else if (lastVal < firstVal) {
        trendDesc = '下降';
        color = '#4caf50';
        advice = '税负趋势良好，可维持当前减排策略';
    }
    
    insightsDiv.innerHTML = `
        <div class="insight-item">
            <h4><i class="fas fa-chart-line"></i> 趋势预测</h4>
            <p>预测期内CBAM税负将<span style="color: ${color}; font-weight: bold;">${changePercent >= 0 ? '上升' : '下降'} ${Math.abs(changePercent)}%</span></p>
            <small>整体趋势：${trendDesc}</small>
            <small>${advice}</small>
        </div>
        <div class="insight-item">
            <h4><i class="fas fa-chart-bar"></i> 统计信息</h4>
            <p>平均税负: <strong>${avgVal.toFixed(2)} 元</strong></p>
            <small>预测期总税负: ${total.toFixed(2)} 元 | 月均约: ${monthlyAvg.toFixed(2)} 元</small>
        </div>
        <div class="insight-item">
            <h4><i class="fas fa-lightbulb"></i> 财务建议</h4>
            <p>${changePercent >= 0 ? '建议提前进行税务规划，考虑碳减排投资' : '税负趋势良好，可维持当前减排策略'}</p>
            <small>${changePercent >= 0 ? '可考虑绿色能源采购或能效提升项目' : '当前策略有效，可进一步优化'}</small>
        </div>
    `;
}

// 填充CBAM数据明细表格
function fillCBAMDataTable(rows) {
    const tbody = document.querySelector('#cbam-data-table tbody');
    if (!tbody) return;
    if (!rows || rows.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-tip">无数据</td></tr>';
        return;
    }
    let html = '';
    rows.forEach(row => {
        html += `<tr>
            <td>${row.date}</td>
            <td>${row.price.toFixed(2)}</td>
            <td>${row.cumulative_change.toFixed(2)}</td>
            <td>${row.daily_change.toFixed(2)}</td>
        </tr>`;
    });
    tbody.innerHTML = html;
}