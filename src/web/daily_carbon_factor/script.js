/**
 * 电碳因子查询前端逻辑（适配中文列名 + 查询地区取自下拉框）
 * =====================================================
 * 后端接口 /api/carbon-factor/daily-all 返回的数据格式：
 * [
 *   { "日期": "2022-01-01", "电力碳因子(kgCO2e/kWh)": 0.716368 },
 *   ...
 * ]
 * 
 * ⚠️ 注意：数据库中无地区字段，因此所有地区查询均返回同一份数据。
 *   但页面上的「查询地区」下拉框会真实显示在结果中，以保持界面一致性。
 * =====================================================
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== 电碳因子查询页面加载 (适配中文列名 + 查询地区取自下拉框) ===');
    loadDailyCarbonFactorsData();
});

let dailyCarbonFactorsData = [];

/**
 * 从后端加载数据，并将字段名转换为统一的英文格式
 */
async function loadDailyCarbonFactorsData() {
    try {
        const response = await fetch("/api/carbon-factor/daily-all");
        if (!response.ok) {
            throw new Error(`HTTP错误：${response.status}`);
        }
        const result = await response.json();

        if (result.code !== 200) {
            throw new Error(result.msg || "数据读取失败");
        }

        // 转换字段名：中文 → 英文（date / carbon_factor）
        dailyCarbonFactorsData = result.data.map(item => ({
            date: item['日期'],
            carbon_factor: item['电力碳因子(kgCO2e/kWh)']
        }));

        console.log("✅ 每日碳因子数据加载完成，共", dailyCarbonFactorsData.length, "条记录");
        console.log("示例记录：", dailyCarbonFactorsData[0]);

        // 数据加载成功后初始化页面
        initializePage();

    } catch (error) {
        console.error("❌ 每日碳因子数据加载失败：", error.message);
        showNotification("每日碳因子数据加载失败：" + error.message, 'error');
        dailyCarbonFactorsData = [];
        initializePage();
    }
}

// ---------- 初始化页面 ----------
function initializePage() {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth() + 1;
    const day = today.getDate();

    // 年份：从数据中提取所有年份，若数据为空则提供默认范围
    const yearSelect = document.getElementById('query-year');
    yearSelect.innerHTML = '';
    let years = [];
    if (dailyCarbonFactorsData.length > 0) {
        years = [...new Set(dailyCarbonFactorsData.map(item => item.date.split('-')[0]))].sort();
    }
    if (years.length === 0) {
        years = ['2022', '2023', '2024'];
    }
    years.forEach(y => {
        const option = document.createElement('option');
        option.value = y;
        option.textContent = `${y}年`;
        if (y == year) option.selected = true;
        yearSelect.appendChild(option);
    });

    // 月份：1-12
    const monthSelect = document.getElementById('query-month');
    monthSelect.innerHTML = '';
    for (let m = 1; m <= 12; m++) {
        const option = document.createElement('option');
        option.value = m;
        option.textContent = `${m}月`;
        if (m === month) option.selected = true;
        monthSelect.appendChild(option);
    }

    updateDayOptions();
    setupEventListeners();
}

// 更新日期下拉框（基于选中年月）
function updateDayOptions() {
    const year = parseInt(document.getElementById('query-year').value);
    const month = parseInt(document.getElementById('query-month').value);
    const daySelect = document.getElementById('query-day');
    const daysInMonth = new Date(year, month, 0).getDate();
    const currentDay = parseInt(daySelect.value) || 1;

    daySelect.innerHTML = '';
    for (let d = 1; d <= daysInMonth; d++) {
        const option = document.createElement('option');
        option.value = d;
        option.textContent = `${d}日`;
        if (d === currentDay) option.selected = true;
        daySelect.appendChild(option);
    }
    if (currentDay > daysInMonth) daySelect.value = daysInMonth;
}

// 事件监听
function setupEventListeners() {
    document.getElementById('query-year').addEventListener('change', updateDayOptions);
    document.getElementById('query-month').addEventListener('change', updateDayOptions);
    document.getElementById('queryBtn').addEventListener('click', loadCarbonFactor);
    document.getElementById('resetBtn').addEventListener('click', resetQuery);
    document.getElementById('history-period').addEventListener('change', function() {
        const dateStr = getSelectedDate();
        if (dateStr) loadHistoricalData(dateStr);
    });
}

