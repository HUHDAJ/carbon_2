document.addEventListener('DOMContentLoaded', function() {
    // 加载聊天历史
    loadChatHistory();
    
    // 设置消息框自适应高度
    setupChatInput();
});

// 设置聊天输入框自适应高度
function setupChatInput() {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
}

// 发送消息
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // 添加用户消息
    addMessage(message, 'user');
    
    // 清空输入框并重置高度
    input.value = '';
    input.style.height = 'auto';
    
    // 显示思考状态
    showThinking();
    
    // 模拟AI响应延迟
    setTimeout(() => {
        // 获取AI响应
        const response = getAIResponse(message);
        
        // 移除思考状态
        hideThinking();
        
        // 添加AI响应
        addMessage(response, 'agent');
        
        // 保存到聊天历史
        saveChatHistory();
        
        // 自动滚动到底部
        scrollToBottom();
    }, 1500);
}

// 处理键盘事件
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 快速问题
function quickQuestion(question) {
    const input = document.getElementById('chat-input');
    input.value = question;
    sendMessage();
}

// 添加消息到聊天界面
function addMessage(text, sender) {
    const messagesDiv = document.getElementById('chat-messages');
    const time = getCurrentTime();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    // 格式化消息内容
    const formattedText = formatMessage(text);
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-${sender === 'user' ? 'user' : 'robot'}"></i>
        </div>
        <div class="message-content">
            <div class="message-text">${formattedText}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}

