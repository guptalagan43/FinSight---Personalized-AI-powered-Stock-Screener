/**
 * FinSight – Stock Comparison Tool v2
 * Side-by-side comparison with radar chart and AI analysis
 * Fetches fundamentals from the proper API endpoint
 */

let stockA = null;
let stockB = null;
let radarChart = null;

/* ── Search & Select Stock ──────────────────────────────── */
async function searchStock(inputId, resultsId) {
    const input = document.getElementById(inputId);
    const results = document.getElementById(resultsId);
    if (!input || !results) return;

    const q = input.value.trim();
    if (q.length < 1) { results.innerHTML = ''; results.style.display = 'none'; return; }

    try {
        const data = await api.get(`/instruments/search?q=${encodeURIComponent(q)}`);
        if (data.length === 0) {
            results.innerHTML = '<div style="padding:12px; color:var(--text-light)">No results</div>';
        } else {
            results.innerHTML = data.slice(0, 8).map(i => `
                <div class="compare-result-item" onclick="selectStock('${inputId}', ${JSON.stringify(i).replace(/"/g, '&quot;')})">
                    <strong>${i.symbol}</strong>
                    <span style="color:var(--text-light); font-size:0.85rem; margin-left:8px">${i.name}</span>
                    <span style="margin-left:auto; font-weight:600">₹${Number(i.current_price).toLocaleString()}</span>
                </div>
            `).join('');
        }
        results.style.display = 'block';
    } catch (e) {
        results.style.display = 'none';
    }
}

async function selectStock(inputId, instrument) {
    const input = document.getElementById(inputId);
    const resultsId = inputId.replace('input', 'results');
    const results = document.getElementById(resultsId);

    input.value = `${instrument.symbol} – ${instrument.name}`;
    if (results) results.style.display = 'none';

    // Fetch fundamentals for this stock
    const enriched = await fetchWithFundamentals(instrument);

    if (inputId === 'stock-a-input') {
        stockA = enriched;
        showStockCard('stock-a-card', enriched);
    } else {
        stockB = enriched;
        showStockCard('stock-b-card', enriched);
    }

    if (stockA && stockB) {
        runComparison();
    }
}

async function fetchWithFundamentals(instrument) {
    try {
        const fundData = await api.get(`/instruments/${instrument.id}/fundamentals`);
        if (fundData && fundData.length > 0) {
            // Merge latest fundamentals into instrument
            const latest = fundData[0]; // Already sorted by fiscal_year desc
            return { ...instrument, ...latest, ...{ id: instrument.id, name: instrument.name, symbol: instrument.symbol } };
        }
    } catch (e) {
        console.log('Could not fetch fundamentals for', instrument.symbol, e);
    }
    return instrument;
}

