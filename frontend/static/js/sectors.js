/**
 * FinSight – Sectors JS
 * Loads sector list, displays sector detail instrument table.
 * Each sector has a unique, industry-appropriate SVG icon.
 */
const SECTOR_ICONS = {
    'Information Technology': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
        css: 'it'
    },
    'Banking': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M3 10h18"/><path d="M12 3l9 7H3l9-7z"/><path d="M5 10v11"/><path d="M19 10v11"/><path d="M9 10v11"/><path d="M15 10v11"/></svg>',
        css: 'banking'
    },
    'Pharma': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        css: 'pharma'
    },
    'Energy': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        css: 'energy'
    },
    'FMCG': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
        css: 'fmcg'
    },
    'Automobile': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17h14a2 2 0 0 0 2-2v-3l-2.5-5H5.5L3 12v3a2 2 0 0 0 2 2z"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/></svg>',
        css: 'auto'
    },
    'Financial Services': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        css: 'finserv'
    },
    'Metals and Mining': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
        css: 'metals'
    },
    'Real Estate': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
        css: 'realty'
    },
    'Infrastructure': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="4" y1="10" x2="20" y2="10"/><line x1="12" y1="2" x2="12" y2="22"/></svg>',
        css: 'infra'
    },
    'Telecom': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>',
        css: 'telecom'
    },
    'Media': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>',
        css: 'media'
    },
    'Chemicals': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 2h7"/><path d="M10 2v7.31"/><path d="M14 9.3V2"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><line x1="5.52" y1="16" x2="18.48" y2="16"/></svg>',
        css: 'chemicals'
    },
    'Consumer Durables': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
        css: 'consumer'
    },
    'Insurance': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        css: 'insurance'
    },
    'Diversified': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
        css: 'diversified'
    },
    'ETF': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        css: 'etf'
    },
    'Mutual Fund': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
        css: 'fund'
    },
    'Index': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
        css: 'index'
    },
    'Commodity': {
        icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>',
        css: 'commodity'
    },
};

document.addEventListener('DOMContentLoaded', loadSectors);

async function loadSectors() {
    const grid = document.getElementById('sector-grid');
    try {
        const sectors = await api.get('/sectors/');
        grid.innerHTML = sectors.map(s => {
            const meta = SECTOR_ICONS[s.sector] || { icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>', css: 'default' };
            const changeCls = s.avg_day_change_pct >= 0 ? 'text-positive' : 'text-negative';
            return `
                <div class="sector-card" onclick="loadSectorDetail('${s.sector}')">
                    <div class="sector-icon ${meta.css}">${meta.icon}</div>
                    <h4>${s.sector}</h4>
                    <div class="sector-stats">
                        ${s.instrument_count} instruments ·
                        <span class="${changeCls}">${s.avg_day_change_pct >= 0 ? '+' : ''}${s.avg_day_change_pct}%</span>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        grid.innerHTML = '<p style="color:var(--danger)">Failed to load sectors</p>';
    }
}

async function loadSectorDetail(sectorName) {
    const section = document.getElementById('sector-detail');
    const tbody = document.getElementById('sector-tbody');
    document.getElementById('sector-title').textContent = sectorName;
    section.style.display = 'block';
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:32px"><div class="spinner" style="margin:0 auto"></div></td></tr>';

    try {
        const instruments = await api.get(`/sectors/${encodeURIComponent(sectorName)}/instruments`);
        tbody.innerHTML = instruments.map(i => `
            <tr onclick="window.location.href='/pages/instrument_detail.html?id=${i.id}'" style="cursor:pointer">
                <td><strong>${i.symbol}</strong></td>
                <td>${i.name}</td>
                <td>${i.industry || '—'}</td>
                <td>${formatMarketCap(i.market_cap)}</td>
                <td>${formatCurrency(i.current_price)}</td>
                <td class="${i.day_change_pct >= 0 ? 'text-positive' : 'text-negative'}">
                    ${i.day_change_pct >= 0 ? '+' : ''}${i.day_change_pct}%
                </td>
                <td>${formatCurrency(i.high_52w)}</td>
                <td>${formatCurrency(i.low_52w)}</td>
            </tr>
        `).join('');
        section.scrollIntoView({ behavior: 'smooth' });
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="8" style="color:var(--danger)">Failed to load</td></tr>';
    }
}

function closeSectorDetail() {
    document.getElementById('sector-detail').style.display = 'none';
}
