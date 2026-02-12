let cbamForecastData = [];

async function loadCBAMForecastData() {
    try {
        const response = await fetch("/api/cbam/forecast");
        if (!response.ok) {
            throw new Error(`HTTP错误：${response.status}`);
        }
        const result = await response.json();

        if (result.code !== 200) {
            throw new Error(result.msg || "数据读取失败");
        }

        cbamForecastData = result.data;
        console.log("✅ CBAM预测数据加载完成：", cbamForecastData);

        // 调用原有渲染函数（需自行实现，此处仅占位）
        if (typeof renderCBAMForecast === 'function') {
            renderCBAMForecast(cbamForecastData);
        }
    } catch (error) {
        console.error("❌ CBAM数据加载失败：", error.message);
        alert("CBAM预测数据加载失败：" + error.message);
    }
}

// ========== 原CBAM计算代码（保持不变） ==========
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== CBAM计算页面开始加载 ===');

    // 新增：读取CBAM预测数据（不影响原有计算）
    loadCBAMForecastData();

    // 从基础信息读取企业数据
    const currentEnterprise = JSON.parse(localStorage.getItem('current-enterprise-info') || '{}');
    console.log('当前企业信息:', currentEnterprise);

    // 核心元素获取
    const cbamIndustryType = document.getElementById('cbamIndustryType');
    const cbamProductType = document.getElementById('cbamProductType');
    const cbamRegion = document.getElementById('cbamRegion');
    const calcDate = document.getElementById('calcDate');
    const importCarbonFootprintBtn = document.getElementById('importCarbonFootprintBtn');
    const scope1Emissions = document.getElementById('scope1-emissions');
    const scope2Emissions = document.getElementById('scope2-emissions');

    // 行业-产品映射（每个行业仅保留一个对应产品）
    const industryProductMap = {
        'steel': [
            { value: 'rebar', text: '螺纹钢' }
        ],
        'cement': [
            { value: 'clinker', text: '水泥熟料' }
        ],
        'fertilizer': [
            { value: 'urea', text: '尿素' }
        ]
    };

    // 初始化：填充基础信息
    if (currentEnterprise.industryType) {
        cbamIndustryType.value = currentEnterprise.industryType;
        updateProductOptions(currentEnterprise.industryType);
    }

    if (currentEnterprise.region) {
        cbamRegion.value = currentEnterprise.region.replace('地区', '');
    }

    // 默认选中当前日期
    const today = new Date().toISOString().split('T')[0];
    calcDate.value = today;

    // 从碳足迹结果导入数据
    importCarbonFootprintBtn.addEventListener('click', function() {
        const carbonFootprintData = JSON.parse(localStorage.getItem('carbon-footprint-results') || '{}');
        const scope1Result = parseFloat(localStorage.getItem('scope1Result') || '0');
        const scope2Result = parseFloat(localStorage.getItem('scope2Result') || '0');

        if (scope1Result > 0 || scope2Result > 0) {
            scope1Emissions.value = scope1Result.toFixed(2);
            scope2Emissions.value = scope2Result.toFixed(2);
            showNotification(`成功导入碳足迹数据：Scope1=${scope1Result.toFixed(2)} tCO₂, Scope2=${scope2Result.toFixed(2)} tCO₂`, 'success');
        } else if (carbonFootprintData.scope1Total) {
            scope1Emissions.value = carbonFootprintData.scope1Total.toFixed(2);
            scope2Emissions.value = carbonFootprintData.scope2Total.toFixed(2);
            showNotification(`成功导入碳足迹数据：Scope1=${carbonFootprintData.scope1Total.toFixed(2)} tCO₂, Scope2=${carbonFootprintData.scope2Total.toFixed(2)} tCO₂`, 'success');
        } else {
            showNotification('未找到可用的碳足迹计算结果，请先完成碳足迹计算', 'error');
        }
    });

    // 行业变化时更新产品选项
    cbamIndustryType.addEventListener('change', function() {
        updateProductOptions(this.value);
    });

    // 更新产品下拉选项函数
    function updateProductOptions(industryVal) {
        cbamProductType.innerHTML = '';

        if (!industryVal) {
            cbamProductType.innerHTML = '<option value="">请先选择行业</option>';
            return;
        }

        const products = industryProductMap[industryVal] || [];

        if (products.length > 0) {
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '请选择产品';
            cbamProductType.appendChild(defaultOption);

            products.forEach(product => {
                const option = document.createElement('option');
                option.value = product.value;
                option.textContent = product.text;
                cbamProductType.appendChild(option);
            });
        } else {
            cbamProductType.innerHTML = '<option value="">暂无对应产品</option>';
        }
    }

    // 加载保存的输入数据
    loadSavedInputData();

    console.log('=== CBAM计算页面加载完成 ===');
});