function showStockCard(cardId, inst) {
    const card = document.getElementById(cardId);
    if (!card) return;
    const changePct = inst.day_change_pct || 0;
    const isUp = changePct >= 0;

    // Build quick metrics from fundamentals
    const metricsHtml = [
        { label: 'PE', val: inst.pe },
        { label: 'ROE', val: inst.roe, fmt: v => v + '%' },
        { label: 'D/E', val: inst.debt_to_equity },
    ].filter(m => m.val != null).map(m =>
        `<span style="font-size:0.75rem; padding:3px 8px; background:var(--bg-alt); border-radius:4px; color:var(--text-light);">${m.label}: <strong>${m.fmt ? m.fmt(Number(m.val).toFixed(1)) : Number(m.val).toFixed(1)}</strong></span>`
    ).join(' ');

    card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
                <div style="font-weight:700; font-size:1.1rem;">${inst.symbol}</div>
                <div style="font-size:0.85rem; color:var(--text-light);">${inst.name}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-weight:700; font-size:1.2rem;">₹${Number(inst.current_price).toLocaleString()}</div>
                <div class="${isUp ? 'text-positive' : 'text-negative'}" style="font-size:0.85rem; font-weight:600;">${isUp ? '+' : ''}${changePct.toFixed(2)}%</div>
            </div>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
            <span style="font-size:0.8rem; color:var(--text-muted);">${inst.sector || 'N/A'}</span>
            ${metricsHtml}
        </div>
    `;
    card.style.display = 'block';
}

/* ── Run Comparison ─────────────────────────────────────── */
function runComparison() {
    const section = document.getElementById('comparison-results');
    if (!section) return;
    section.style.display = 'block';

    // Update table headers
    const thA = document.getElementById('th-stock-a');
    const thB = document.getElementById('th-stock-b');
    if (thA) thA.textContent = stockA.symbol;
    if (thB) thB.textContent = stockB.symbol;

    renderComparisonTable(stockA, stockB);
    renderRadarChart(stockA, stockB);
    generateAIComparison(stockA, stockB);

    // Scroll to results
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderComparisonTable(a, b) {
    const tbody = document.getElementById('comparison-tbody');
    if (!tbody) return;

    const metrics = [
        { label: 'Current Price', key: 'current_price', fmt: v => '₹' + Number(v).toLocaleString() },
        { label: 'Day Change', key: 'day_change_pct', fmt: v => (v >= 0 ? '+' : '') + Number(v).toFixed(2) + '%', color: true },
        { label: 'Market Cap', key: 'market_cap', fmt: v => v ? '₹' + Number(v).toLocaleString() + ' Cr' : 'N/A' },
        { label: 'PE Ratio', key: 'pe', fmt: v => v ? Number(v).toFixed(1) : 'N/A', lower: true },
        { label: 'PB Ratio', key: 'pb', fmt: v => v ? Number(v).toFixed(1) : 'N/A', lower: true },
        { label: 'ROE (%)', key: 'roe', fmt: v => v ? Number(v).toFixed(1) + '%' : 'N/A' },
        { label: 'ROCE (%)', key: 'roce', fmt: v => v ? Number(v).toFixed(1) + '%' : 'N/A' },
        { label: 'Debt/Equity', key: 'debt_to_equity', fmt: v => v != null ? Number(v).toFixed(2) : 'N/A', lower: true },
        { label: 'Net Margin (%)', key: 'net_profit_margin', fmt: v => v ? Number(v).toFixed(1) + '%' : 'N/A' },
        { label: 'Sales Growth (%)', key: 'sales_growth', fmt: v => v ? Number(v).toFixed(1) + '%' : 'N/A' },
        { label: 'Profit Growth (%)', key: 'profit_growth', fmt: v => v ? Number(v).toFixed(1) + '%' : 'N/A' },
        { label: 'Promoter Holding (%)', key: 'promoter_holding', fmt: v => v ? Number(v).toFixed(1) + '%' : 'N/A' },
        { label: 'EPS', key: 'eps', fmt: v => v ? '₹' + Number(v).toFixed(2) : 'N/A' },
    ];

    tbody.innerHTML = metrics.map(m => {
        const valA = a[m.key];
        const valB = b[m.key];
        const fmtA = valA != null ? m.fmt(valA) : 'N/A';
        const fmtB = valB != null ? m.fmt(valB) : 'N/A';

        let classA = '', classB = '';
        if (valA != null && valB != null && m.key !== 'current_price' && m.key !== 'market_cap') {
            const lowerBetter = m.lower === true;
            if (lowerBetter) {
                if (valA < valB) classA = 'compare-winner';
                else if (valB < valA) classB = 'compare-winner';
            } else {
                if (valA > valB) classA = 'compare-winner';
                else if (valB > valA) classB = 'compare-winner';
            }
        }

        if (m.color && valA != null) classA += valA >= 0 ? ' text-positive' : ' text-negative';
        if (m.color && valB != null) classB += valB >= 0 ? ' text-positive' : ' text-negative';

        return `<tr>
            <td class="${classA}" style="text-align:right; font-weight:600;">${fmtA}</td>
            <td style="text-align:center; font-weight:500; color:var(--text-light);">${m.label}</td>
            <td class="${classB}" style="font-weight:600;">${fmtB}</td>
        </tr>`;
    }).join('');
}

function renderRadarChart(a, b) {
    const canvas = document.getElementById('radar-chart');
    if (!canvas || typeof Chart === 'undefined') return;

    const labels = ['ROE', 'ROCE', 'Net Margin', 'Sales Growth', 'Profit Growth'];
    const keysArr = ['roe', 'roce', 'net_profit_margin', 'sales_growth', 'profit_growth'];

    const dataA = keysArr.map(k => Math.max(0, Number(a[k]) || 0));
    const dataB = keysArr.map(k => Math.max(0, Number(b[k]) || 0));

    if (radarChart) radarChart.destroy();

    radarChart = new Chart(canvas, {
        type: 'radar',
        data: {
            labels,
            datasets: [
                {
                    label: a.symbol || 'Stock A',
                    data: dataA,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.15)',
                    borderWidth: 2.5,
                    pointBackgroundColor: '#3b82f6',
                    pointRadius: 4,
                },
                {
                    label: b.symbol || 'Stock B',
                    data: dataB,
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.15)',
                    borderWidth: 2.5,
                    pointBackgroundColor: '#8b5cf6',
                    pointRadius: 4,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    ticks: { font: { size: 11 }, backdropColor: 'transparent' },
                    pointLabels: { font: { size: 13, weight: '600' } },
                    grid: { color: 'rgba(0,0,0,0.08)' },
                    angleLines: { color: 'rgba(0,0,0,0.06)' },
                }
            },
            plugins: {
                legend: { position: 'bottom', labels: { font: { size: 13, weight: '600' }, padding: 20, usePointStyle: true } }
            }
        }
    });
}

/* ── AI-Generated Comparison Summary ────────────────────── */
async function generateAIComparison(a, b) {
    const container = document.getElementById('ai-comparison');
    if (!container) return;

    // Build a rich comparison summary directly from data
    const buildMetricRow = (label, vA, vB, format, lowerBetter) => {
        if (vA == null && vB == null) return '';
        const fA = vA != null ? format(vA) : 'N/A';
        const fB = vB != null ? format(vB) : 'N/A';
        let winner = '';
        if (vA != null && vB != null) {
            if (lowerBetter) winner = vA < vB ? a.symbol : vA > vB ? b.symbol : 'Tie';
            else winner = vA > vB ? a.symbol : vA < vB ? b.symbol : 'Tie';
        }
        return `| ${label} | ${fA} | ${fB} | ${winner} |`;
    };

    const pct = v => v.toFixed(1) + '%';
    const num = v => v.toFixed(1);
    const cur = v => '₹' + Number(v).toLocaleString();

    let scoreA = 0, scoreB = 0;
    const compareMetric = (vA, vB, lowerBetter) => {
        if (vA == null || vB == null) return;
        if (lowerBetter) { if (vA < vB) scoreA++; else if (vB < vA) scoreB++; }
        else { if (vA > vB) scoreA++; else if (vB > vA) scoreB++; }
    };

    compareMetric(a.pe, b.pe, true);
    compareMetric(a.pb, b.pb, true);
    compareMetric(a.roe, b.roe, false);
    compareMetric(a.roce, b.roce, false);
    compareMetric(a.debt_to_equity, b.debt_to_equity, true);
    compareMetric(a.net_profit_margin, b.net_profit_margin, false);
    compareMetric(a.sales_growth, b.sales_growth, false);
    compareMetric(a.profit_growth, b.profit_growth, false);
    compareMetric(a.promoter_holding, b.promoter_holding, false);

    const total = scoreA + scoreB;
    const pctA = total > 0 ? Math.round(scoreA / total * 100) : 50;
    const pctB = total > 0 ? Math.round(scoreB / total * 100) : 50;
    const overall = scoreA > scoreB ? a.symbol : scoreB > scoreA ? b.symbol : 'Both are evenly matched';

    // Build the analysis HTML
    let html = `
        <div style="display:flex; gap:16px; margin-bottom:24px;">
            <div style="flex:1; text-align:center; padding:16px; background:linear-gradient(135deg, rgba(59,130,246,0.06), rgba(59,130,246,0.02)); border-radius:var(--radius-lg); border:1px solid rgba(59,130,246,0.1);">
                <div style="font-size:2rem; font-weight:800; color:#3b82f6;">${scoreA}</div>
                <div style="font-weight:600; color:var(--text);">${a.symbol}</div>
                <div style="font-size:0.8rem; color:var(--text-light);">metrics won</div>
            </div>
            <div style="flex:1; text-align:center; padding:16px; background:linear-gradient(135deg, rgba(139,92,246,0.06), rgba(139,92,246,0.02)); border-radius:var(--radius-lg); border:1px solid rgba(139,92,246,0.1);">
                <div style="font-size:2rem; font-weight:800; color:#8b5cf6;">${scoreB}</div>
                <div style="font-weight:600; color:var(--text);">${b.symbol}</div>
                <div style="font-size:0.8rem; color:var(--text-light);">metrics won</div>
            </div>
        </div>

        <div style="margin-bottom:20px;">
            <div style="font-size:0.8rem; color:var(--text-light); margin-bottom:6px; display:flex; justify-content:space-between;">
                <span>${a.symbol} (${pctA}%)</span>
                <span>${b.symbol} (${pctB}%)</span>
            </div>
            <div style="height:8px; background:var(--gray-100); border-radius:4px; overflow:hidden; display:flex;">
                <div style="width:${pctA}%; background:linear-gradient(90deg, #3b82f6, #60a5fa); transition:width 0.5s ease;"></div>
                <div style="width:${pctB}%; background:linear-gradient(90deg, #8b5cf6, #a78bfa); transition:width 0.5s ease;"></div>
            </div>
        </div>

        <div style="padding:16px; background:var(--bg-alt); border-radius:var(--radius); margin-bottom:20px;">
            <strong>📊 Overall Verdict:</strong> <strong style="color:var(--primary);">${overall}</strong> leads on fundamentals with ${Math.max(scoreA, scoreB)} out of ${total} metrics.
        </div>
    `;

    // Key insights
    html += '<h4 style="margin-bottom:12px; font-size:0.95rem;">Key Insights</h4><ul style="list-style:none; padding:0; margin:0;">';

    if (a.pe != null && b.pe != null) {
        const cheaper = a.pe < b.pe ? a : b;
        html += `<li style="padding:6px 0; border-bottom:1px solid var(--gray-100);">📈 <strong>Valuation:</strong> ${cheaper.symbol} is cheaper at PE ${Number(cheaper.pe).toFixed(1)} vs ${(cheaper === a ? b : a).symbol}'s ${Number(cheaper === a ? b.pe : a.pe).toFixed(1)}</li>`;
    }
    if (a.roe != null && b.roe != null) {
        const better = a.roe > b.roe ? a : b;
        html += `<li style="padding:6px 0; border-bottom:1px solid var(--gray-100);">💰 <strong>Profitability:</strong> ${better.symbol} has higher ROE at ${Number(better.roe).toFixed(1)}% vs ${Number(better === a ? b.roe : a.roe).toFixed(1)}%</li>`;
    }
    if (a.debt_to_equity != null && b.debt_to_equity != null) {
        const safer = a.debt_to_equity < b.debt_to_equity ? a : b;
        html += `<li style="padding:6px 0; border-bottom:1px solid var(--gray-100);">🛡️ <strong>Leverage:</strong> ${safer.symbol} has lower debt (D/E: ${Number(safer.debt_to_equity).toFixed(2)}) — less financial risk</li>`;
    }
    if (a.profit_growth != null && b.profit_growth != null) {
        const grower = a.profit_growth > b.profit_growth ? a : b;
        html += `<li style="padding:6px 0; border-bottom:1px solid var(--gray-100);">🚀 <strong>Growth:</strong> ${grower.symbol} is growing profits faster at ${Number(grower.profit_growth).toFixed(1)}%</li>`;
    }
    if (a.net_profit_margin != null && b.net_profit_margin != null) {
        const efficient = a.net_profit_margin > b.net_profit_margin ? a : b;
        html += `<li style="padding:6px 0;">✅ <strong>Efficiency:</strong> ${efficient.symbol} has better margins at ${Number(efficient.net_profit_margin).toFixed(1)}%</li>`;
    }

    html += '</ul>';

    html += `<div style="margin-top:20px; padding:12px; border-radius:var(--radius); border:1px solid var(--gray-200); font-size:0.8rem; color:var(--text-muted);">
        ⚠️ <em>Disclaimer: This is AI-generated educational information only, not investment advice. Please consult a qualified financial advisor before making investment decisions.</em>
    </div>`;

    container.innerHTML = html;
}

/* ── Event Listeners ─────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    let debounceA, debounceB;

    const inputA = document.getElementById('stock-a-input');
    const inputB = document.getElementById('stock-b-input');

    if (inputA) {
        inputA.addEventListener('input', () => {
            clearTimeout(debounceA);
            debounceA = setTimeout(() => searchStock('stock-a-input', 'stock-a-results'), 300);
        });
    }
    if (inputB) {
        inputB.addEventListener('input', () => {
            clearTimeout(debounceB);
            debounceB = setTimeout(() => searchStock('stock-b-input', 'stock-b-results'), 300);
        });
    }

    // Close results on outside click
    document.addEventListener('click', (e) => {
        ['stock-a-results', 'stock-b-results'].forEach(id => {
            const el = document.getElementById(id);
            if (el && !el.contains(e.target) && !document.getElementById(id.replace('results', 'input'))?.contains(e.target)) {
                el.style.display = 'none';
            }
        });
    });
});