// 获取选中日期字符串（YYYY-MM-DD）
function getSelectedDate() {
    const year = document.getElementById('query-year').value;
    const month = String(document.getElementById('query-month').value).padStart(2, '0');
    const day = String(document.getElementById('query-day').value).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// ---------- 查询核心：按日期查找，忽略地区 ----------
function loadCarbonFactor() {
    const dateStr = getSelectedDate();
    if (!dateStr) {
        showNotification('请选择完整的查询日期', 'error');
        return;
    }

    // 从全局数据中查找匹配日期的记录（忽略地区）
    const record = dailyCarbonFactorsData.find(r => r.date === dateStr);
    if (!record) {
        hideResultsCard();
        showNotification(`${dateStr} 无碳因子数据`, 'warning');
        return;
    }

    // 获取下拉框选中的地区文本（用于显示）
    const regionSelect = document.getElementById('region-select');
    const selectedRegion = regionSelect.options[regionSelect.selectedIndex].text;

    // 展示数据，地区显示为用户选择的地区
    displayCarbonFactor(record, selectedRegion, dateStr);
    showNotification(`${dateStr} ${selectedRegion} 电碳因子查询成功！`, 'success');
    loadHistoricalData(dateStr);
}

/**
 * 加载历史数据（忽略地区，仅按日期筛选）
 * @param {string} baseDate - 基准日期（YYYY-MM-DD）
 */
function loadHistoricalData(baseDate) {
    const period = parseInt(document.getElementById('history-period').value);
    
    // 筛选：日期 <= baseDate
    const filtered = dailyCarbonFactorsData.filter(r => r.date <= baseDate);
    // 按日期降序排列
    const sorted = filtered.sort((a, b) => (a.date > b.date ? -1 : 1));
    const historyData = sorted.slice(0, period).map(r => ({
        date: r.date,
        carbon_factor: r.carbon_factor
    }));

    displayHistoricalData(historyData);
}

// ---------- 渲染UI ----------
function displayCarbonFactor(record, region, originalDate) {
    const dateParts = record.date.split('-');
    const displayDate = `${dateParts[0]}年${parseInt(dateParts[1])}月${parseInt(dateParts[2])}日`;

    document.getElementById('query-date-display').textContent = displayDate;
    document.getElementById('query-region-display').textContent = region; // 显示用户选择的地区

    const summaryHtml = `
        <div class="data-item">
            <span class="data-label">电碳因子值</span>
            <span class="data-value">${record.carbon_factor.toFixed(3)}<span class="data-unit">kgCO₂/kWh</span></span>
        </div>
        <div class="data-item">
            <span class="data-label">数据日期</span>
            <span class="data-value">${record.date}</span>
        </div>
        ${originalDate !== record.date ? `
        <div class="data-item">
            <span class="data-label">原始查询日期</span>
            <span class="data-value">${originalDate}</span>
        </div>` : ''}
        <div class="data-item">
            <span class="data-label">数据来源</span>
            <span class="data-value">后端碳因子库</span>
        </div>
    `;
    document.getElementById('carbon-factor-summary').innerHTML = summaryHtml;
    document.getElementById('current-result-card').style.display = 'block';
}

function displayHistoricalData(data) {
    if (!data || data.length === 0) {
        document.getElementById('historical-data-container').innerHTML = '<div class="no-data">暂无历史数据</div>';
        return;
    }

    let tableHtml = `<table class="data-table"><thead><tr><th>日期</th><th>电碳因子 (kgCO₂/kWh)</th><th>变化趋势</th></tr></thead><tbody>`;
    // 最新在上
    for (let i = 0; i < data.length; i++) {
        const item = data[i];
        const displayDate = item.date.slice(5); // MM-DD
        let trend = '', trendClass = '';
        if (i < data.length - 1) {
            const prev = data[i + 1];
            if (item.carbon_factor > prev.carbon_factor) { trend = '↑'; trendClass = 'trend-up'; }
            else if (item.carbon_factor < prev.carbon_factor) { trend = '↓'; trendClass = 'trend-down'; }
            else { trend = '→'; trendClass = 'trend-stable'; }
        } else { trend = '-'; }
        const rowClass = i === data.length - 1 ? 'current-row' : '';
        tableHtml += `<tr class="${rowClass}"><td>${displayDate}</td><td>${item.carbon_factor.toFixed(3)}</td><td class="${trendClass}">${trend}</td></tr>`;
    }
    tableHtml += `</tbody></table>`;
    document.getElementById('historical-data-container').innerHTML = tableHtml;
}

function hideResultsCard() {
    document.getElementById('current-result-card').style.display = 'none';
}

// 重置查询
function resetQuery() {
    if (!confirm('确定要重置查询条件吗？所有查询结果将被清除。')) return;
    const today = new Date();
    document.getElementById('query-year').value = today.getFullYear();
    document.getElementById('query-month').value = today.getMonth() + 1;
    updateDayOptions();
    setTimeout(() => {
        document.getElementById('query-day').value = today.getDate();
    }, 50);
    // 重置地区下拉框为默认值（华中）
    document.getElementById('region-select').value = '华中';
    document.getElementById('history-period').value = '30';
    hideResultsCard();
    showNotification('查询条件已重置', 'info');
}

// 通知（保持与原版一致）
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    else if (type === 'error') icon = 'fa-exclamation-circle';
    else if (type === 'warning') icon = 'fa-exclamation-triangle';
    notification.innerHTML = `<i class="fas ${icon}"></i><span>${message}</span>`;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}