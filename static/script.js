document.addEventListener('DOMContentLoaded', function() {
    const envForm = document.getElementById('env-form');
    const envSections = document.getElementById('env-sections');

    // 显示加载动画
    showLoading();

    // 图标映射
    const sectionIcons = {
        'Web管理': 'fa-cog',
        '123云盘': 'fa-cloud',
        '115云盘': 'fa-database',
        '天翼云盘': 'fa-server',
        'Telegram': 'fa-paper-plane',
        '监控': 'fa-eye',
        'AI检测': 'fa-robot',
        '其他': 'fa-sliders-h'
    };

    // 从服务器获取.env配置数据
    fetch('/api/env')
        .then(response => response.json())
        .then(data => {
            // 动态生成表单
            const sections = data.sections;
            const order = data.order;

            order.forEach(section => {
                const sectionDiv = document.createElement('div');
                sectionDiv.className = 'section fade-in';

                const sectionTitle = document.createElement('h2');
                const icon = sectionIcons[section] || 'fa-folder';
                sectionTitle.innerHTML = `<i class="fas ${icon}"></i> ${section}`;
                sectionDiv.appendChild(sectionTitle);

                sections[section].forEach((item, index) => {
                    const configItem = document.createElement('div');
                    configItem.className = 'config-item';

                    const label = document.createElement('label');
                    label.textContent = item.key;
                    label.setAttribute('for', `${section}-${index}`);
                    configItem.appendChild(label);

                    if (item.comment) {
                        const comment = document.createElement('div');
                        comment.className = 'comment' + (item.comment.includes('必填') ? ' required-comment' : '');
                        comment.textContent = item.comment;
                        configItem.appendChild(comment);
                    }

                    const input = document.createElement('input');
                    input.type = item.key.toLowerCase().includes('password') ? 'password' : 'text';
                    input.id = `${section}-${index}`;
                    input.name = `${section}[${index}]`;
                    input.value = item.value || '';
                    input.dataset.key = item.key;
                    input.dataset.comment = item.comment || '';
                    input.placeholder = `请输入 ${item.key}`;
                    input.className = 'form-control';
                    configItem.appendChild(input);

                    sectionDiv.appendChild(configItem);
                });

                envSections.appendChild(sectionDiv);
            });

            hideLoading();
        })
        .catch(error => {
            console.error('Error fetching env data:', error);
            hideLoading();
            showNotification('加载配置数据失败，请刷新页面重试', 'error');
            envSections.innerHTML = '<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i>加载配置数据失败，请刷新页面重试</div>';
        });

    // 提交表单
    envForm.addEventListener('submit', function(e) {
        e.preventDefault();

        showLoading();

        const formData = {};
        const sections = document.querySelectorAll('.section');

        sections.forEach(section => {
            const sectionTitle = section.querySelector('h2').textContent.replace(/^\s*<i[^>]*>.*?<\/i>\s*/, '').trim();
            formData[sectionTitle] = [];

            const inputs = section.querySelectorAll('input');
            inputs.forEach(input => {
                formData[sectionTitle].push({
                    comment: input.dataset.comment,
                    key: input.dataset.key,
                    value: input.value
                });
            });
        });

        // 发送数据到服务器
        fetch('/api/env', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.success) {
                showNotification('配置保存成功！容器将自动重启应用新配置', 'success');
            } else {
                showNotification('保存失败，请检查配置后重试', 'error');
            }
        })
        .catch(error => {
            console.error('Error saving env data:', error);
            hideLoading();
            showNotification('配置已保存，容器正在重启...', 'success');
        });
    });
});

// 工具函数
function showLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.add('show');
    }
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.classList.remove('show');
    }
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    if (notification) {
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            ${message}
        `;
        
        setTimeout(() => {
            notification.classList.remove('success', 'error');
        }, 5000);
    }
}