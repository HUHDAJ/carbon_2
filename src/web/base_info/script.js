document.addEventListener('DOMContentLoaded', function() {
    const baseInfoForm = document.getElementById('baseInfoForm');
    const infoTableBody = document.getElementById('infoTableBody');
    const noDataRow = document.getElementById('noDataRow');

    // 加载已有信息
    loadBaseInfo();

    // 提交表单
    baseInfoForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 表单验证
        if (!baseInfoForm.checkValidity()) {
            showNotification('请填写所有必填字段！', 'error');
            return;
        }
        
        const formData = new FormData(baseInfoForm);
        const info = {
            enterpriseName: formData.get('enterpriseName'),
            industryType: formData.get('industryType'),
            region: formData.get('region')
        };

        // 保存到本地存储（模拟API调用）
        saveToLocalStorage(info);
        
        // 显示成功消息
        showNotification('企业基础信息保存成功！', 'success');
        
        // 重置表单
        baseInfoForm.reset();
        
        // 重新加载列表
        loadBaseInfo();
    });

    // 从本地存储加载数据（模拟API调用）
    function loadBaseInfo() {
        // 模拟API调用延迟
        setTimeout(() => {
            const savedData = getFromLocalStorage();
            
            infoTableBody.innerHTML = '';
            
            if (savedData && savedData.length > 0) {
                // 隐藏"暂无数据"行
                if (noDataRow) noDataRow.style.display = 'none';
                
                savedData.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${item.enterpriseName}</td>
                        <td>${getIndustryName(item.industryType)}</td>
                        <td>${getRegionName(item.region)}</td>
                        <td>
                            <button class="action-btn set-current-btn" data-id="${item.id}" title="设为当前计算企业">
                                <i class="fas fa-check-circle"></i> 设为当前
                            </button>
                            <button class="action-btn edit-btn" data-id="${item.id}">
                                <i class="fas fa-edit"></i> 编辑
                            </button>
                            <button class="action-btn delete-btn" data-id="${item.id}">
                                <i class="fas fa-trash"></i> 删除
                            </button>
                        </td>
                    `;
                    infoTableBody.appendChild(tr);
                });
                
                // 绑定事件
                bindTableEvents();
            } else {
                // 显示"暂无数据"行
                if (noDataRow) noDataRow.style.display = '';
                infoTableBody.appendChild(noDataRow);
            }
        }, 300);
    }

    // 绑定表格按钮事件
    function bindTableEvents() {
        // 设为当前按钮
        document.querySelectorAll('.set-current-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const savedData = getFromLocalStorage();
                const item = savedData.find(item => item.id == id);
                
                if (item) {
                    // 保存为当前企业信息
                    localStorage.setItem('current-enterprise-info', JSON.stringify(item));
                    
                    // 高亮显示当前选中的企业
                    document.querySelectorAll('tr').forEach(tr => {
                        tr.classList.remove('current-selected');
                    });
                    this.closest('tr').classList.add('current-selected');
                    
                    showNotification(`已设为当前计算企业: ${item.enterpriseName}`, 'success');
                }
            });
        });

        // 编辑按钮
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const savedData = getFromLocalStorage();
                const item = savedData.find(item => item.id == id);
                
                if (item) {
                    // 填充表单
                    document.getElementById('enterpriseName').value = item.enterpriseName;
                    document.getElementById('industryType').value = item.industryType;
                    document.getElementById('region').value = item.region;
                    
                    // 滚动到表单区域
                    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
                    
                    showNotification('已加载编辑数据，请修改后重新保存', 'success');
                }
            });
        });

        // 删除按钮
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const savedData = getFromLocalStorage();
                const item = savedData.find(item => item.id == id);
                
                if (item && confirm(`确定要删除 "${item.enterpriseName}" 的信息吗？`)) {
                    // 从本地存储删除
                    deleteFromLocalStorage(id);
                    
                    showNotification('企业信息删除成功！', 'success');
                    
                    // 重新加载列表
                    loadBaseInfo();
                }
            });
        });
    }

    // 获取行业类型名称
    function getIndustryName(type) {
        const map = {
            'steel': '钢铁',
            'cement': '水泥',
            'fertilizer': '化肥'
        };
        return map[type] || type;
    }
    
    // 获取地区名称
    function getRegionName(regionCode) {
        // 如果已经是完整名称，直接返回
        if (regionCode.includes('地区')) {
            return regionCode;
        }
        
        const regionMap = {
            '华中': '华中地区',
            '华南': '华南地区',
            '华北': '华北地区',
            '华东': '华东地区',
            '西南': '西南地区',
            '西北': '西北地区'
        };
        
        return regionMap[regionCode] || regionCode;
    }

    // 显示通知函数
    function showNotification(message, type) {
        // 移除现有的通知
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        const notification = document.createElement('div');
        notification.className = `notification ${type === 'success' ? '' : 'error'}`;
        notification.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        // 3秒后移除通知
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }

    // 本地存储辅助函数
    function saveToLocalStorage(info) {
        const savedData = getFromLocalStorage();
        const newItem = {
            id: Date.now().toString(),
            ...info,
            createdAt: new Date().toISOString()
        };
        
        savedData.push(newItem);
        localStorage.setItem('enterprise-base-info', JSON.stringify(savedData));
        // 注意：不再自动设置为当前企业信息
        // localStorage.setItem('current-enterprise-info', JSON.stringify(newItem));
        return newItem;
    }
    
    function getFromLocalStorage() {
        const data = localStorage.getItem('enterprise-base-info');
        return data ? JSON.parse(data) : [];
    }
    
    function deleteFromLocalStorage(id) {
        const savedData = getFromLocalStorage();
        const filteredData = savedData.filter(item => item.id !== id);
        localStorage.setItem('enterprise-base-info', JSON.stringify(filteredData));
        
        // 如果删除的是当前选中的信息，清空
        const currentInfo = JSON.parse(localStorage.getItem('current-enterprise-info') || '{}');
        if (currentInfo.id === id) {
            localStorage.removeItem('current-enterprise-info');
        }
        return true;
    }
});