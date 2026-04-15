/**
 * FinSight – Main JavaScript (shared utilities)
 * API helper, auth token management, navbar logic, theme toggle, toast notifications
 */

// ── Configuration ───────────────────────────────────────────
const API_BASE = window.location.origin + '/api';

// ── Auth Token Management ───────────────────────────────────
const Auth = {
    getToken()  { return localStorage.getItem('finsight_token'); },
    setToken(t) { localStorage.setItem('finsight_token', t); },
    getUser()   { try { return JSON.parse(localStorage.getItem('finsight_user')); } catch { return null; } },
    setUser(u)  { localStorage.setItem('finsight_user', JSON.stringify(u)); },
    isLoggedIn(){ return !!this.getToken(); },
    isAdmin()   { const u = this.getUser(); return u && u.role === 'admin'; },
    logout() {
        localStorage.removeItem('finsight_token');
        localStorage.removeItem('finsight_user');
        window.location.href = '/pages/login.html';
    }
};

// ── API Helper ──────────────────────────────────────────────
async function api(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : API_BASE + endpoint;
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    const token = Auth.getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch(url, { ...options, headers });
        const data = await res.json();
        if (!res.ok) {
            throw { status: res.status, ...data };
        }
        return data;
    } catch (err) {
        if (err.status === 401) {
            Auth.logout();
        }
        throw err;
    }
}

// Shorthand methods
api.get    = (url)       => api(url);
api.post   = (url, body) => api(url, { method: 'POST',   body: JSON.stringify(body) });
api.put    = (url, body) => api(url, { method: 'PUT',    body: JSON.stringify(body) });
api.delete = (url)       => api(url, { method: 'DELETE' });

// ── Toast Notifications ─────────────────────────────────────
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}


// ── Navbar ──────────────────────────────────────────────────
function initNavbar() {
    const authArea = document.getElementById('auth-area');
    if (authArea) {
        if (Auth.isLoggedIn()) {
            const user = Auth.getUser();
            const initials = (user?.name || 'U').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

            authArea.innerHTML = `
                <div class="user-dropdown" id="user-dropdown">
                    <button class="user-dropdown-trigger" id="user-dropdown-trigger" aria-haspopup="true" aria-expanded="false">
                        <span class="user-avatar">${initials}</span>
                        <span class="user-trigger-name">${user?.name || 'User'}</span>
                        <svg class="dropdown-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </button>
                    <div class="user-dropdown-menu" id="user-dropdown-menu">
                        <div class="dropdown-user-info">
                            <span class="user-avatar user-avatar-lg">${initials}</span>
                            <div>
                                <div class="dropdown-user-name">${user?.name || 'User'}</div>
                                <div class="dropdown-user-email">${user?.email || ''}</div>
                            </div>
                        </div>
                        <div class="dropdown-divider"></div>
                        <a href="/pages/dashboard.html" class="dropdown-item">
                            <span class="dropdown-item-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width: 1em; height: 1em; vertical-align: middle;"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg></span> My Dashboard
                        </a>
                        <a href="/pages/dashboard.html#watchlists" class="dropdown-item">
                            <span class="dropdown-item-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width: 1em; height: 1em; vertical-align: middle;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></span> My Watchlists
                        </a>
                        <a href="/pages/profile.html" class="dropdown-item">
                            <span class="dropdown-item-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></span> Profile & Settings
                        </a>

                        ${Auth.isAdmin() ? `
                        <div class="dropdown-divider"></div>
                        <a href="/pages/admin.html" class="dropdown-item">
                            <span class="dropdown-item-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg></span> Admin Panel
                        </a>` : ''}
                        <div class="dropdown-divider"></div>
                        <button class="dropdown-item dropdown-item-danger" onclick="Auth.logout()">
                            <span class="dropdown-item-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg></span> Logout
                        </button>
                    </div>
                </div>
            `;

            // Remove Dashboard from navbar
            document.querySelectorAll('.nav-link').forEach(link => {
                if (link.getAttribute('href') === '/pages/dashboard.html') {
                    link.style.display = 'none';
                }
            });

            // Dropdown toggle
            const trigger = document.getElementById('user-dropdown-trigger');
            const menu = document.getElementById('user-dropdown-menu');
            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = menu.classList.toggle('open');
                trigger.setAttribute('aria-expanded', isOpen);
            });

            // Close on outside click
            document.addEventListener('click', (e) => {
                if (!document.getElementById('user-dropdown')?.contains(e.target)) {
                    menu.classList.remove('open');
                    trigger.setAttribute('aria-expanded', 'false');
                }
            });

        } else {
            authArea.innerHTML = `
                <a href="/pages/login.html" class="btn btn-sm btn-ghost">Log in</a>
                <a href="/pages/signup.html" class="btn btn-sm btn-primary">Sign Up</a>
            `;
        }
    }

    // Mobile menu toggle
    const menuBtn = document.getElementById('menu-toggle');
    const nav = document.getElementById('navbar-nav');
    if (menuBtn && nav) {
        menuBtn.addEventListener('click', () => nav.classList.toggle('mobile-open'));
    }

    // Active link highlighting
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Scroll effect
    let _hidden = false;
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        const ticker = document.querySelector('.ticker-wrap');
        if (navbar) {
            navbar.style.boxShadow = window.scrollY > 10 ? 'var(--shadow)' : 'none';
        }
        
        const shouldHide = window.scrollY > 100;
        if (shouldHide !== _hidden) {
            _hidden = shouldHide;
            if (ticker) ticker.classList.toggle('ticker-hidden', _hidden);
            if (navbar) navbar.classList.toggle('navbar-float', _hidden);
        }
    }, { passive: true });
}


