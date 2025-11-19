const productGrid = document.getElementById('product-grid');
const statusEl = document.getElementById('status');
const searchInput = document.getElementById('search');
const sortSelect = document.getElementById('sort');

let products = [];
let filtered = [];

// Theme Toggle
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    const slider = document.querySelector('.theme-toggle-slider');
    slider.textContent = newTheme === 'dark' ? '🌙' : '☀️';
}

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
if (savedTheme === 'dark') {
    document.querySelector('.theme-toggle-slider').textContent = '🌙';
}

function debounce(fn, wait = 300) {
    let t;
    return (...args) => {
        clearTimeout(t);
        t = setTimeout(() => fn(...args), wait);
    };
}


function setStatus(text) {
    statusEl.textContent = text;
}

function renderProducts(list) {
    productGrid.innerHTML = '';

    if (!list.length) {
        productGrid.innerHTML = `
          <div class="empty-state" style="grid-column: 1/-1;">
            <div class="empty-state-icon">📦</div>
            <h2>No products found</h2>
            <p>Try adjusting your search or filters</p>
          </div>
        `;
        return;
    }

    list.forEach((p, idx) => {
        const card = document.createElement('article');
        card.className = 'card';
        card.style.animationDelay = `${idx * 0.05}s`;
        card.innerHTML = `
          <div class="card-image">
            <img src="${p.thumbnail || p.images?.[0] || ''}" alt="${escapeHtml(p.title)}" loading="lazy">
          </div>
          <div class="card-content">
            <h3>${escapeHtml(p.title)}</h3>
            <div class="card-meta">
              ${p.brand ? `<span class="badge">${escapeHtml(p.brand)}</span>` : ''}
              ${p.category ? `<span class="badge">${escapeHtml(p.category)}</span>` : ''}
            </div>
            <div class="price">₹${formatPrice(p.price)}</div>
          </div>
        `;
        productGrid.appendChild(card);
    });
}

function escapeHtml(s = '') {
    return String(s).replace(/[&<>"']/g, (m) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }[m]));
}

function formatPrice(n) {
    return Number(n).toFixed(2);
}

async function fetchProducts() {
    try {
        setStatus('Loading...');
        productGrid.innerHTML = '<div class="spinner" style="grid-column: 1/-1;"></div>';

        const res = await fetch('https://dummyjson.com/products');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();
        products = data.products || [];
        filtered = products.slice();

        setStatus(`${products.length} products`);
        renderProducts(filtered);
    } catch (err) {
        console.error(err);
        setStatus('Failed to load');
        productGrid.innerHTML = `
          <div class="empty-state" style="grid-column: 1/-1;">
            <div class="empty-state-icon">⚠️</div>
            <h2>Unable to load products</h2>
            <p>Please try again later</p>
          </div>
        `;
    }
}

function applyFilters() {
    const q = searchInput.value.trim().toLowerCase();

    filtered = products.filter(p => {
        if (!q) return true;
        const hay = `${p.title} ${p.brand} ${p.category}`.toLowerCase();
        return hay.includes(q);
    });

    const s = sortSelect.value;
    if (s === 'price-desc') {
        filtered.sort((a, b) => b.price - a.price);
    } else if (s === 'price-asc') {
        filtered.sort((a, b) => a.price - b.price);
    } else if (s === 'name-asc') {
        filtered.sort((a, b) => a.title.localeCompare(b.title));
    }

    renderProducts(filtered);
    setStatus(`${filtered.length} products`);
}

searchInput.addEventListener('input', debounce(applyFilters, 250));
sortSelect.addEventListener('change', applyFilters);

fetchProducts();