import os
import glob
import re

# 1. Update existing 11 basic HTML pages with full mega menu string.
html_files = glob.glob(r'd:\WD Lab Project\frontend\pages\*.html')

mega_menu_inner = """
                    <a href="#" class="nav-link active">Calculators ▾</a>
                    <div class="dropdown-menu">
                        <div class="dropdown-grid">
                            <a href="/pages/calculators/sip.html">SIP Calculator</a>
                            <a href="/pages/calculators/brokerage.html">Brokerage Calculator</a>
                            <a href="/pages/calculators/rd.html">RD Calculator</a>
                            <a href="/pages/calculators/hra.html">HRA Calculator</a>
                            <a href="/pages/calculators/home-loan.html">Home Loan EMI Calculator</a>
                            <a href="/pages/calculators/lumpsum.html">Lumpsum Calculator</a>
                            <a href="/pages/calculators/margin.html">Margin Calculator</a>
                            <a href="/pages/calculators/fd.html">FD Calculator</a>
                            <a href="/pages/calculators/swp.html">SWP Calculator</a>
                            <a href="/pages/calculators/epf.html">EPF Calculator</a>
                            <a href="/pages/calculators/tds.html">TDS Calculator</a>
                            <a href="/pages/calculators/income-tax.html">Income Tax Calculator</a>
                            <a href="/pages/calculators/emi.html">EMI Calculator</a>
                            <a href="/pages/calculators/step-up-sip.html">Step-up SIP Calculator</a>
                            <a href="/pages/calculators/ppf.html">PPF Calculator</a>
                            <a href="/pages/calculators/gst.html">GST Calculator</a>
                            <a href="/pages/calculators/car-loan.html">Car Loan Calculator</a>
                        </div>
                    </div>
"""
mega_menu_inner_unactive = mega_menu_inner.replace('active', '')

for f in html_files:
    if not os.path.isfile(f): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # We replace everything inside <div class="nav-item-dropdown"> ... </div> right before Dashboard nav.
    pattern = r'(<div class="nav-item-dropdown">).*?(</div>\s*<a href="/pages/dashboard.html")'
    new_content = re.sub(pattern, r'\1' + mega_menu_inner_unactive + r'\2', content, flags=re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)
    print(f"Updated megamenu in base page {os.path.basename(f)}")

# 2. Extract FULL navbar from index.html to use for 17 calculators
with open(r'd:\WD Lab Project\frontend\pages\index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

# Match the entire <nav class="navbar"> ... </nav>
nav_match = re.search(r'(<nav class="navbar">.*?</nav>)', idx_html, re.DOTALL)
full_navbar = nav_match.group(1) if nav_match else ""
# Make calculators active for inner pages
full_navbar = full_navbar.replace('<a href="#" class="nav-link">Calculators ▾</a>', '<a href="#" class="nav-link active">Calculators ▾</a>')

# 3. Generate 17 calculators with 1fr 1fr grid, full navbar, and usage descriptions
base_dir = r'd:\WD Lab Project\frontend\pages\calculators'
os.makedirs(base_dir, exist_ok=True)

chart_html_template = """
            <section class="calc-details-section" id="chart-section" style="margin-bottom: -10px;">
                <h3>Growth Graph</h3>
                <div class="calc-chart-container" style="position: relative; height: 320px; width: 100%;">
                    <canvas id="growthChart"></canvas>
                </div>
            </section>
"""

common_chart_js = """
        let myChart = null;
        function updateChart(labels, dataset1, dataset2, label1, label2) {
            const ctx = document.getElementById('growthChart');
            if(!ctx) return;
            if (myChart) {
                myChart.data.labels = labels;
                myChart.data.datasets[0].data = dataset1;
                myChart.data.datasets[0].label = label1;
                if(dataset2) {
                    if(myChart.data.datasets.length > 1) {
                        myChart.data.datasets[1].data = dataset2;
                        myChart.data.datasets[1].label = label2;
                    } else {
                        myChart.data.datasets.push({
                            label: label2,
                            data: dataset2,
                            backgroundColor: '#FFE0B2',
                            fill: true,
                            tension: 0.4
                        });
                    }
                } else if(myChart.data.datasets.length > 1) {
                    myChart.data.datasets.pop();
                }
                myChart.update();
            } else {
                let datasets = [{
                    label: label1,
                    data: dataset1,
                    backgroundColor: '#2EC4B6',
                    fill: true,
                    tension: 0.4
                }];
                if (dataset2) {
                    datasets.push({
                        label: label2,
                        data: dataset2,
                        backgroundColor: '#FFE0B2',
                        fill: true,
                        tension: 0.4
                    });
                }
                myChart = new Chart(ctx, {
                    type: 'line',
                    data: { labels: labels, datasets: datasets },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: { mode: 'index', intersect: false },
                        scales: {
                            y: { beginAtZero: true, ticks: { callback: function(value) { return '₹' + (value/100000 > 1 ? (value/100000).toFixed(1) + 'L' : value.toLocaleString('en-IN')); } } },
                            x: { grid: { display: false } }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) { return context.dataset.label + ': ₹' + Math.round(context.raw).toLocaleString('en-IN'); }
                                }
                            }
                        }
                    }
                });
            }
        }
"""

def get_html(title, description, form_html, result_html, script_code, usage_html, has_chart=False):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} Calculator – FinSight</title>
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/calculators.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
    <style>
        .calc-details-section {{ background: var(--bg-alt); padding: 32px; border-radius: var(--radius-lg); margin-top: 40px; border: 1px solid var(--gray-200); }}
        .calc-details-section h3 {{ color: var(--teal); margin-bottom: 16px; font-size: var(--fs-xl); }}
        .calc-details-section p, .calc-details-section li {{ color: var(--text-light); line-height: 1.8; margin-bottom: 8px; font-size: var(--fs-base); }}
        .calc-details-section ul {{ list-style-type: disc; margin-left: 20px; }}
        
        @media (max-width: 768px) {{
            .desktop-grid {{ grid-template-columns: 1fr !important; gap: 24px !important; }}
        }}
    </style>