// 计算CBAM税额
function calculateCBAM() {
    console.log('开始计算CBAM税额');

    if (!validateBasicInfo()) {
        return;
    }

    const data = collectCBAMData();

    try {
        showNotification('正在计算CBAM税额...', 'info');

        const results = calculateCBAMLocally(data);

        displayCBAMResults(results);

        saveInputData(data);

        showNotification('CBAM计算成功！', 'success');

    } catch (error) {
        console.error('计算失败:', error);
        showNotification(`计算失败: ${error.message}`, 'error');
    }
}

// 验证基本信息
function validateBasicInfo() {
    const industry = document.getElementById('cbamIndustryType').value;
    const product = document.getElementById('cbamProductType').value;
    const region = document.getElementById('cbamRegion').value;
    const calcDateValue = document.getElementById('calcDate').value;

    if (!industry) {
        showNotification('请选择行业类型', 'error');
        return false;
    }

    if (!product) {
        showNotification('请选择产品类型', 'error');
        return false;
    }

    if (!region) {
        showNotification('请选择所属地区', 'error');
        return false;
    }

    if (!calcDateValue) {
        showNotification('请选择计算时间', 'error');
        return false;
    }

    // 验证排放数据及新增字段
    const scope1 = parseFloat(document.getElementById('scope1-emissions').value);
    const scope2 = parseFloat(document.getElementById('scope2-emissions').value);
    const quantity = parseFloat(document.getElementById('product-quantity').value);
    const euPrice = parseFloat(document.getElementById('eu-carbon-price').value);
    const cnPrice = parseFloat(document.getElementById('cn-carbon-price').value);
    const rate = parseFloat(document.getElementById('exchange-rate').value);
    const euFree = parseFloat(document.getElementById('eu-free-allowance').value);

    if (isNaN(scope1) || scope1 < 0) {
        showNotification('请输入有效的Scope 1排放量', 'error');
        return false;
    }
    if (isNaN(scope2) || scope2 < 0) {
        showNotification('请输入有效的Scope 2排放量', 'error');
        return false;
    }
    if (isNaN(quantity) || quantity <= 0) {
        showNotification('请输入有效的产品数量', 'error');
        return false;
    }
    if (isNaN(euPrice) || euPrice <= 0) {
        showNotification('请输入有效的欧盟碳价', 'error');
        return false;
    }
    if (isNaN(cnPrice) || cnPrice <= 0) {
        showNotification('请输入有效的中国碳价', 'error');
        return false;
    }
    if (isNaN(rate) || rate <= 0) {
        showNotification('请输入有效的汇率', 'error');
        return false;
    }
    if (isNaN(euFree) || euFree < 0 || euFree > 100) {
        showNotification('请输入有效的欧盟免费配额比例(0-100)', 'error');
        return false;
    }

    return true;
}

// 收集CBAM数据
function collectCBAMData() {
    const industry = document.getElementById('cbamIndustryType').value;
    const product = document.getElementById('cbamProductType').value;
    const region = document.getElementById('cbamRegion').value;
    const calcDateValue = document.getElementById('calcDate').value;
    const scope1 = parseFloat(document.getElementById('scope1-emissions').value);
    const scope2 = parseFloat(document.getElementById('scope2-emissions').value);
    const quantity = parseFloat(document.getElementById('product-quantity').value);
    const euPrice = parseFloat(document.getElementById('eu-carbon-price').value);
    const cnPrice = parseFloat(document.getElementById('cn-carbon-price').value);
    const rate = parseFloat(document.getElementById('exchange-rate').value);
    const cnFree = parseFloat(document.getElementById('cn-free-allowance').value);
    const euFree = parseFloat(document.getElementById('eu-free-allowance').value);

    return {
        calculation_date: calcDateValue,
        industry: industry,
        product: product,
        region: region,
        scope1_emissions: scope1,
        scope2_emissions: scope2,
        product_quantity: quantity,
        eu_carbon_price: euPrice,
        cn_carbon_price: cnPrice,
        exchange_rate: rate,
        cn_free_allowance: cnFree,
        eu_free_allowance: euFree,
        calculated_at: new Date().toISOString()
    };
}

