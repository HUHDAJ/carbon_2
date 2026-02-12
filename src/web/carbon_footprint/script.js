document.addEventListener('DOMContentLoaded', function() {
    console.log('=== 碳足迹页面开始加载 (新版) ===');
    
    // 从基础信息读取企业数据
    const currentEnterprise = JSON.parse(localStorage.getItem('current-enterprise-info') || '{}');
    
    // 核心元素获取
    const cfIndustryType = document.getElementById('cfIndustryType');
    const productType = document.getElementById('productType');
    const cfRegion = document.getElementById('cfRegion');
    const calcDate = document.getElementById('calcDate');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    const scope1Form = document.getElementById('scope1Form');
    const scope2Form = document.getElementById('scope2Form');
    const getCarbonFactorBtn = document.getElementById('getCarbonFactorBtn');
    const calcTotalBtn = document.getElementById('calcTotalBtn');
    const carbonFactor = document.getElementById('carbonFactor');
    const processEmissionContainer = document.getElementById('processEmissionContainer');
    const processEmissionTitle = document.getElementById('processEmissionTitle');
    const processDescription = document.getElementById('process-description');
    const resetScope1Btn = document.getElementById('resetScope1Btn');
    const resetScope2Btn = document.getElementById('resetScope2Btn');
    const resetAllBtn = document.getElementById('resetAllBtn');
    
    // 结果存储
    let scope1ResultVal = 0, scope2ResultVal = 0, fuelEmissionVal = 0, processEmissionVal = 0;
    
    // ---------- 新版行业-产品映射（仅保留需求产品）--------
    const industryProductMap = {
        'steel': [{ value: 'rebar', text: '螺纹钢' }],
        'cement': [{ value: 'clinker', text: '水泥熟料' }],
        'fertilizer': [{ value: 'urea', text: '尿素' }]
    };

    // ---------- 新版过程排放配置（完整参数 + 合理因子）--------
    const processEmissionMap = {
        'steel': {
            'rebar': {
                name: '螺纹钢',
                description: '电弧炉/转炉炼钢过程排放参数',
                inputs: [
                    { id: 'pig_iron_weight', label: '生铁消耗量 (吨)', description: '炼钢用生铁' },
                    { id: 'direct_reduced_iron', label: '直接还原铁消耗量 (吨)', description: 'DRI消耗' },
                    { id: 'fe_ni', label: '镍铁消耗量 (吨)', description: '镍铁合金' },
                    { id: 'fe_cr', label: '铬铁消耗量 (吨)', description: '铬铁合金' },
                    { id: 'mo_fe', label: '钼铁消耗量 (吨)', description: '钼铁合金' },
                    { id: 'caco3', label: '碳酸钙 (石灰石) 消耗量 (吨)', description: '造渣剂' },
                    { id: 'electrode', label: '电极消耗量 (吨)', description: '石墨电极' }
                ],
                factors: {
                    'pig_iron_weight': 1.8,
                    'direct_reduced_iron': 1.5,
                    'fe_ni': 2.0,
                    'fe_cr': 1.9,
                    'mo_fe': 2.1,
                    'caco3': 0.4,
                    'electrode': 0.8
                }
            }
        },
        'cement': {
            'clinker': {
                name: '水泥熟料',
                description: '水泥熟料煅烧过程排放',
                inputs: [
                    { id: 'feco3', label: '菱铁矿消耗量 (吨)', description: '碳酸亚铁' },
                    { id: 'caco3', label: '石灰石消耗量 (吨)', description: '碳酸钙' },
                    { id: 'dolomitic', label: '白云石消耗量 (吨)', description: '碳酸镁钙' }
                ],
                factors: {
                    'feco3': 0.3,
                    'caco3': 0.5,
                    'dolomitic': 0.45
                }
            }
        },
        'fertilizer': {
            'urea': {
                name: '尿素',
                description: '尿素合成过程排放',
                inputs: [
                    { id: 'ammonia_coal', label: '煤头氨消耗量 (吨)', description: '以煤为原料的合成氨' },
                    { id: 'ammonia_gas', label: '气头氨消耗量 (吨)', description: '以天然气为原料的合成氨' },
                    { id: 'final_urea', label: '最终尿素产量 (吨)', description: '尿素产品' }
                ],
                factors: {
                    'ammonia_coal': 1.6,
                    'ammonia_gas': 1.2,
                    'final_urea': 0.5
                }
            }
        }
    };

    // ---------- 燃料排放因子（煤炭7、燃油5、燃气7）--------
    const FUEL_FACTORS = {
        coal: [2.66, 2.55, 2.48, 2.40, 2.32, 2.25, 2.18], // 吨CO₂/吨
        oil:  [3.16, 3.10, 3.05, 2.98, 2.90],            // 吨CO₂/吨
        gas:  [1.98, 1.92, 1.85, 1.78, 1.70, 1.65, 1.58] // 吨CO₂/万立方米
    };

    // ---------- 地区电碳因子（固定）--------
    const REGION_FACTORS = {
        '华中': 0.852, '华南': 0.785, '华北': 0.921,
        '华东': 0.812, '西南': 0.898, '西北': 0.756
    };

    // ---------- 工具函数：更新本地存储中的碳足迹结果（供CBAM导入）--------
    function updateCarbonFootprintStorage() {
        // 存储独立数值（便于CBAM页面直接读取）
        localStorage.setItem('scope1Result', scope1ResultVal.toString());
        localStorage.setItem('scope2Result', scope2ResultVal.toString());
        
        // 存储完整对象（包含基础信息，便于扩展）
        const carbonFootprintResults = {
            scope1Total: scope1ResultVal,
            scope2Total: scope2ResultVal,
            calcDate: calcDate.value,
            industry: cfIndustryType.value,
            product: productType.value,
            productText: productType.selectedOptions[0]?.text || '',
            region: cfRegion.value,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('carbon-footprint-results', JSON.stringify(carbonFootprintResults));
        console.log('✅ 碳足迹结果已保存到 localStorage', carbonFootprintResults);
    }

    // ---------- 初始化：填充企业信息 & 默认日期--------
    if (currentEnterprise.industryType) {
        cfIndustryType.value = currentEnterprise.industryType;
        updateProductOptions(currentEnterprise.industryType);
    }
    if (currentEnterprise.region) {
        cfRegion.value = currentEnterprise.region.replace('地区', '');
    }
    calcDate.value = new Date().toISOString().split('T')[0];

    // ---------- 行业变化--------
    cfIndustryType.addEventListener('change', function() {
        updateProductOptions(this.value);
        // 清空过程排放容器
        processEmissionContainer.innerHTML = `<div class="no-process-data"><i class="fas fa-industry"></i><p>请选择产品类型</p></div>`;
        processEmissionTitle.innerHTML = '<i class="fas fa-industry"></i> 过程排放';
        processDescription.textContent = '请先选择行业和产品以显示过程排放表单';
        document.querySelector('.process-card')?.classList.remove('product-selected');
    });

    // ---------- 产品变化：动态生成过程排放表单--------
    productType.addEventListener('change', function() {
        const industry = cfIndustryType.value;
        const product = this.value;
        if (!industry || !product) {
            processEmissionContainer.innerHTML = `<div class="no-process-data"><i class="fas fa-industry"></i><p>请先选择行业和产品</p></div>`;
            return;
        }

        const config = processEmissionMap[industry]?.[product];
        if (!config) {
            processEmissionContainer.innerHTML = `<div class="no-process-data"><i class="fas fa-exclamation-triangle"></i><h4>暂无过程排放配置</h4><p>当前产品暂未配置参数</p></div>`;
            processEmissionTitle.innerHTML = `<i class="fas fa-industry"></i> ${productType.selectedOptions[0]?.text || '产品'} 过程排放`;
            processDescription.textContent = '该产品暂无过程排放参数配置';
            return;
        }

        // 更新标题与描述
        processEmissionTitle.innerHTML = `<i class="fas fa-industry"></i> ${config.name} 过程排放`;
        processDescription.textContent = config.description;

        // 生成输入字段
        let html = '';
        config.inputs.forEach(input => {
            html += `<div class="form-group">
                <label for="${input.id}" data-required="*">${input.label}</label>
                <input type="number" id="${input.id}" name="${input.id}" step="0.01" min="0" value="0" placeholder="请输入数值" required>
                ${input.description ? `<small>${input.description}</small>` : ''}
            </div>`;
        });
        processEmissionContainer.innerHTML = html;
        document.querySelector('.process-card')?.classList.add('product-selected');
    });

    // ---------- 选项卡切换--------
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.dataset.tab;
            tabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            tabPanels.forEach(panel => {
                panel.classList.toggle('active', panel.id === `${tabId}Panel`);
            });
        });
    });

    // ---------- Scope1 计算（燃料 + 过程）--------
    scope1Form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!this.checkValidity()) {
            showNotification('请填写所有必填字段！', 'error');
            return;
        }

        const industry = cfIndustryType.value;
        const product = productType.value;
        if (!industry || !product) {
            showNotification('请先选择行业和产品', 'error');
            return;
        }

        // 1. 燃料燃烧排放计算（煤炭、燃油、燃气）
        let fuelTotal = 0;
        // 煤炭
        for (let i = 1; i <= 7; i++) {
            const val = parseFloat(document.getElementById(`coal${i}`)?.value) || 0;
            fuelTotal += val * FUEL_FACTORS.coal[i-1];
        }
        // 燃油
        for (let i = 1; i <= 5; i++) {
            const val = parseFloat(document.getElementById(`oil${i}`)?.value) || 0;
            fuelTotal += val * FUEL_FACTORS.oil[i-1];
        }
        // 燃气
        for (let i = 1; i <= 7; i++) {
            const val = parseFloat(document.getElementById(`gas${i}`)?.value) || 0;
            fuelTotal += val * FUEL_FACTORS.gas[i-1];
        }

        // 2. 过程排放计算
        let processTotal = 0;
        const config = processEmissionMap[industry]?.[product];
        if (config) {
            config.inputs.forEach(input => {
                const val = parseFloat(document.getElementById(input.id)?.value) || 0;
                processTotal += val * (config.factors[input.id] || 0);
            });
        }

        // 更新结果存储与UI
        fuelEmissionVal = fuelTotal;
        processEmissionVal = processTotal;
        scope1ResultVal = fuelTotal + processTotal;

        document.getElementById('fuelResult').textContent = `${fuelTotal.toFixed(2)} 吨CO₂`;
        document.getElementById('processResult').textContent = `${processTotal.toFixed(2)} 吨CO₂`;
        document.getElementById('scope1TotalResult').textContent = `${scope1ResultVal.toFixed(2)} 吨CO₂`;
        document.getElementById('scope1Result').textContent = `${scope1ResultVal.toFixed(2)} 吨CO₂`;

        // ===== 保存结果到 localStorage =====
        updateCarbonFootprintStorage();

        showNotification(`Scope 1 计算完成！总排放: ${scope1ResultVal.toFixed(2)} 吨CO₂`, 'success');
    });

    // ---------- Scope2 计算--------
    scope2Form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!this.checkValidity()) {
            showNotification('请填写所有必填字段！', 'error');
            return;
        }

        const electricity = parseFloat(document.getElementById('electricity').value) || 0;
        const cf = parseFloat(carbonFactor.value) || 0;
        scope2ResultVal = electricity * cf;

        document.getElementById('electricityValue').textContent = `${electricity.toFixed(2)} 万千瓦时`;
        document.getElementById('carbonFactorValue').textContent = `${cf.toFixed(3)} 吨CO₂/万千瓦时`;
        document.getElementById('scope2TotalResult').textContent = `${scope2ResultVal.toFixed(2)} 吨CO₂`;
        document.getElementById('scope2Result').textContent = `${scope2ResultVal.toFixed(2)} 吨CO₂`;

        // ===== 保存结果到 localStorage =====
        updateCarbonFootprintStorage();

        showNotification(`Scope 2 计算完成！总排放: ${scope2ResultVal.toFixed(2)} 吨CO₂`, 'success');
    });

    // ---------- 获取电碳因子（预留月份日期）--------
    getCarbonFactorBtn.addEventListener('click', function() {
        if (!cfRegion.value) {
            showNotification('请先选择所属地区！', 'error');
            return;
        }
        // 此处可扩展根据月份、日期动态获取，目前使用固定地区因子
        const factor = REGION_FACTORS[cfRegion.value] || 0.8;
        carbonFactor.value = factor.toFixed(3);
        showNotification('电碳因子获取成功！', 'success');
    });

    // ---------- 计算总碳足迹--------
    calcTotalBtn.addEventListener('click', function() {
        if (scope1ResultVal === 0 && scope2ResultVal === 0) {
            showNotification('请先计算Scope 1和Scope 2！', 'error');
            return;
        }
        const total = scope1ResultVal + scope2ResultVal;
        document.getElementById('totalResult').textContent = `${total.toFixed(2)} 吨CO₂`;
        showNotification('总碳足迹计算完成！', 'success');
    });

    // ---------- 重置Scope1（燃料 + 过程）--------
    resetScope1Btn.addEventListener('click', function() {
        // 重置煤炭
        for (let i = 1; i <= 7; i++) {
            const el = document.getElementById(`coal${i}`);
            if (el) el.value = '';
        }
        // 重置燃油
        for (let i = 1; i <= 5; i++) {
            const el = document.getElementById(`oil${i}`);
            if (el) el.value = '';
        }
        // 重置燃气
        for (let i = 1; i <= 7; i++) {
            const el = document.getElementById(`gas${i}`);
            if (el) el.value = '';
        }
        // 重置过程排放输入
        document.querySelectorAll('#processEmissionContainer input[type="number"]').forEach(input => {
            input.value = '0';
        });
        
        // 重置结果
        scope1ResultVal = fuelEmissionVal = processEmissionVal = 0;
        document.getElementById('fuelResult').textContent = '-- 吨CO₂';
        document.getElementById('processResult').textContent = '-- 吨CO₂';
        document.getElementById('scope1TotalResult').textContent = '-- 吨CO₂';
        document.getElementById('scope1Result').textContent = '-- 吨CO₂';

        // ===== 清除 Scope1 相关存储并更新完整对象 =====
        localStorage.removeItem('scope1Result');
        updateCarbonFootprintStorage();

        showNotification('Scope 1 数据已重置', 'success');
    });

    // ---------- 重置Scope2--------
    resetScope2Btn.addEventListener('click', function() {
        document.getElementById('electricity').value = '';
        carbonFactor.value = '';
        document.getElementById('electricityMonth').value = '';
        document.getElementById('electricityDay').value = '';
        
        scope2ResultVal = 0;
        document.getElementById('electricityValue').textContent = '-- 万千瓦时';
        document.getElementById('carbonFactorValue').textContent = '-- 吨CO₂/万千瓦时';
        document.getElementById('scope2TotalResult').textContent = '-- 吨CO₂';
        document.getElementById('scope2Result').textContent = '-- 吨CO₂';

        // ===== 清除 Scope2 相关存储并更新完整对象 =====
        localStorage.removeItem('scope2Result');
        updateCarbonFootprintStorage();

        showNotification('Scope 2 数据已重置', 'success');
    });

    // ---------- 重置所有--------
    resetAllBtn.addEventListener('click', function() {
        if (!confirm('确定要重置所有数据吗？所有输入和计算结果将被清除。')) return;
        
        // 触发各个重置按钮的逻辑
        resetScope1Btn.click();
        resetScope2Btn.click();
        
        // 额外重置基础信息与总碳足迹
        document.getElementById('totalResult').textContent = '-- 吨CO₂';

        // ===== 清除所有碳足迹存储（独立键+完整对象）=====
        localStorage.removeItem('scope1Result');
        localStorage.removeItem('scope2Result');
        localStorage.removeItem('carbon-footprint-results');

        showNotification('所有数据已重置', 'success');
    });

    // ---------- 辅助函数：更新产品下拉--------
    function updateProductOptions(industryVal) {
        productType.innerHTML = '';
        if (!industryVal) {
            productType.innerHTML = '<option value="">请先选择行业</option>';
            return;
        }
        const products = industryProductMap[industryVal] || [];
        if (products.length) {
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '请选择产品';
            productType.appendChild(defaultOption);
            products.forEach(p => {
                const option = document.createElement('option');
                option.value = p.value;
                option.textContent = p.text;
                productType.appendChild(option);
            });
        } else {
            productType.innerHTML = '<option value="">暂无对应产品</option>';
        }
    }

    // ---------- 通知提示--------
    function showNotification(message, type) {
        const existing = document.querySelector('.notification');
        if (existing) existing.remove();
        const notif = document.createElement('div');
        notif.className = `notification ${type === 'success' ? '' : 'error'}`;
        notif.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i><span>${message}</span>`;
        document.body.appendChild(notif);
        setTimeout(() => {
            notif.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notif.remove(), 300);
        }, 3000);
    }
    
    // 自动测试：如果URL中有测试参数，自动选择钢铁和螺纹钢
    if (window.location.href.includes('test=1')) {
        console.log('=== 运行自动测试 ===');
        setTimeout(() => {
            cfIndustryType.value = 'steel';
            cfIndustryType.dispatchEvent(new Event('change'));
            setTimeout(() => {
                productType.value = 'rebar';
                productType.dispatchEvent(new Event('change'));
                console.log('自动测试完成：已选择钢铁行业和螺纹钢产品');
            }, 500);
        }, 1000);
    }
    
    console.log('=== 碳足迹页面加载完成 (新版) ===');
});