</head>
<body>
    {full_navbar}

    <div class="page">
        <div class="container" style="padding-top:40px; max-width: 1100px;">
            <div class="page-header text-center">
                <h1>{title} <span class="text-gradient">Calculator</span></h1>
                <p style="font-size: var(--fs-lg); color: var(--text-light); margin-top:12px;">{description}</p>
            </div>

            <div class="calc-panel active" style="display:block">
                <!-- IMPORTANT: 2 Column Desktop Layout -->
                <div class="calc-layout desktop-grid mt-3" style="display:grid; grid-template-columns: 1fr 1fr; gap: 40px;">
                    <div class="calc-form">
                        <h3>Input Details</h3>
                        {form_html}
                    </div>
                    <div class="calc-result">
                        <h3>Results</h3>
                        {result_html}
                    </div>
                </div>
            </div>
            
            {chart_html_template if has_chart else ""}
            
            <section class="calc-details-section">
                <h3>Usage & Details</h3>
                {usage_html}
            </section>
        </div>
    </div>

    <footer class="footer">
        <div class="footer-inner">
            <div class="footer-bottom">© 2026 <span class="text-gradient">FinSight</span>. Educational platform — not investment advice.</div>
        </div>
    </footer>

    <script src="/static/js/main.js"></script>
    <script>
        {common_chart_js if has_chart else ""}
        {script_code}
        
        document.querySelectorAll('input').forEach(input => {{
            input.addEventListener('input', runCalc);
        }});
        document.addEventListener('DOMContentLoaded', runCalc);
        
        function formatCurr(num) {{ return '₹' + Math.round(num).toLocaleString('en-IN'); }}
    </script>
