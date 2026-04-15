/**
 * FinSight – Screeners JS
 * Load predefined, build custom, run and display results.
 */
document.addEventListener('DOMContentLoaded', loadPredefined);

async function loadPredefined() {
    const container = document.getElementById('predefined-screeners');
    try {
        const screens = await api.get('/screeners/predefined');
        // Unique icon per screener strategy
        const icons = [
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 17"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg>',
            '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"/></svg>',
        ];
        container.innerHTML = screens.map((s, i) => `
            <div class="screener-card" onclick='runPredefined(${JSON.stringify(s.definition_json)})'>
                <div class="screener-icon">${icons[i % icons.length]}</div>
                <h4>${s.name}</h4>
                <p>${s.description || ''}</p>
            </div>
        `).join('');
    } catch (e) {
        container.innerHTML = '<p style="color:var(--danger)">Failed to load screeners</p>';
    }
}

async function runPredefined(defJson) {
    const definition_json = typeof defJson === 'string' ? JSON.parse(defJson) : defJson;
    await runScreen(definition_json);
}

function addFilterRow() {
    const html = `
        <div class="filter-row">
            <select class="filter-field">
                <option value="pe">PE Ratio</option>
                <option value="pb">PB Ratio</option>
                <option value="roe">ROE %</option>
                <option value="roce">ROCE %</option>
                <option value="debt_to_equity">Debt/Equity</option>
                <option value="net_profit_margin">Net Margin %</option>
                <option value="sales_growth">Sales Growth %</option>
                <option value="profit_growth">Profit Growth %</option>
                <option value="market_cap">Market Cap (Cr)</option>
            </select>
            <select class="filter-op">
                <option value=">">&gt;</option>
                <option value="<">&lt;</option>
                <option value=">=">&ge;</option>
                <option value="<=">&le;</option>
                <option value="=">=</option>
            </select>
            <input type="number" step="any" class="filter-value" placeholder="Value">
            <button class="filter-remove" onclick="this.closest('.filter-row').remove()">×</button>
        </div>
    `;
    document.getElementById('filter-rows').insertAdjacentHTML('beforeend', html);
}

function getFilterDefinition() {
    const rows = document.querySelectorAll('.filter-row');
    const conditions = [];
    rows.forEach(row => {
        const field = row.querySelector('.filter-field').value;
        const op = row.querySelector('.filter-op').value;
        const value = parseFloat(row.querySelector('.filter-value').value);
        if (!isNaN(value)) conditions.push({ field, op, value });
    });
    const logic = document.getElementById('filter-logic').value;
    return { conditions, logic };
}

async function runCustomScreen() {
    const defn = getFilterDefinition();
    if (defn.conditions.length === 0) {
        showToast('Add at least one filter with a value', 'error');
        return;
    }
    await runScreen(defn);
}

async function runScreen(definition_json) {
    const section = document.getElementById('results-section');
    const tbody = document.getElementById('results-tbody');
    section.style.display = 'block';
    tbody.innerHTML = '<tr><td colspan="11" style="text-align:center;padding:32px"><div class="spinner" style="margin:0 auto"></div></td></tr>';

    try {
        const results = await api.post('/screeners/run', { definition_json });
        document.getElementById('result-count').textContent = results.length + ' matches';
        if (results.length === 0) {
            tbody.innerHTML = '<tr><td colspan="11" style="text-align:center;padding:32px;color:var(--text-light)">No instruments match your criteria</td></tr>';
            return;
        }
        tbody.innerHTML = results.map(r => `
            <tr onclick="window.location.href='/pages/instrument_detail.html?id=${r.id}'" style="cursor:pointer">
                <td><strong>${r.symbol}</strong></td>
                <td>${r.name}</td>
                <td>${r.sector || '—'}</td>
                <td>${formatMarketCap(r.market_cap)}</td>
                <td>${formatCurrency(r.current_price)}</td>
                <td>${formatNumber(r.pe)}</td>
                <td>${formatNumber(r.pb)}</td>
                <td>${formatNumber(r.roe)}%</td>
                <td>${formatNumber(r.debt_to_equity)}</td>
                <td>${formatNumber(r.sales_growth)}%</td>
                <td>${formatNumber(r.profit_growth)}%</td>
            </tr>
        `).join('');
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="11" style="color:var(--danger)">Error running screen</td></tr>';
    }
}

async function saveCustomScreen() {
    if (!Auth.isLoggedIn()) { showToast('Login to save screens', 'info'); return; }
    const defn = getFilterDefinition();
    if (defn.conditions.length === 0) { showToast('Add filters first', 'error'); return; }
    const name = prompt('Screen name:');
    if (!name) return;
    try {
        await api.post('/screeners/custom', { name, description: '', definition_json: defn });
        showToast('Screen saved!', 'success');
    } catch (e) {
        showToast(e.error || 'Save failed', 'error');
    }
}