// 本地CBAM计算逻辑（完整抵扣公式）
function calculateCBAMLocally(data) {
    console.log('本地计算CBAM:', data);

    const totalEmissions = data.scope1_emissions + data.scope2_emissions;
    const unitCarbonFootprint = data.product_quantity > 0 ? totalEmissions / data.product_quantity : 0;

    // 将中国碳价换算为欧元
    const cnPriceInEuro = data.cn_carbon_price * data.exchange_rate;
    // 免费配额比例转换为小数
    const cnFreeRate = data.cn_free_allowance / 100;
    const euFreeRate = data.eu_free_allowance / 100;

    let cbamTax;
    // 根据原Python逻辑：若中国免费配额 <=0，视为无免费配额，仅抵扣中国已支付碳价
    if (data.cn_free_allowance <= 0) {
        // 无中国免费配额：需支付欧盟排放量 × (欧盟碳价 - 中国碳价欧元)
        const euPayableEmissions = totalEmissions * (1 - euFreeRate);
        cbamTax = (data.eu_carbon_price - cnPriceInEuro) * euPayableEmissions;
    } else {
        // 有中国免费配额：欧盟碳价×欧盟应税排放 - 中国碳价×中国应税排放
        const euPayableEmissions = totalEmissions * (1 - euFreeRate);
        const cnPayableEmissions = totalEmissions * (1 - cnFreeRate);
        cbamTax = data.eu_carbon_price * euPayableEmissions - cnPriceInEuro * cnPayableEmissions;
    }

    // 税额不应为负数（若抵扣后为负，按0处理）
    cbamTax = Math.max(0, cbamTax);

    return {
        total_emissions: totalEmissions,
        unit_carbon_footprint: unitCarbonFootprint,
        cbam_tax: cbamTax,
        eu_carbon_price: data.eu_carbon_price,
        cn_carbon_price: data.cn_carbon_price,
        exchange_rate: data.exchange_rate,
        cn_free_allowance: data.cn_free_allowance,
        eu_free_allowance: data.eu_free_allowance,
        ...data
    };
}