// ── Global Search ───────────────────────────────────────────
function initSearch() {
    const input = document.getElementById('global-search');
    const results = document.getElementById('search-results');
    if (!input || !results) return;

    let debounce;
    input.addEventListener('input', () => {
        clearTimeout(debounce);
        const q = input.value.trim();
        if (q.length < 1) { results.classList.remove('active'); return; }
        debounce = setTimeout(async () => {
            try {
                const data = await api.get(`/instruments/search?q=${encodeURIComponent(q)}`);
                if (data.length === 0) {
                    results.innerHTML = '<div style="padding:16px;color:var(--text-light)">No results found</div>';
                } else {
                    results.innerHTML = data.map(i => `
                        <div class="search-result-item" onclick="window.location.href='/pages/instrument_detail.html?id=${i.id}'">
                            <div>
                                <strong>${i.symbol}</strong>
                                <span style="color:var(--text-light);font-size:0.8rem;margin-left:8px">${i.name}</span>
                            </div>
                            <div style="text-align:right">
                                <div style="font-weight:600">₹${Number(i.current_price).toLocaleString()}</div>
                                <div class="${i.day_change_pct >= 0 ? 'text-positive' : 'text-negative'}" style="font-size:0.75rem">
                                    ${i.day_change_pct >= 0 ? '+' : ''}${i.day_change_pct}%
                                </div>
                            </div>
                        </div>
                    `).join('');
                }
                results.classList.add('active');
            } catch (e) {
                results.classList.remove('active');
            }
        }, 300);
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !results.contains(e.target)) {
            results.classList.remove('active');
        }
    });
}

// ── Format Helpers ──────────────────────────────────────────
const cachedCurrencyFormatter = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 2 });
const cachedNumberFormatters = new Map();

function getNumberFormatter(decimals) {
    if (!cachedNumberFormatters.has(decimals)) {
        cachedNumberFormatters.set(decimals, new Intl.NumberFormat('en-IN', { maximumFractionDigits: decimals }));
    }
    return cachedNumberFormatters.get(decimals);
}

function formatCurrency(val) {
    if (val === null || val === undefined) return '—';
    return '₹' + cachedCurrencyFormatter.format(Number(val));
}

function formatNumber(val, decimals = 2) {
    if (val === null || val === undefined) return '—';
    return getNumberFormatter(decimals).format(Number(val));
}

function formatMarketCap(val) {
    if (!val) return '—';
    const n = Number(val);
    if (n >= 100000) return `₹${(n/100000).toFixed(1)}L Cr`;
    if (n >= 1000) return `₹${(n/1000).toFixed(1)}K Cr`;
    return `₹${n.toFixed(0)} Cr`;
}

// ── Auth Guard ──────────────────────────────────────────────
function requireAuth() {
    if (!Auth.isLoggedIn()) {
        window.location.href = '/pages/login.html';
        return false;
    }
    return true;
}

