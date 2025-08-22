// 档案馆页面JavaScript - 显示所有梦境记录
document.addEventListener('DOMContentLoaded', function() {
    const loadingElement = document.getElementById('loading');
    const galleryContainer = document.getElementById('gallery-container');
    const errorMessage = document.getElementById('error-message');
    const emptyMessage = document.getElementById('empty-message');
    
    // 显示加载状态
    showElement(loadingElement);
    hideElement(galleryContainer);
    hideElement(errorMessage);
    hideElement(emptyMessage);

    // 加载梦境数据
    fetch('./data/dreams.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不正常');
            }
            return response.json();
        })
        .then(dreams => {
            if (dreams && dreams.length > 0) {
                displayDreamsGallery(dreams);
            } else {
                showEmptyMessage();
            }
        })
        .catch(error => {
            console.error('加载梦境数据失败:', error);
            showError('无法加载梦境档案');
        });
});

function displayDreamsGallery(dreams) {
    const galleryContainer = document.getElementById('gallery-container');
    galleryContainer.innerHTML = '';

    dreams.forEach(dream => {
        const dreamCard = createDreamCard(dream);
        galleryContainer.appendChild(dreamCard);
    });

    // 显示画廊，隐藏加载状态
    hideElement(document.getElementById('loading'));
    showElement(galleryContainer);
}

function createDreamCard(dream) {
    const card = document.createElement('div');
    card.className = 'dream-card';
    
    card.innerHTML = `
        <div class="card-image">
            <img src="${dream.image_path}" alt="${dream.date}的梦境图像" loading="lazy">
            <div class="card-overlay">
                <span class="card-date">${formatDate(dream.date)}</span>
            </div>
        </div>
        <div class="card-content">
            <h3>${formatDate(dream.date)}</h3>
            <div class="card-seeds">
                ${dream.seeds.map(seed => `<span class="seed-tag">${seed}</span>`).join('')}
            </div>
            <p class="card-preview">${dream.text.substring(0, 100)}...</p>
            <button class="view-details" onclick="viewDreamDetails('${dream.date}')">查看详情</button>
        </div>
    `;

    // 图片加载错误处理
    const img = card.querySelector('img');
    img.addEventListener('error', function() {
        this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMzMzIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iI2ZmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPua1i+ivleWbvueJhzwvdGV4dD48L3N2Zz4=';
        this.alt = '图片加载失败';
    });

    return card;
}

function viewDreamDetails(date) {
    // 这里可以跳转到详情页面或显示模态框
    // 暂时简单跳转到主页，因为主页显示最新梦境
    window.location.href = 'index.html';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
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

function showEmptyMessage() {
    hideElement(document.getElementById('loading'));
    showElement(document.getElementById('empty-message'));
}

// 搜索功能（可选扩展）
function setupSearch() {
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = '搜索梦境...';
    searchInput.className = 'search-input';
    
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.dream-card');
        
        cards.forEach(card => {
            const text = card.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // 将搜索框添加到页面
    const header = document.querySelector('.archive-header');
    if (header) {
        header.appendChild(searchInput);
    }
}

// 初始化搜索功能（如果需要）
// setupSearch();
