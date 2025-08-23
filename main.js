// 主页面JavaScript - 显示最新梦境
document.addEventListener('DOMContentLoaded', function() {
    const loadingElement = document.getElementById('loading');
    const dreamContainer = document.getElementById('dream-container');
    const errorMessage = document.getElementById('error-message');
    
    // 显示加载状态
    showElement(loadingElement);
    hideElement(dreamContainer);
    hideElement(errorMessage);

    // 获取URL参数中的日期
    const urlParams = new URLSearchParams(window.location.search);
    const targetDate = urlParams.get('date');

    // 加载梦境数据，添加时间戳和缓存控制头以防止缓存
    fetch(`./data/dreams.json?t=${new Date().getTime()}`, {
        headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不正常');
            }
            return response.json();
        })
        .then(dreams => {
            if (dreams && dreams.length > 0) {
                if (targetDate) {
                    // 查找特定日期的梦境
                    const targetDream = dreams.find(dream => dream.date === targetDate);
                    if (targetDream) {
                        displayLatestDream(targetDream);
                    } else {
                        showError(`找不到 ${targetDate} 的梦境记录`);
                    }
                } else {
                    // 显示最新梦境
                    displayLatestDream(dreams[0]);
                }
            } else {
                showError('暂无梦境数据');
            }
        })
        .catch(error => {
            console.error('加载梦境数据失败:', error);
            showError('无法加载梦境数据');
        });
});

function displayLatestDream(dream) {
    // 更新页面内容
    document.getElementById('dream-date').textContent = `梦境记录 - ${formatDate(dream.date)}`;
    document.getElementById('dream-img').src = dream.image_path;
    document.getElementById('dream-img').alt = `${dream.date}的梦境图像`;
    document.getElementById('dream-text').textContent = dream.text;
    document.getElementById('seeds-list').textContent = dream.seeds.join(', ');
    document.getElementById('generation-time').textContent = formatDate(dream.date);

    // 更新页面标题
    document.title = `AI梦境档案馆 - ${formatDate(dream.date)}`;

    // 显示种子标签
    const seedsContainer = document.getElementById('dream-seeds');
    seedsContainer.innerHTML = '';
    dream.seeds.forEach(seed => {
        const seedTag = document.createElement('span');
        seedTag.className = 'seed-tag';
        seedTag.textContent = seed;
        seedsContainer.appendChild(seedTag);
    });

    // 显示内容，隐藏加载状态
    hideElement(document.getElementById('loading'));
    showElement(document.getElementById('dream-container'));
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showElement(element) {
    element.classList.remove('hidden');
}

function hideElement(element) {
    element.classList.add('hidden');
}

function showError(message) {
    const errorElement = document.getElementById('error-message');
    if (errorElement) {
        errorElement.querySelector('p').textContent = message;
        hideElement(document.getElementById('loading'));
        showElement(errorElement);
    }
}

// 图片加载错误处理
document.getElementById('dream-img').addEventListener('error', function() {
    this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMzMzIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iI2ZmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPua1i+ivleWbvueJhzwvdGV4dD48L3N2Zz4=';
    this.alt = '图片加载失败';
});