// ── Market Overview Nav Link Injection ──────────────────────
function initMarketOverviewNav() {
    const navbars = document.querySelectorAll('.navbar-nav');
    navbars.forEach(nav => {
        // Don't add if already present
        if (nav.querySelector('a[href="/pages/market-overview.html"]')) return;
        // Find the Dashboard link or last link to insert before
        const dashLink = nav.querySelector('a[href="/pages/dashboard.html"]');
        const moLink = document.createElement('a');
        moLink.href = '/pages/market-overview.html';
        moLink.className = 'nav-link';
        moLink.textContent = 'Market Overview';
        if (window.location.pathname === '/pages/market-overview.html') {
            moLink.classList.add('active');
        }
        if (dashLink) {
            nav.insertBefore(moLink, dashLink);
        } else {
            nav.appendChild(moLink);
        }
    });
}

// ── Footer Market Sections Injection ────────────────────────
function initFooterSections() {
    const footerBottom = document.querySelector('.footer-bottom');
    if (!footerBottom) return;

    // Market Overview tab data
    const marketTabs = {
        'Market Overview': [
            'Top Gainers Stocks', 'Top Losers Stocks', 'Most Traded Stocks', 'Stocks Feed',
            '52 Weeks High Stocks', '52 Weeks Low Stocks', 'Stocks Market Calendar',
            {"name": "Suzlon Energy", "id": 901},
            {"name": "Tata Motors", "id": 131},
            {"name": "IREDA", "id": 104},
            {"name": "Tata Steel", "id": 178},
            {"name": "Zomato (Eternal)", "id": 284},
            {"name": "NHPC", "id": 102},
            {"name": "State Bank of India", "id": 33},
            {"name": "Tata Power", "id": 96},
            {"name": "Yes Bank", "id": 56},
            {"name": "ITC", "id": 111},
            {"name": "Adani Power", "id": 109},
            "Bharat Heavy Electricals",
            {"name": "Infosys", "id": 2},
            {"name": "Wipro", "id": 3},
            {"name": "CDSL", "id": 176},
            {"name": "Indian Oil Corporation", "id": 94},
            {"name": "NBCC", "id": 218},
            "FII DII Activity",
            {"name": "IRFC", "id": 169},
            {"name": "Bharat Electronics", "id": 224},
            {"name": "HDFC Bank", "id": 31},
            {"name": "Vedanta", "id": 181},
            {"name": "Reliance Power", "id": 902}
        ],
        'Indices': [
            {name: 'Nifty 50', id: 492}, {name: 'BSE Sensex', id: 493}, {name: 'Nifty Bank', id: 494}, {name: 'Nifty IT', id: 495},
            {name: 'Nifty Pharma', id: 496}, {name: 'Nifty FMCG', id: 497}, {name: 'Nifty Auto', id: 498}, {name: 'Nifty Metal', id: 499},
            {name: 'Nifty Realty', id: 500}, {name: 'Nifty Media', id: 501}, {name: 'Nifty Energy', id: 502}, {name: 'Nifty Infrastructure', id: 503},
            {name: 'Nifty PSE', id: 504}, {name: 'Nifty Private Bank', id: 505}, {name: 'Nifty PSU Bank', id: 506}, {name: 'Nifty Financial Services', id: 507},
            {name: 'Nifty Fin Services 25/50', id: 508}, {name: 'Nifty 100', id: 509}, {name: 'Nifty 200', id: 510}, {name: 'Nifty 500', id: 511},
            {name: 'Nifty Next 50', id: 512}, {name: 'Nifty Midcap 50', id: 513}, {name: 'Nifty Midcap 100', id: 514}, {name: 'Nifty Midcap 150', id: 515},
            {name: 'Nifty Smallcap 100', id: 516}, {name: 'Nifty Smallcap 250', id: 517}, {name: 'Nifty Smallcap 50', id: 518}, {name: 'Nifty MicroCap 250', id: 519},
            {name: 'Nifty LargeMidcap 250', id: 520}, {name: 'Nifty Consumer Durables', id: 521}
        ],
        'ETFs': [
            {name: 'Nippon Nifty 50 BeES', id: 314}, {name: 'Nippon Bank BeES', id: 315}, {name: 'Nippon Gold BeES', id: 316}, {name: 'Nippon Silver BeES', id: 317},
            {name: 'Nippon IT BeES', id: 318}, {name: 'Nippon Pharma BeES', id: 319}, {name: 'Nippon Nifty Next 50 BeES', id: 320}, {name: 'Nippon Liquid BeES', id: 321},
            {name: 'CPSE ETF', id: 322}, {name: 'Bharat 22 ETF', id: 323}, {name: 'SBI Nifty 50 ETF', id: 324}, {name: 'SBI Nifty Next 50 ETF', id: 325},
            {name: 'SBI Gold ETF', id: 326}, {name: 'HDFC Nifty 50 ETF', id: 327}, {name: 'HDFC Sensex ETF', id: 328}, {name: 'HDFC Gold ETF', id: 329},
            {name: 'ICICI Nifty 50 ETF', id: 330}, {name: 'ICICI Bank Nifty ETF', id: 331}, {name: 'Kotak Nifty ETF', id: 332}, {name: 'Kotak Gold ETF', id: 333}
        ]
    };

    // Calc link helper
    const calcLinks = {
        'SIP Calculator': '/pages/calculators/sip.html',
        'Lumpsum Calculator': '/pages/calculators/lumpsum.html',
        'EMI Calculator': '/pages/calculators/emi.html',
        'FD Calculator': '/pages/calculators/fd.html',
        'RD Calculator': '/pages/calculators/rd.html',
        'PPF Calculator': '/pages/calculators/ppf.html',
        'EPF Calculator': '/pages/calculators/epf.html',
        'SWP Calculator': '/pages/calculators/swp.html',
        'Home Loan EMI': '/pages/calculators/home-loan.html',
        'Car Loan Calculator': '/pages/calculators/car-loan.html',
        'Income Tax Calculator': '/pages/calculators/income-tax.html',
        'GST Calculator': '/pages/calculators/gst.html',
        'TDS Calculator': '/pages/calculators/tds.html',
        'Brokerage Calculator': '/pages/calculators/brokerage.html',
        'Margin Calculator': '/pages/calculators/margin.html',
        'HRA Calculator': '/pages/calculators/hra.html',
        'Step-up SIP Calculator': '/pages/calculators/step-up-sip.html',
        'Options Calculator': '/pages/calculators/margin.html'
    };

    function getLink(item) {
        if (typeof item === 'object' && item.id) {
            return `/pages/instrument_detail.html?id=${item.id}`;
        }
        if (typeof item === 'string' && calcLinks[item]) return calcLinks[item];
        
        const catLinks = {
            'Top Gainers Stocks': '/pages/top-gainers.html',
            'Top Losers Stocks': '/pages/top-losers.html',
            '52 Weeks High Stocks': '/pages/52-weeks-high.html',
            '52 Weeks Low Stocks': '/pages/52-weeks-low.html',
            'Most Traded Stocks': '/pages/most-traded.html',
            'Stocks Market Calendar': '/pages/market-calendar.html',
            'Stocks Feed': '/pages/stocks-feed.html'
        };
        const name = typeof item === 'string' ? item : item.name;
        if (catLinks[name]) return catLinks[name];
        
        return '/pages/screeners.html?filter=' + encodeURIComponent(name);
    }

    // Build Market Overview section
    const visibleCount = 24; // first 24 links visible
    let tabsHTML = '<div class="footer-section-tabs" id="footer-mo-tabs">';
    let panelsHTML = '';
    let first = true;
    for (const [tabName, items] of Object.entries(marketTabs)) {
        const activeClass = first ? ' active' : '';
        tabsHTML += `<button class="footer-section-tab${activeClass}" data-tab="${tabName}">${tabName}</button>`;
        let linksHTML = '';
        items.forEach((item, idx) => {
            const extra = idx >= visibleCount ? ' class="extra-link"' : '';
            const itemName = typeof item === 'object' ? item.name : item;
            linksHTML += `<a href="${getLink(item)}"${extra}>${itemName}</a>`;
        });
        panelsHTML += `<div class="footer-tab-panel${activeClass}" data-panel="${tabName}"><div class="footer-link-grid" id="footer-grid-${tabName.replace(/[^a-zA-Z]/g,'')}">${linksHTML}</div></div>`;
        first = false;
    }
    tabsHTML += '</div>';

    // Assemble full HTML
    const sectionsHTML = `
        <div class="footer-market-sections">
            <!-- Market Overview -->
            <div class="footer-market-section">
                ${tabsHTML}
                ${panelsHTML}
                <button class="footer-show-more" id="footer-show-more">
                    Show More <span class="chevron"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-bottom: 2px; margin-right: 2px;"><polyline points="6 9 12 15 18 9"></polyline></svg></span>
                </button>
            </div>
        </div>
    `;

    footerBottom.insertAdjacentHTML('beforebegin', sectionsHTML);

    // Tab switching
    const tabs = document.querySelectorAll('#footer-mo-tabs .footer-section-tab');
    const panels = document.querySelectorAll('.footer-tab-panel');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            tab.classList.add('active');
            const panel = document.querySelector(`.footer-tab-panel[data-panel="${tab.dataset.tab}"]`);
            if (panel) panel.classList.add('active');
        });
    });

    // Show More toggle
    const showMoreBtn = document.getElementById('footer-show-more');
    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', () => {
            const grids = document.querySelectorAll('.footer-market-sections .footer-tab-panel .footer-link-grid');
            const isExpanded = showMoreBtn.classList.toggle('expanded');
            grids.forEach(g => {
                if (isExpanded) {
                    g.classList.add('expanded');
                } else {
                    g.classList.remove('expanded');
                }
            });
            showMoreBtn.innerHTML = isExpanded
                ? 'Show Less <span class="chevron"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-bottom: 2px; margin-right: 2px;"><polyline points="6 9 12 15 18 9"></polyline></svg></span>'
                : 'Show More <span class="chevron"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-bottom: 2px; margin-right: 2px;"><polyline points="6 9 12 15 18 9"></polyline></svg></span>';
        });
    }
}