// 显示CBAM计算结果
function displayCBAMResults(data) {
    console.log('显示CBAM结果:', data);

    document.getElementById('results-card').style.display = 'block';

    // 主要结果
    document.getElementById('cbam-tax').textContent = data.cbam_tax ? data.cbam_tax.toFixed(2) : '0.00';
    document.getElementById('total-emissions-result').textContent = data.total_emissions ? data.total_emissions.toFixed(2) : '0.00';
    document.getElementById('unit-carbon-footprint').textContent = data.unit_carbon_footprint ? data.unit_carbon_footprint.toFixed(2) : '0.00';
    document.getElementById('carbon-price').textContent = data.eu_carbon_price ? data.eu_carbon_price.toFixed(2) : '0.00';

    // 详细计算结果
    document.getElementById('detail-scope1').textContent = data.scope1_emissions ? data.scope1_emissions.toFixed(2) : '0.00';
    document.getElementById('detail-scope2').textContent = data.scope2_emissions ? data.scope2_emissions.toFixed(2) : '0.00';
    document.getElementById('detail-quantity').textContent = data.product_quantity ? data.product_quantity.toFixed(2) : '0.00';
    document.getElementById('detail-unit-footprint').textContent = data.unit_carbon_footprint ? data.unit_carbon_footprint.toFixed(2) : '0.00';
    document.getElementById('detail-carbon-price').textContent = data.eu_carbon_price ? data.eu_carbon_price.toFixed(2) : '0.00';
    // 新增详细字段
    document.getElementById('detail-cn-price').textContent = data.cn_carbon_price ? data.cn_carbon_price.toFixed(2) : '0.00';
    document.getElementById('detail-exchange-rate').textContent = data.exchange_rate ? data.exchange_rate.toFixed(4) : '0.0000';
    document.getElementById('detail-cn-free').textContent = data.cn_free_allowance ? data.cn_free_allowance.toFixed(1) : '0.0';
    document.getElementById('detail-eu-free').textContent = data.eu_free_allowance ? data.eu_free_allowance.toFixed(1) : '0.0';
    document.getElementById('detail-cbam-tax').textContent = data.cbam_tax ? data.cbam_tax.toFixed(2) : '0.00';

    document.getElementById('results-card').scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// 保存输入数据到本地存储
function saveInputData(inputData) {
    localStorage.setItem('cbamInputData', JSON.stringify(inputData));
    localStorage.setItem('cbamSelectedIndustry', inputData.industry);
    localStorage.setItem('cbamSelectedProduct', inputData.product);
    localStorage.setItem('cbamSelectedRegion', inputData.region);
    localStorage.setItem('cbamCalculationDate', inputData.calculation_date);

    // 保存计算结果摘要
    const results = {
        total_emissions: inputData.scope1_emissions + inputData.scope2_emissions,
        unit_carbon_footprint: inputData.product_quantity > 0 ? 
            (inputData.scope1_emissions + inputData.scope2_emissions) / inputData.product_quantity : 0,
        cbam_tax: (inputData.scope1_emissions + inputData.scope2_emissions) * inputData.eu_carbon_price, // 仅为简化存储，实际以详细计算为准
        calculation_date: new Date().toISOString()
    };
    localStorage.setItem('cbamResults', JSON.stringify(results));
}

// 从本地存储加载保存的输入数据
function loadSavedInputData() {
    const savedIndustry = localStorage.getItem('cbamSelectedIndustry');
    const savedProduct = localStorage.getItem('cbamSelectedProduct');
    const savedRegion = localStorage.getItem('cbamSelectedRegion');
    const savedDate = localStorage.getItem('cbamCalculationDate');

    if (savedIndustry) {
        document.getElementById('cbamIndustryType').value = savedIndustry;
        const event = new Event('change');
        document.getElementById('cbamIndustryType').dispatchEvent(event);

        setTimeout(() => {
            if (savedProduct) {
                document.getElementById('cbamProductType').value = savedProduct;
            }
        }, 100);
    }

    if (savedRegion) {
        document.getElementById('cbamRegion').value = savedRegion;
    }

    if (savedDate) {
        document.getElementById('calcDate').value = savedDate;
    }

    const savedInputData = localStorage.getItem('cbamInputData');
    if (savedInputData) {
        const data = JSON.parse(savedInputData);
        document.getElementById('scope1-emissions').value = data.scope1_emissions || '0';
        document.getElementById('scope2-emissions').value = data.scope2_emissions || '0';
        document.getElementById('product-quantity').value = data.product_quantity || '1';
        document.getElementById('eu-carbon-price').value = data.eu_carbon_price || '65.00';
        // 加载新增字段
        document.getElementById('cn-carbon-price').value = data.cn_carbon_price || '60.00';
        document.getElementById('exchange-rate').value = data.exchange_rate || '0.13';
        document.getElementById('cn-free-allowance').value = data.cn_free_allowance || '0';
        document.getElementById('eu-free-allowance').value = data.eu_free_allowance || '0';
    }

    document.getElementById('results-card').style.display = 'none';
}

// 重置CBAM计算
function resetCBAM() {
    console.log('重置CBAM数据');

    if (!confirm('确定要重置所有数据吗？所有输入和计算结果将被清除。')) {
        return;
    }

    document.getElementById('cbamIndustryType').value = '';
    document.getElementById('cbamProductType').innerHTML = '<option value="">请先选择行业</option>';
    document.getElementById('cbamRegion').value = '';

    const today = new Date().toISOString().split('T')[0];
    document.getElementById('calcDate').value = today;

    document.getElementById('scope1-emissions').value = '0';
    document.getElementById('scope2-emissions').value = '0';
    document.getElementById('product-quantity').value = '1';
    document.getElementById('eu-carbon-price').value = '65.00';
    // 重置新增字段为默认值
    document.getElementById('cn-carbon-price').value = '60.00';
    document.getElementById('exchange-rate').value = '0.13';
    document.getElementById('cn-free-allowance').value = '0';
    document.getElementById('eu-free-allowance').value = '0';

    document.getElementById('results-card').style.display = 'none';

    localStorage.removeItem('cbamInputData');
    localStorage.removeItem('cbamSelectedIndustry');
    localStorage.removeItem('cbamSelectedProduct');
    localStorage.removeItem('cbamSelectedRegion');
    localStorage.removeItem('cbamCalculationDate');
    localStorage.removeItem('cbamResults');

    showNotification('表单已重置', 'info');
}

// 显示通知
function showNotification(message, type) {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) existingNotification.remove();

    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}