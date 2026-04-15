/**
 * FinSight – Dashboard JS
 * Loads profile, watchlists, portfolio positions.
 */
document.addEventListener('DOMContentLoaded', () => {
    if (!requireAuth()) return;
    loadProfile();
    loadWatchlists();
    loadPositions();
});

async function loadProfile() {
    try {
        const user = await api.get('/user/profile');
        document.getElementById('user-name').textContent = user.name || 'User';
        document.getElementById('user-email').textContent = user.email;
        const meta = document.getElementById('profile-meta');
        meta.innerHTML = `
            <span><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width: 1em; height: 1em; vertical-align: middle;"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg> ${user.risk_profile || 'Moderate'}</span>
            <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg> ${user.experience_level || 'Beginner'}</span>
            <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg> ${user.country || 'India'}</span>
        `;
    } catch (e) {
        console.error('Profile load error:', e);
    }
}

async function loadWatchlists() {
    const container = document.getElementById('watchlists-container');
    try {
        const watchlists = await api.get('/watchlists/');
        if (watchlists.length === 0) {
            container.innerHTML = '<p style="color:var(--text-light);padding:20px 0">No watchlists yet. Create one to start tracking stocks!</p>';
            return;
        }
        container.innerHTML = watchlists.map(wl => `
            <div class="watchlist-card card" style="margin-bottom:16px">
                <div class="flex-between mb-2">
                    <h4>${wl.name}</h4>
                    <span class="badge badge-info">${wl.items.length} items</span>
                </div>
                ${wl.items.length === 0 
                    ? '<p style="color:var(--text-light);font-size:0.85rem">Empty watchlist</p>'
                    : wl.items.map(item => `
                        <div class="watchlist-item">
                            <div>
                                <a href="/pages/instrument_detail.html?id=${item.instrument_id}" class="instrument-name" style="color:var(--text)">${item.symbol}</a>
                                <span style="color:var(--text-light);font-size:0.75rem;margin-left:8px">${item.name}</span>
                            </div>
                            <div class="instrument-price">
                                <div class="price">${formatCurrency(item.current_price)}</div>
                                <div class="change ${item.day_change_pct >= 0 ? 'text-positive' : 'text-negative'}">
                                    ${item.day_change_pct >= 0 ? '+' : ''}${item.day_change_pct}%
                                </div>
                            </div>
                        </div>
                    `).join('')
                }
            </div>
        `).join('');
    } catch (e) {
        container.innerHTML = '<p style="color:var(--danger)">Failed to load watchlists</p>';
    }
}

async function createWatchlist() {
    const name = prompt('Watchlist name:');
    if (!name) return;
    try {
        await api.post('/watchlists/', { name });
        showToast('Watchlist created!', 'success');
        loadWatchlists();
    } catch (e) {
        showToast(e.error || 'Failed to create watchlist', 'error');
    }
}

async function loadPositions() {
    const tbody = document.getElementById('positions-tbody');
    try {
        const positions = await api.get('/portfolio/');
        if (positions.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;padding:32px;color:var(--text-light)">No positions yet</td></tr>';
            updateSummary(0, 0, 0);
            return;
        }
        let totalInvested = 0, totalCurrent = 0, totalPL = 0;
        tbody.innerHTML = positions.map(p => {
            const invested = p.buy_price * p.quantity;
            const current = p.current_price * p.quantity;
            totalInvested += invested;
            totalCurrent += current;
            totalPL += p.unrealized_pl;
            return `<tr>
                <td><a href="/pages/instrument_detail.html?id=${p.instrument_id}">${p.symbol} – ${p.name}</a></td>
                <td>${p.quantity}</td>
                <td>${formatCurrency(p.buy_price)}</td>
                <td>${formatCurrency(p.current_price)}</td>
                <td class="${p.unrealized_pl >= 0 ? 'text-positive' : 'text-negative'}">${formatCurrency(p.unrealized_pl)}</td>
                <td class="${p.return_pct >= 0 ? 'text-positive' : 'text-negative'}">${p.return_pct}%</td>
            </tr>`;
        }).join('');
        updateSummary(totalInvested, totalCurrent, totalPL);
        renderAllocationChart(positions);
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="6" style="color:var(--danger)">Failed to load</td></tr>';
    }
}

function renderAllocationChart(positions) {
    const card = document.getElementById('allocation-card');
    const canvas = document.getElementById('allocation-chart');
    if (!card || !canvas || typeof Chart === 'undefined' || positions.length === 0) return;

    card.style.display = 'block';

    // Group by sector
    const sectorMap = {};
    positions.forEach(p => {
        const sector = p.sector || 'Other';
        const value = p.current_price * p.quantity;
        sectorMap[sector] = (sectorMap[sector] || 0) + value;
    });

    const labels = Object.keys(sectorMap);
    const data = Object.values(sectorMap);
    const colors = [
        '#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b',
        '#ef4444', '#ec4899', '#6366f1', '#14b8a6', '#f97316',
        '#84cc16', '#a855f7'
    ];

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#ffffff',
                hoverBorderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { font: { size: 12, weight: '500' }, padding: 12 }
                }
            }
        }
    });
}

function updateSummary(invested, current, pl) {
    document.getElementById('total-invested').textContent = formatCurrency(invested);
    document.getElementById('current-value').textContent = formatCurrency(current);
    const plEl = document.getElementById('total-pl');
    plEl.textContent = formatCurrency(pl);
    plEl.className = `stat-value ${pl >= 0 ? 'text-positive' : 'text-negative'}`;
}

function showAddPosition() {
    document.getElementById('position-modal').classList.add('active');
}

async function addPosition() {
    const data = {
        instrument_id: parseInt(document.getElementById('pos-instrument').value),
        quantity: parseFloat(document.getElementById('pos-qty').value),
        buy_price: parseFloat(document.getElementById('pos-price').value),
        buy_date: document.getElementById('pos-date').value,
    };
    try {
        await api.post('/portfolio/positions', data);
        showToast('Position added!', 'success');
        document.getElementById('position-modal').classList.remove('active');
        loadPositions();
    } catch (e) {
        showToast(e.error || 'Failed to add position', 'error');
    }
}