// ── Scroll-to-Top Button ────────────────────────────────────
function initScrollToTop() {
    // Inject button into DOM
    const btn = document.createElement('button');
    btn.className = 'scroll-to-top';
    btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"></polyline></svg>';
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    document.body.appendChild(btn);

    window.addEventListener('scroll', () => {
        btn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
}

// ── Keyboard Shortcuts ──────────────────────────────────────
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl+K or Cmd+K → Focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const search = document.getElementById('global-search');
            if (search) search.focus();
        }

        // Esc → Close modals, chatbot, search
        if (e.key === 'Escape') {
            // Close chatbot
            if (typeof chatPanelOpen !== 'undefined' && chatPanelOpen && typeof toggleChatbot === 'function') {
                toggleChatbot();
            }
            // Close modals
            document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
            // Close search results
            const results = document.getElementById('search-results');
            if (results) results.classList.remove('active');
        }
    });
}

// ── Compare Nav Link Injection ──────────────────────────────
function initCompareNav() {
    const navbars = document.querySelectorAll('.navbar-nav');
    navbars.forEach(nav => {
        if (nav.querySelector('a[href="/pages/compare.html"]')) return;
        const moLink = nav.querySelector('a[href="/pages/market-overview.html"]');
        const cmpLink = document.createElement('a');
        cmpLink.href = '/pages/compare.html';
        cmpLink.className = 'nav-link';
        cmpLink.textContent = 'Compare';
        if (window.location.pathname === '/pages/compare.html') {
            cmpLink.classList.add('active');
        }
        if (moLink) {
            moLink.insertAdjacentElement('afterend', cmpLink);
        } else {
            const dashLink = nav.querySelector('a[href="/pages/dashboard.html"]');
            if (dashLink) nav.insertBefore(cmpLink, dashLink);
            else nav.appendChild(cmpLink);
        }
    });
}

// ── Init on DOM ready ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initSearch();
    initMarketOverviewNav();
    initCompareNav();
    initFooterSections();
    initScrollToTop();
    initKeyboardShortcuts();
});

// Global Glow Card Tracker
document.addEventListener("mousemove", e => {
    const cards = document.querySelectorAll(".glow-card");
    for(const card of cards) {
        const rect = card.getBoundingClientRect(),
              x = e.clientX - rect.left,
              y = e.clientY - rect.top;
        card.style.setProperty("--mouse-x", `${x}px`);
        card.style.setProperty("--mouse-y", `${y}px`);
    }
});
