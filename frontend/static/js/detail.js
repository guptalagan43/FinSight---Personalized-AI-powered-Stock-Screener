/**
 * FinSight – Instrument Detail JS
 * Loads instrument data, renders Chart.js chart, fundamentals.
 */
let priceChart = null;
const instrumentId = new URLSearchParams(window.location.search).get('id');

document.addEventListener('DOMContentLoaded', () => {
    if (!instrumentId) {
        showToast('No instrument ID specified', 'error');
        return;
    }
    loadInstrument();
    loadChart('1M');
    loadFundamentals();
    initChartControls();
});

async function loadInstrument() {
    try {
        const inst = await api.get(`/instruments/${instrumentId}`);
        document.title = `${inst.symbol} – ${inst.name} | FinSight`;
        document.getElementById('inst-name').textContent = inst.name;
        document.getElementById('inst-symbol').textContent = inst.symbol;
        document.getElementById('inst-exchange').textContent = inst.exchange;
        document.getElementById('inst-sector').textContent = inst.sector || 'N/A';
        document.getElementById('inst-price').textContent = formatCurrency(inst.current_price);
        document.getElementById('chat-inst-name').textContent = inst.name;

        const changeEl = document.getElementById('inst-change');
        const pct = inst.day_change_pct || 0;
        const abs = inst.day_change || 0;
        changeEl.textContent = `${abs >= 0 ? '+' : ''}${abs} (${pct >= 0 ? '+' : ''}${pct}%)`;
        changeEl.className = `price-change ${pct >= 0 ? 'text-positive' : 'text-negative'}`;

        document.getElementById('stat-mcap').textContent = formatMarketCap(inst.market_cap);
        document.getElementById('stat-52h').textContent = formatCurrency(inst.high_52w);
        document.getElementById('stat-52l').textContent = formatCurrency(inst.low_52w);
        document.getElementById('stat-daychange').textContent = `${pct >= 0 ? '+' : ''}${pct}%`;
        document.getElementById('stat-daychange').className = `f-value ${pct >= 0 ? 'text-positive' : 'text-negative'}`;
    } catch (e) {
        showToast('Failed to load instrument', 'error');
    }
}

async function loadChart(range) {
    try {
        const res = await api.get(`/instruments/${instrumentId}/chart?range=${range}`);
        const data = res.data;
        const labels = data.map(d => d.timestamp.split('T')[0] || d.timestamp);
        const prices = data.map(d => d.close);

        if (priceChart) priceChart.destroy();

        const ctx = document.getElementById('price-chart').getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(46, 196, 182, 0.3)');
        gradient.addColorStop(1, 'rgba(46, 196, 182, 0)');

        priceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Price (₹)',
                    data: prices,
                    borderColor: '#2EC4B6',
                    backgroundColor: gradient,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: '#FF9F1C',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { intersect: false, mode: 'index' },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1F2937',
                        titleColor: '#FFBF69',
                        bodyColor: '#fff',
                        cornerRadius: 8,
                        padding: 12,
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { maxTicksLimit: 8, font: { size: 11 } }
                    },
                    y: {
                        grid: { color: 'rgba(0,0,0,0.05)' },
                        ticks: { font: { size: 11 } }
                    }
                }
            }
        });
    } catch (e) {
        console.error('Chart error:', e);
    }
}

function initChartControls() {
    document.querySelectorAll('.chart-range-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.chart-range-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadChart(btn.dataset.range);
        });
    });
}

async function loadFundamentals() {
    try {
        const rows = await api.get(`/instruments/${instrumentId}/fundamentals`);
        const grid = document.getElementById('fundamentals-grid');
        const thead = document.getElementById('fin-thead');
        const tbody = document.getElementById('fin-tbody');

        if (rows.length === 0) {
            grid.innerHTML = '<p style="color:var(--text-light);grid-column:1/-1">No fundamentals available</p>';
            tbody.innerHTML = '<tr><td colspan="10" style="text-align:center">No data</td></tr>';
            return;
        }

        // Latest fundamentals grid
        const latest = rows[0];
        const metrics = [
            { label: 'PE Ratio', key: 'pe' },
            { label: 'PB Ratio', key: 'pb' },
            { label: 'ROE %', key: 'roe' },
            { label: 'ROCE %', key: 'roce' },
            { label: 'EPS', key: 'eps' },
            { label: 'D/E Ratio', key: 'debt_to_equity' },
            { label: 'Net Margin %', key: 'net_profit_margin' },
            { label: 'Promoter %', key: 'promoter_holding' },
        ];
        grid.innerHTML = metrics.map(m => `
            <div class="fundamental-item">
                <div class="f-label">${m.label}</div>
                <div class="f-value">${latest[m.key] !== null ? formatNumber(latest[m.key]) : '—'}</div>
            </div>
        `).join('');

        // Financial history table
        const fields = ['revenue', 'net_profit', 'eps', 'roe', 'roce', 'pe', 'pb', 'debt_to_equity', 'sales_growth', 'profit_growth'];
        const fieldLabels = ['Revenue (Cr)', 'Net Profit (Cr)', 'EPS', 'ROE %', 'ROCE %', 'PE', 'PB', 'D/E', 'Sales Gr %', 'Profit Gr %'];

        thead.innerHTML = `<tr><th>Metric</th>${rows.map(r => `<th>${r.fiscal_year}</th>`).join('')}</tr>`;
        tbody.innerHTML = fields.map((f, i) => `
            <tr>
                <td style="font-weight:500">${fieldLabels[i]}</td>
                ${rows.map(r => `<td>${r[f] !== null ? formatNumber(r[f]) : '—'}</td>`).join('')}
            </tr>
        `).join('');
    } catch (e) {
        console.error('Fundamentals error:', e);
    }
}

async function addToWatchlist() {
    if (!Auth.isLoggedIn()) {
        showToast('Please login to add to watchlist', 'info');
        return;
    }
    try {
        // Get or create default watchlist
        let watchlists = await api.get('/watchlists/');
        let wlId;
        if (watchlists.length === 0) {
            const wl = await api.post('/watchlists/', { name: 'My Watchlist' });
            wlId = wl.id;
        } else {
            wlId = watchlists[0].id;
        }
        await api.post(`/watchlists/${wlId}/items`, { instrument_id: parseInt(instrumentId) });
        showToast('Added to watchlist!', 'success');
    } catch (e) {
        showToast(e.error || e.message || 'Already in watchlist', 'info');
    }
}