// 获取当前时间
function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// 格式化消息文本
function formatMessage(text) {
    // 替换换行符
    let formatted = text.replace(/\n/g, '<br>');
    
    // 替换标题
    formatted = formatted.replace(/^### (.*?)$/gm, '<strong>$1</strong>');
    
    // 替换列表项
    formatted = formatted.replace(/^(\d+)\.\s+(.*?)$/gm, '$1. $2<br>');
    formatted = formatted.replace(/^-\s+(.*?)$/gm, '• $1<br>');
    
    // 替换加粗文本
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // 替换代码
    formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
    
    return formatted;
}

// 显示思考状态
function showThinking() {
    const messagesDiv = document.getElementById('chat-messages');
    
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'message agent thinking';
    thinkingDiv.id = 'thinking-message';
    thinkingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-text">
                <span class="thinking-text">正在思考...</span>
            </div>
        </div>
    `;
    
    messagesDiv.appendChild(thinkingDiv);
    scrollToBottom();
}

// 隐藏思考状态
function hideThinking() {
    const thinkingDiv = document.getElementById('thinking-message');
    if (thinkingDiv) {
        thinkingDiv.remove();
    }
}

// 滚动到底部
function scrollToBottom() {
    const messagesDiv = document.getElementById('chat-messages');
    if (messagesDiv) {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
}

// 获取AI响应（模拟）
function getAIResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // 关键词匹配响应
    if (lowerMessage.includes('scope 1') || lowerMessage.includes('直接排放')) {
        return `### Scope 1排放计算指南
        
Scope 1排放是指企业拥有或控制的排放源产生的直接温室气体排放，主要包括：

**1. 燃料燃烧排放**
   - 锅炉、窑炉、车辆等使用的化石燃料
   - 计算公式：燃料消耗量 × 燃料排放因子

**2. 工艺过程排放**
   - 水泥生产中的熟料生产过程
   - 钢铁冶炼中的还原反应
   - 计算公式：原料消耗量 × 工艺排放因子

**3. 逸散排放**
   - 设备泄漏（如阀门、管道）
   - 制冷剂逸散
   - 煤炭开采和运输中的逸散

**关键数据需求：**
- 各类燃料的消耗量（吨、立方米等）
- 工艺原料的使用量
- 相关设备的运行参数

您需要我帮您计算具体的Scope 1排放量吗？可以提供相关数据。`;
        
    } else if (lowerMessage.includes('cbam') || lowerMessage.includes('碳边境')) {
        return `### CBAM（碳边境调节机制）详解
        
**实施时间表：**
- 过渡期：2023年10月1日 - 2025年12月31日
- 正式实施：2026年1月1日开始

**覆盖产品范围：**
1. 钢铁及相关制品
2. 水泥
3. 铝
4. 化肥（硝酸、氨、尿素等）
5. 电力
6. 氢气

**计算公式：**
CBAM税负 = (产品隐含碳排放量 × 欧盟碳配额价格) - 已支付的碳成本

**具体计算步骤：**
1. 计算产品的隐含碳排放量
2. 获取当季度欧盟碳配额均价
3. 计算需购买的CBAM证书数量
4. 减去在原产国已支付的碳成本

**报告要求：**
- 每季度提交一次CBAM报告
- 每年5月31日前提交年度报告
- 需要第三方机构验证

您想了解特定产品的CBAM税负计算示例吗？`;
        
    } else if (lowerMessage.includes('减排') || lowerMessage.includes('节能') || lowerMessage.includes('措施')) {
        return `### 企业减排措施建议
        
根据您的企业类型，推荐以下减排措施：

**一、能效提升措施**
1. **设备更新**
   - 更换高效电机和泵
   - 安装变频器控制设备
   - 采用高效照明系统

2. **工艺优化**
   - 优化生产流程，减少能源浪费
   - 实施热能回收系统
   - 采用先进控制系统

3. **能源管理**
   - 建立能源管理体系
   - 实施能源监测系统
   - 开展能源审计

**二、清洁能源利用**
1. **可再生能源**
   - 安装光伏发电系统
   - 采购绿色电力
   - 利用生物质能源

2. **燃料替代**
   - 用天然气替代煤炭
   - 使用生物燃料
   - 探索氢能应用

**三、碳减排技术**
1. **碳捕集利用与封存**
   - 实施CCUS项目
   - 利用捕集的二氧化碳
   - 开展碳汇项目

2. **循环经济**
   - 提高资源利用率
   - 实施废物资源化
   - 开发再生材料

您想了解哪类减排措施的详细实施方案？`;
        
    } else if (lowerMessage.includes('光伏') || lowerMessage.includes('太阳能') || lowerMessage.includes('投资')) {
        return `### 光伏投资项目分析框架
        
**一、投资成本估算**
1. **系统容量规划**
   - 屋顶面积：___ 平方米
   - 装机容量：___ kWp
   - 预计投资：4-6元/瓦

2. **成本构成**
   - 光伏组件：约占总投资的45%
   - 逆变器：约占总投资的15%
   - 支架和安装：约占总投资的15%
   - 其他（电缆、监控等）：约占总投资的25%

**二、收益分析**
1. **发电量估算**
   - 年等效利用小时数：___ 小时（受地区影响）
   - 年发电量：装机容量 × 利用小时数

2. **经济效益**
   - 自发自用电价：___ 元/度（工商业电价）
   - 余电上网电价：___ 元/度
   - 年度电费节省：发电量 × 电价

3. **环境效益**
   - 每度电减排：约0.7 kg CO₂
   - 年度减排量：___ 吨CO₂

**三、投资回收期**
- 简单回收期：总投资 ÷ 年度收益
- 考虑补贴和税收优惠：通常5-8年

**四、政策支持**
1. **国家政策**
   - 可再生能源补贴
   - 税收优惠政策
   - 绿色电力证书

2. **地方政策**
   - 地方补贴政策
   - 电价优惠政策
   - 土地和审批支持

您想进行具体的光伏投资回报分析吗？请提供详细参数。`;
        
    } else if (lowerMessage.includes('计算') || lowerMessage.includes('怎么算') || lowerMessage.includes('核算')) {
        return `### 碳排放核算方法指南
        
**一、核算边界确定**
1. **组织边界**
   - 股权比例法
   - 财务控制法
   - 运营控制法

2. **运营边界**
   - Scope 1：直接排放
   - Scope 2：间接排放（外购能源）
   - Scope 3：其他间接排放

**二、数据收集**
1. **活动数据**
   - 燃料消耗量（吨、立方米）
   - 电力消耗量（kWh）
   - 原材料使用量
   - 产品产量

2. **排放因子**
   - IPCC排放因子数据库
   - 国家温室气体排放因子
   - 行业特定排放因子
   - 供应商提供的数据

**三、计算方法**
1. **基本公式**
   排放量 = 活动数据 × 排放因子

2. **具体计算**
   - 燃料燃烧：燃料消耗量 × 燃料热值 × 排放因子
   - 电力消耗：用电量 × 电碳因子
   - 工艺过程：原料消耗量 × 工艺排放因子

**四、报告要求**
1. **报告内容**
   - 排放总量
   - 分范围排放量
   - 主要排放源分析
   - 减排措施和成效

2. **质量保证**
   - 数据准确性验证
   - 计算方法说明
   - 不确定性分析

您需要针对特定排放源的计算指导吗？`;
        
    } else {
        // 默认响应
        const defaultResponses = [
            "感谢您的提问！让我为您详细解答这个问题...",
            "这是一个很好的问题。根据我的专业知识，相关信息如下：",
            "我理解您的关注点。让我为您分析这个情况。",
            "您的问题很有价值。让我为您提供相关信息和建议。"
        ];
        
        const randomResponse = defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
        
        return `${randomResponse}

### 我可以为您提供以下帮助：

**1. 碳排放管理**
   - Scope 1/2/3排放计算
   - 碳足迹分析
   - 减排目标设定

**2. CBAM应对**
   - CBAM税负计算
   - 申报材料准备
   - 合规策略制定

**3. 减排方案**
   - 技术可行性分析
   - 经济性评估
   - 实施路径规划

**4. 投资决策**
   - 绿色项目投资分析
   - 回报期计算
   - 风险评估

请告诉我您具体想了解哪个方面？`;
    }
}

// 打开工具
function openTool(toolName) {
    const toolNames = {
        'report-generator': '报告生成器',
        'comparison-tool': '对比分析工具',
        'investment-calculator': '投资计算器',
        'scenario-simulator': '情景模拟器'
    };
    
    const name = toolNames[toolName] || toolName;
    showNotification(`${name}功能开发中，敬请期待！`, 'info');
}

// 清空聊天
function clearChat() {
    const messagesDiv = document.getElementById('chat-messages');
    
    if (messagesDiv.children.length <= 1 || confirm('确定要清空对话记录吗？')) {
        // 保留第一条欢迎消息
        const welcomeMessage = messagesDiv.querySelector('.message.agent:first-child');
        messagesDiv.innerHTML = '';
        if (welcomeMessage) {
            messagesDiv.appendChild(welcomeMessage.cloneNode(true));
        }
        
        // 清除本地存储
        localStorage.removeItem('agent-chat-history');
        showNotification('对话已清空', 'success');
    }
}

// 导出聊天
function exportChat() {
    const messages = document.querySelectorAll('.message');
    if (messages.length <= 1) {
        showNotification('没有可导出的对话内容', 'info');
        return;
    }
    
    let chatText = '碳足迹智能助手 - 对话记录\n';
    chatText += '导出时间：' + new Date().toLocaleString() + '\n';
    chatText += '='.repeat(50) + '\n\n';
    
    messages.forEach((msg, index) => {
        const isAgent = msg.classList.contains('agent');
        const text = msg.querySelector('.message-text').textContent;
        const time = msg.querySelector('.message-time')?.textContent || '';
        
        if (index > 0) { // 跳过第一条欢迎消息
            chatText += `${isAgent ? '【智能助手】' : '【用户】'} ${time}\n`;
            chatText += text + '\n';
            chatText += '-'.repeat(40) + '\n\n';
        }
    });
    
    // 创建并下载文件
    const blob = new Blob([chatText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `碳足迹对话记录_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('对话记录已导出', 'success');
}

// 保存聊天历史
function saveChatHistory() {
    const messagesDiv = document.getElementById('chat-messages');
    const messages = [];
    
    // 跳过第一条欢迎消息
    const messageElements = Array.from(messagesDiv.querySelectorAll('.message')).slice(1);
    
    messageElements.forEach(msg => {
        // 跳过思考消息
        if (msg.querySelector('.thinking-text')) return;
        
        const isAgent = msg.classList.contains('agent');
        const text = msg.querySelector('.message-text').textContent;
        const time = msg.querySelector('.message-time')?.textContent || '';
        
        messages.push({
            sender: isAgent ? 'agent' : 'user',
            text: text,
            time: time
        });
    });
    
    if (messages.length > 0) {
        localStorage.setItem('agent-chat-history', JSON.stringify(messages));
    }
}

// 加载聊天历史
function loadChatHistory() {
    const savedChat = localStorage.getItem('agent-chat-history');
    if (savedChat) {
        try {
            const messages = JSON.parse(savedChat);
            const messagesDiv = document.getElementById('chat-messages');
            
            // 清空现有消息（保留欢迎消息）
            const welcomeMessage = messagesDiv.querySelector('.message.agent:first-child');
            messagesDiv.innerHTML = '';
            if (welcomeMessage) {
                messagesDiv.appendChild(welcomeMessage.cloneNode(true));
            }
            
            // 添加历史消息
            messages.forEach(msg => {
                addMessage(msg.text, msg.sender);
            });
            
            // 滚动到底部
            setTimeout(() => {
                scrollToBottom();
            }, 100);
            
        } catch (error) {
            console.error('加载聊天历史失败:', error);
            localStorage.removeItem('agent-chat-history');
        }
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    // 移除现有的通知
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification ${type === 'success' ? '' : 'error'}`;
    notification.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
        <span style="font-size: 14px;">${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // 3秒后自动移除
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}