</body>
</html>"""

calcs = [
    {
        "file": "sip.html", "title": "SIP", "desc": "Calculate returns on your Systematic Investment Plan effortlessly with compounding.",
        "form": """<div class="form-group"><label>Monthly Investment (₹)</label><input type="number" id="inp1" value="5000" class="form-input"></div>
        <div class="form-group"><label>Expected Return (%)</label><input type="number" id="inp2" value="12" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="10" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Est. Returns</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>""",
        "usage": """<p>A Systematic Investment Plan (SIP) allows you to invest a fixed amount regularly into a mutual fund. This calculator uses compound interest to project your future wealth based on your monthly investment and expected growth rate.</p>
        <ul><li><strong>Monthly Investment:</strong> The dedicated amount you commit to investing every month.</li><li><strong>Expected Return:</strong> Conservative long term equity estimates range from 10-12%.</li><li><strong>Time Period:</strong> The power of compounding shines brightest across 10+ year horizons.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value) / 1200; let n = Number(document.getElementById('inp3').value); let totalMonths = n * 12; let invested = P * totalMonths; let total = P * (((1 + r)**totalMonths - 1) / r) * (1 + r); document.getElementById('res1').innerText = formatCurr(invested); document.getElementById('res2').innerText = formatCurr(total - invested); document.getElementById('res3').innerText = formatCurr(total); let labels=[]; let invData=[]; let totData=[]; let curInv=0; let curTot=0; for(let i=1;i<=n;i++){ curInv+=P*12; curTot = curTot * Math.pow(1+r, 12) + (P * (((1 + r)**12 - 1) / r) * (1 + r)); labels.push(i+'Y'); invData.push(curInv); totData.push(curTot); } updateChart(labels, invData, totData, 'Invested', 'Total Value'); }",
        "chart": True
    },
    {
        "file": "step-up-sip.html", "title": "Step-up SIP", "desc": "Calculate growth on SIPs where you increase your monthly contribution annually.",
        "form": """<div class="form-group"><label>Initial Monthly Investment (₹)</label><input type="number" id="inp1" value="5000" class="form-input"></div>
        <div class="form-group"><label>Annual Step-up (%)</label><input type="number" id="step" value="10" class="form-input"></div>
        <div class="form-group"><label>Expected Return (%)</label><input type="number" id="inp2" value="12" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="10" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Est. Returns</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>""",
        "usage": """<p>As your income grows, your investments should too. A Step-up SIP automatically increases your monthly contribution by a set percentage each year, drastically boosting your final corpus.</p>
        <ul><li><strong>Annual Step-up:</strong> The percentage by which you increase your monthly SIP every year (e.g., matching a 10% salary hike).</li><li><strong>Impact:</strong> Even a modest 10% annual step-up can double your final returns compared to a flat SIP.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let step = 1 + (Number(document.getElementById('step').value) / 100); let r = Number(document.getElementById('inp2').value) / 1200; let n = Number(document.getElementById('inp3').value); let invested=0; let total=0; let labels=[]; let invData=[]; let totData=[]; let initP = P; for(let i=1; i<=n; i++){ for(let j=0; j<12; j++){ invested += initP; total = (total + initP) * (1+r); } labels.push(i+'Y'); invData.push(invested); totData.push(total); initP *= step; } document.getElementById('res1').innerText = formatCurr(invested); document.getElementById('res2').innerText = formatCurr(total - invested); document.getElementById('res3').innerText = formatCurr(total); updateChart(labels, invData, totData, 'Invested', 'Total Value'); }",
        "chart": True
    },
    {
        "file": "lumpsum.html", "title": "Lumpsum", "desc": "Estimate the wealth generated from a one-time capital deployment.",
        "form": """<div class="form-group"><label>Investment Amount (₹)</label><input type="number" id="inp1" value="100000" class="form-input"></div>
        <div class="form-group"><label>Expected Return (%)</label><input type="number" id="inp2" value="12" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="10" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Est. Returns</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>""",
        "usage": """<p>A lumpsum investment is when you invest a significant amount of money in one go, rather than staggering it over time. This exposes the entire capital to compounding immediately.</p>
        <ul><li>Best used when you receive a large bonus, unexpected windfall, or inheritance.</li><li>Keep an eye on market valuations; investing a huge lumpsum right before a crash can impact short-term returns.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value)/100; let n = Number(document.getElementById('inp3').value); let total = P * Math.pow(1+r, n); document.getElementById('res1').innerText = formatCurr(P); document.getElementById('res2').innerText = formatCurr(total - P); document.getElementById('res3').innerText = formatCurr(total); let labels=[]; let invData=[]; let totData=[]; for(let i=0; i<=n; i++){ labels.push(i+'Y'); invData.push(P); totData.push(P * Math.pow(1+r, i)); } updateChart(labels, invData, totData, 'Invested', 'Total Value'); }",
        "chart": True
    },
    {
        "file": "fd.html", "title": "Fixed Deposit (FD)", "desc": "Calculate guaranteed returns compounded quarterly.",
        "form": """<div class="form-group"><label>Total Investment (₹)</label><input type="number" id="inp1" value="100000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (% P.A.)</label><input type="number" id="inp2" value="7.5" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="5" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Interest Earned</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>""",
        "usage": """<p>Fixed Deposits (FDs) are safe, guaranteed-return instruments offered by banks and NBFCs. Unlike stocks, your principal is secure and insured up to ₹5 Lakhs.</p>
        <ul><li><strong>Compounding:</strong> Banks generally calculate FD interest using quarterly compounding, which results in slightly higher yields than advertised.</li><li><strong>Taxation:</strong> Interest earned is entirely taxable at your income tax slab rate.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value)/100; let n = Number(document.getElementById('inp3').value); let total = P * Math.pow(1+r/4, 4*n); document.getElementById('res1').innerText = formatCurr(P); document.getElementById('res2').innerText = formatCurr(total - P); document.getElementById('res3').innerText = formatCurr(total); let labels=[]; let invData=[]; let totData=[]; for(let i=0; i<=n; i++){ labels.push(i+'Y'); invData.push(P); totData.push(P * Math.pow(1+r/4, 4*i)); } updateChart(labels, invData, totData, 'Invested Amount', 'Total Value'); }",
        "chart": True
    },
    {
        "file": "rd.html", "title": "Recurring Deposit (RD)", "desc": "Project maturity values for your monthly scheduled deposits.",
        "form": """<div class="form-group"><label>Monthly Investment (₹)</label><input type="number" id="inp1" value="5000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (% P.A.)</label><input type="number" id="inp2" value="7" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="5" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Interest Earned</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>""",
        "usage": """<p>A Recurring Deposit behaves like an automated savings account. Instead of requiring a large lumpsum, you deposit a fixed monthly amount which compounds at a fixed rate.</p>
        <ul><li>Interest is typically compounded quarterly.</li><li>Safe, predictable way to save for short-term goals securely.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value)/400; let years = Number(document.getElementById('inp3').value); let months = years*12; let invested = P * months; let total=0; let labels=[]; let invData=[]; let totData=[]; for(let i=1; i<=months; i++){ total+=P; if(i%3===0) total += total*r; if(i%12===0) { labels.push((i/12)+'Y'); invData.push(P*i); totData.push(total); } } document.getElementById('res1').innerText = formatCurr(invested); document.getElementById('res2').innerText = formatCurr(total - invested); document.getElementById('res3').innerText = formatCurr(total); updateChart(labels, invData, totData, 'Invested Amount', 'Total Value'); }",
        "chart": True
    },
    {
        "file": "ppf.html", "title": "Public Provident Fund (PPF)", "desc": "Calculate your maturity value for this tax-exempt government scheme.",
        "form": """<div class="form-group"><label>Yearly Investment (₹)</label><input type="number" id="inp1" value="150000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (%)</label><input type="number" id="inp2" value="7.1" class="form-input" readonly></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="15" class="form-input" min="15"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Interest Earned</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Maturity</div></div>
        </div>""",
        "usage": """<p>The PPF is one of India's most popular long-term savings schemes backed by the Govt. of India, offering attractive interest rates and unmatched tax benefits under the EEE regime.</p>
        <ul><li><strong>Lock-in:</strong> Strict 15-year maturity lock-in, with limited partial withdrawal options post 7 years.</li><li><strong>Taxation:</strong> EEE status meaning the investment, accrued interest, and maturity amount are entirely tax-free.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value)/100; let y = Number(document.getElementById('inp3').value); let invested=0; let total=0; let labels=[]; let invData=[]; let totData=[]; for(let i=1;i<=y;i++){ total+=P; invested+=P; total+=total*r; labels.push(i+'Y'); invData.push(invested); totData.push(total); } document.getElementById('res1').innerText = formatCurr(invested); document.getElementById('res2').innerText = formatCurr(total - invested); document.getElementById('res3').innerText = formatCurr(total); updateChart(labels, invData, totData, 'Invested Amount', 'Total Value'); }",
        "chart": True
    },
    {
        "file": "epf.html", "title": "Employee Provident Fund (EPF)", "desc": "Project your retirement corpus relying on employer + employee contributions.",
        "form": """<div class="form-group"><label>Basic Salary (₹/month)</label><input type="number" id="inp1" value="50000" class="form-input"></div>
        <div class="form-group"><label>Employee Cont. (%)</label><input type="number" id="inp2" value="12" class="form-input" readonly></div>
        <div class="form-group"><label>Employer Cont. (%)</label><input type="number" id="inp4" value="3.67" class="form-input" readonly></div>
        <div class="form-group"><label>Years to Retirement</label><input type="number" id="inp3" value="25" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Your Contrib.</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Employer Contrib.</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Retirement Fund</div></div>
        </div>""",
        "usage": """<p>The EPF is a mandatory retirement savings scheme for salaried employees working in registered companies. Both you and your employer deposit a chunk to fund your retirement.</p>
        <ul><li><strong>Rates:</strong> You contribute 12% of Basic. Employers contribute 12% (3.67% to EPF, 8.33% to EPS pension).</li><li><strong>Interest:</strong> Set annually by the EPFO (currently ~8.15% to 8.25%).</li></ul>""",
        "js": "function runCalc() { let basic = Number(document.getElementById('inp1').value); let years = Number(document.getElementById('inp3').value); let r = 8.15/100; let e1 = basic * 0.12; let e2 = basic * 0.0367; let te=0; let tem=0; let f=0; let labels=[]; let empData=[]; let totData=[]; for(let i=1; i<=years*12; i++){ te+=e1; tem+=e2; f+=(e1+e2); if(i%12===0) { f+=f*r; labels.push((i/12)+'Y'); empData.push(te); totData.push(f); } } document.getElementById('res1').innerText = formatCurr(te); document.getElementById('res2').innerText = formatCurr(tem); document.getElementById('res3').innerText = formatCurr(f); updateChart(labels, empData, totData, 'Your Contribution', 'Total Fund'); }",
        "chart": True
    },
    {
        "file": "emi.html", "title": "EMI", "desc": "Calculate Equated Monthly Installment and total interest for loans.",
        "form": """<div class="form-group"><label>Loan Amount (₹)</label><input type="number" id="inp1" value="1000000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (% P.A.)</label><input type="number" id="inp2" value="8.5" class="form-input"></div>
        <div class="form-group"><label>Loan Tenure (Years)</label><input type="number" id="inp3" value="5" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Monthly EMI</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Total Interest</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Payment</div></div>
        </div>""",
        "usage": """<p>An EMI is a fixed amount paid by a borrower to a lender at a specified date each calendar month. EMIs are applied to both interest and principal each month.</p>
        <ul><li><strong>Principal Reduction:</strong> Initially, a large portion of your EMI goes towards covering the interest, while principal declines very slowly.</li><li>Avoid extremely long tenures for personal loans, as total interest inflates rapidly.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value)/1200; let years = Number(document.getElementById('inp3').value); let n = years*12; let emi = P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1); document.getElementById('res1').innerText=formatCurr(emi); document.getElementById('res2').innerText=formatCurr((emi*n)-P); document.getElementById('res3').innerText=formatCurr(emi*n); let labels=[]; let prinData=[]; let intData=[]; let bal=P; let totPaid=0; let prinPaid=0; for(let i=1; i<=n; i++){ let intP = bal*r; let prinP = emi - intP; bal -= prinP; prinPaid += prinP; totPaid += emi; if(i%12===0 || i===n){ labels.push((i/12).toFixed(1)+'Y'); prinData.push(prinPaid); intData.push(totPaid); } } updateChart(labels, prinData, intData, 'Principal Paid', 'Total Paid'); }",
        "chart": True
    },
    {
        "file": "home-loan.html", "title": "Home Loan EMI", "desc": "Calculate your Home Loan EMI, factoring in major capital commitments.",
        "form": """<div class="form-group"><label>Home Loan Amount (₹)</label><input type="number" id="inp1" value="5000000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (% P.A.)</label><input type="number" id="inp2" value="8.5" class="form-input"></div>
        <div class="form-group"><label>Loan Tenure (Years)</label><input type="number" id="inp3" value="20" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Monthly EMI</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Total Interest</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Payment</div></div>
        </div>""",
        "usage": """<p>Home Loans represent the largest debt most individuals take. A tiny change in interest rates or a minor prepayment can shave off years of EMI burdens.</p>
        <ul><li><strong>Tax Benefits:</strong> You can claim up to ₹1.5L against principal (Sec 80C) and ₹2L against interest (Sec 24).</li><li><strong>Variable Rates:</strong> Home loans frequently use floating rates which move with repo rate hikes.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value)/1200; let years = Number(document.getElementById('inp3').value); let n = years*12; let emi = P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1); document.getElementById('res1').innerText=formatCurr(emi); document.getElementById('res2').innerText=formatCurr((emi*n)-P); document.getElementById('res3').innerText=formatCurr(emi*n); let labels=[]; let prinData=[]; let intData=[]; let bal=P; let totPaid=0; let prinPaid=0; for(let i=1; i<=n; i++){ let intP = bal*r; let prinP = emi - intP; bal -= prinP; prinPaid += prinP; totPaid += emi; if(i%12===0 || i===n){ labels.push((i/12).toFixed(1)+'Y'); prinData.push(prinPaid); intData.push(totPaid); } } updateChart(labels, prinData, intData, 'Principal Paid', 'Total Paid'); }",
        "chart": True
    },
    {
        "file": "car-loan.html", "title": "Car Loan EMI", "desc": "Estimate monthly obligations for your vehicle financing.",
        "form": """<div class="form-group"><label>Car Loan Amount (₹)</label><input type="number" id="inp1" value="800000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (% P.A.)</label><input type="number" id="inp2" value="9" class="form-input"></div>
        <div class="form-group"><label>Loan Tenure (Years)</label><input type="number" id="inp3" value="5" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Monthly EMI</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Total Interest</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Payment</div></div>
        </div>""",
        "usage": """<p>Car loans facilitate purchasing an automobile while spreading the cost over 1-7 years. Cars are depreciating assets, which means their value plummets over the loan's span.</p>
        <ul><li>Interest rates on vehicles are typically higher than home loans as the collateral shrinks in value over time.</li><li>Beware zero-percent financing schemes spanning longer terms as they usually lock out potential cash discounts.</li></ul>""",
        "js": "function runCalc() { let P = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value)/1200; let years = Number(document.getElementById('inp3').value); let n = years*12; let emi = P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1); document.getElementById('res1').innerText=formatCurr(emi); document.getElementById('res2').innerText=formatCurr((emi*n)-P); document.getElementById('res3').innerText=formatCurr(emi*n); let labels=[]; let prinData=[]; let intData=[]; let bal=P; let totPaid=0; let prinPaid=0; for(let i=1; i<=n; i++){ let intP = bal*r; let prinP = emi - intP; bal -= prinP; prinPaid += prinP; totPaid += emi; if(i%12===0 || i===n){ labels.push((i/12).toFixed(1)+'Y'); prinData.push(prinPaid); intData.push(totPaid); } } updateChart(labels, prinData, intData, 'Principal Paid', 'Total Paid'); }",
        "chart": True
    },
    {
        "file": "swp.html", "title": "Systematic Withdrawal Plan (SWP)", "desc": "Simulate generating monthly passive income from a parked corpus.",
        "form": """<div class="form-group"><label>Total Investment (₹)</label><input type="number" id="inp1" value="5000000" class="form-input"></div>
        <div class="form-group"><label>Withdrawal per month (₹)</label><input type="number" id="inp2" value="25000" class="form-input"></div>
        <div class="form-group"><label>Expected Return (%)</label><input type="number" id="inp3" value="10" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp4" value="10" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Total Withdrawn</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Final Corpus Value</div></div>
        </div>""",
        "usage": """<p>A Systematic Withdrawal Plan (SWP) allows you to draw down from your investments securely, ensuring a steady stream of income (especially post-retirement). This acts identically to a reverse SIP.</p>
        <ul><li><strong>Sustainability:</strong> The key to an SWP is ensuring your withdrawal rate is lower than the expected return minus inflation.</li><li>Taxation on SWP is highly efficient as you only pay tax on the capital gains proportion, not the principal returned.</li></ul>""",
        "js": "function runCalc() { let fund = Number(document.getElementById('inp1').value); let w = Number(document.getElementById('inp2').value); let r = Number(document.getElementById('inp3').value)/1200; let years = Number(document.getElementById('inp4').value); let n = years*12; let tw=0; let labels=[]; let fundData=[]; let twData=[]; for(let i=1;i<=n;i++){ fund = fund*(1+r) - w; tw+=w; if(i%12===0){ labels.push((i/12)+'Y'); fundData.push(Math.max(0,fund)); twData.push(tw); } if(fund <= 0 && i%12!==0) { labels.push((i/12).toFixed(1)+'Y'); fundData.push(0); twData.push(tw); break; } } document.getElementById('res1').innerText=formatCurr(tw); document.getElementById('res3').innerText=formatCurr(Math.max(0,fund)); updateChart(labels, fundData, null, 'Remaining Corpus', null); }",
        "chart": True
    },
    {
        "file": "margin.html", "title": "Margin Calculator", "desc": "Determine the leverage capital required to initiate a trading position.",
        "form": """<div class="form-group"><label>Instrument Price (₹)</label><input type="number" id="inp1" value="2500" class="form-input"></div>
        <div class="form-group"><label>Quantity</label><input type="number" id="inp2" value="100" class="form-input"></div>
        <div class="form-group"><label>Margin Requirement (%)</label><input type="number" id="inp3" value="20" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Total Contract Value</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Required Margin</div></div>
        </div>""",
        "usage": """<p>Trading on Margin enables you to buy/sell assets while depositing only a fraction of the total trade value. Commonly used for Intraday (MIS) setups and Futures & Options trading.</p>
        <ul><li>Brokers mandate an upfront Initial Margin defined by the exchange.</li><li>Leveraging magnifies both your potential profits, <i>and</i> your potential losses. Please manage risk accordingly.</li></ul>""",
        "js": "function runCalc() { let p = Number(document.getElementById('inp1').value); let q = Number(document.getElementById('inp2').value); let m = Number(document.getElementById('inp3').value)/100; let total = p*q; document.getElementById('res1').innerText=formatCurr(total); document.getElementById('res2').innerText=formatCurr(total*m); }"
    },
    {
        "file": "brokerage.html", "title": "Brokerage", "desc": "Deconstruct trading fees to establish your exact Net Profit/Loss.",
        "form": """<div class="form-group"><label>Buy Price (₹)</label><input type="number" id="inp1" value="100" class="form-input"></div>
        <div class="form-group"><label>Sell Price (₹)</label><input type="number" id="inp2" value="110" class="form-input"></div>
        <div class="form-group"><label>Quantity</label><input type="number" id="inp3" value="500" class="form-input"></div>
        <div class="form-group"><label>Brokerage Charge (₹ per order)</label><input type="number" id="inp4" value="20" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Total Brokerage (Flat)</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="gross">—</div><div class="calc-stat-label">Gross P/L</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Net Profit / Loss</div></div>
        </div>""",
        "usage": """<p>Brokerage, STT, Exchange transaction charges, SEBI turnover fees, and GST can severely eat into the profits of high-frequency day traders.</p>
        <ul><li><strong>Discount Brokers:</strong> Typically charge a flat rate of ₹20 per trade (or 0.05%, whichever is lower) on intraday orders.</li><li>Ensure your profit margins surpass the break-even ceiling created by accumulated taxes and brokerage.</li></ul>""",
        "js": "function runCalc() { let b=Number(document.getElementById('inp1').value); let s=Number(document.getElementById('inp2').value); let q=Number(document.getElementById('inp3').value); let f=Number(document.getElementById('inp4').value)*2; let gross=(s-b)*q; document.getElementById('res1').innerText=formatCurr(f); document.getElementById('gross').innerText=formatCurr(gross); document.getElementById('res2').innerText=formatCurr(gross-f); }"
    },
    {
        "file": "gst.html", "title": "Goods and Services Tax (GST)", "desc": "Quickly extract or append GST slabs to item prices.",
        "form": """<div class="form-group"><label>Original Price (₹)</label><input type="number" id="inp1" value="1000" class="form-input"></div>
        <div class="form-group"><label>GST Rate (%)</label><input type="number" id="inp2" value="18" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">GST Tax Amount</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Final Checkout Price</div></div>
        </div>""",
        "usage": """<p>GST is an indirect tax applied broadly on consumer items, services, software, and commodities globally. India utilizes a 4-tier slab: 5%, 12%, 18%, and 28%.</p>
        <ul><li>If calculating backward from an already GST-inclusive price: <code>Tax = (Inclusive Price * Rate)/(100 + Rate)</code>.</li></ul>""",
        "js": "function runCalc() { let p = Number(document.getElementById('inp1').value); let gst = Number(document.getElementById('inp2').value)/100; let tax = p*gst; document.getElementById('res1').innerText=formatCurr(tax); document.getElementById('res2').innerText=formatCurr(p+tax); }"
    },
    {
        "file": "tds.html", "title": "Tax Deducted at Source (TDS)", "desc": "Estimate the withholding tax executed by the deductor before disbursing payments.",
        "form": """<div class="form-group"><label>Payment Amount (₹)</label><input type="number" id="inp1" value="50000" class="form-input"></div>
        <div class="form-group"><label>Applicable TDS Rate (%)</label><input type="number" id="inp2" value="10" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">TDS Deducted</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Final Payout Receieved</div></div>
        </div>""",
        "usage": """<p>TDS mandates employers, clients, or banks to aggressively deduct taxes upfront before rolling out a scheduled transaction to you. This reduces tax evasion and shores govt revenue early.</p>
        <ul><li><strong>Common Rates:</strong> Interest on securities (10%), Professional Fees (10%), Winnings from lottery/games (30%).</li><li>You must file your Income Tax Returns (ITR) to claim a refund if your actual tax liability is lower than the TDS withheld.</li></ul>""",
        "js": "function runCalc() { let p = Number(document.getElementById('inp1').value); let r = Number(document.getElementById('inp2').value)/100; let tds = p*r; document.getElementById('res1').innerText=formatCurr(tds); document.getElementById('res2').innerText=formatCurr(p-tds); }"
    },
    {
        "file": "income-tax.html", "title": "Income Tax", "desc": "Estimate your aggregate income tax liabilities (Simplified New Tax Regime).",
        "form": """<div class="form-group"><label>Total Annual Income (₹)</label><input type="number" id="inp1" value="1200000" class="form-input"></div>
        <div class="form-group"><label>Standard Deduction (₹)</label><input type="number" id="inp2" value="75000" class="form-input" readonly></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Taxable Income</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Estimated Baseline Tax</div></div>
        </div>""",
        "usage": """<p>Calculate your annual income tax following the modernized simplified New Regime brackets (applicable for FY 2024-25).</p>
        <ul><li><strong>Tiers:</strong> Income up to ₹3L is entirely exempt. Thereafter, tax rates climb at 5% intervals.</li><li><strong>Rebate:</strong> Complete tax rebate applies heavily if your taxable income stays under ₹12 Lakhs (thus resulting in zero final tax under Section 87A).</li><li><i>Note: Educational Cess (4%) and Surcharges haven't been factored in this fundamental baseline output.</i></li></ul>""",
        "js": "function runCalc() { let inc = Number(document.getElementById('inp1').value); let tax_inc = Math.max(0, inc - 75000); let tax = 0; if(tax_inc > 300000){ let slabs = [ {limit: 400000, rate: 0.00}, {limit: 800000, rate: 0.05}, {limit: 1200000, rate: 0.10}, {limit: 1600000, rate: 0.15}, {limit: 2000000, rate: 0.20}, {limit: 2400000, rate: 0.25}, {limit: Infinity, rate: 0.30} ]; let prev=300000; for(let s of slabs){ if(tax_inc > prev){ let amt = Math.min(tax_inc, s.limit) - prev; tax += amt * s.rate; prev = s.limit; } } } if(tax_inc <= 1200000) tax = 0; document.getElementById('res1').innerText=formatCurr(tax_inc); document.getElementById('res2').innerText=formatCurr(tax); }"
    },
    {
        "file": "hra.html", "title": "House Rent Allowance (HRA)", "desc": "Deterimne your legally tax-exempt HRA footprint.",
        "form": """<div class="form-group"><label>Basic Salary + DA (Yearly ₹)</label><input type="number" id="inp1" value="500000" class="form-input"></div>
        <div class="form-group"><label>HRA Provided by Employer (Yearly ₹)</label><input type="number" id="inp2" value="200000" class="form-input"></div>
        <div class="form-group"><label>Total Actual Rent Paid (Yearly ₹)</label><input type="number" id="inp3" value="180000" class="form-input"></div>""",
        "res": """<div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Exempted HRA (Tax-Free)</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Taxable HRA</div></div>
        </div>""",
        "usage": """<p>HRA comprises a vital element bridging your Gross Salary parameters. If you live in a rented accommodation, you can significantly trim your tax liability under the Old Regime using HRA exception calculations.</p>
        <ul><li><strong>The Exemption Math:</strong> HRA relief defaults to the <i>least</i> of: <br>1. Actual HRA Received.<br>2. 50% Basic (Metro cities) or 40% (Non-Metro).<br>3. Rent Paid strictly minus 10% of Basic Salary.</li><li><i>Note: You cannot aggressively claim HRA if you do not reside in actual rented spaces paying documented rent.</i></li></ul>""",
        "js": "function runCalc() { let basic = Number(document.getElementById('inp1').value); let hra = Number(document.getElementById('inp2').value); let rent = Number(document.getElementById('inp3').value); let cond1 = hra; let cond2 = Math.max(0, rent - (0.10 * basic)); let cond3 = 0.50 * basic; let exempt = Math.min(cond1, cond2, cond3); document.getElementById('res1').innerText = formatCurr(exempt); document.getElementById('res2').innerText = formatCurr(hra - exempt); }"
    }
]

for c in calcs:
    with open(os.path.join(base_dir, c["file"]), 'w', encoding='utf-8') as f:
        f.write(get_html(c["title"], c["desc"], c["form"], c["res"], c["js"], c["usage"], c.get("chart", False)))
        print(f"Generated complete calculator {c['file']}")

print("All Mega Menu Updates and 17 Calculator Designs deployed perfectly.")
