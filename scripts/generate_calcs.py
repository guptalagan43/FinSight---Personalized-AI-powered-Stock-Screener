import os

base_dir = r'd:\WD Lab Project\frontend\pages\calculators'
os.makedirs(base_dir, exist_ok=True)

# Shared HTML structure
def get_html(title, description, form_html, result_html, script_code):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} – FinSight</title>
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/calculators.css">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-inner">
            <a href="/" class="navbar-brand"><span class="logo-dot"></span> <span class="brand-text">Fin<span class="text-gradient">Sight</span></span></a>
            <div class="navbar-nav">
                <a href="/" class="nav-link">Home</a>
                <a href="/pages/screeners.html" class="nav-link">Screeners</a>
                <a href="/pages/sectors.html" class="nav-link">Sectors</a>
                <div class="nav-item-dropdown">
                    <a href="#" class="nav-link active">Calculators ▾</a>
                    <div class="dropdown-menu">
                        <div class="dropdown-grid">
                            <a href="/pages/calculators/sip.html">SIP</a>
                            <a href="/pages/calculators/brokerage.html">Brokerage</a>
                            <a href="/pages/calculators/rd.html">RD</a>
                            <a href="/pages/calculators/hra.html">HRA</a>
                            <a href="/pages/calculators/home-loan.html">Home Loan EMI</a>
                            <a href="/pages/calculators/lumpsum.html">Lumpsum</a>
                            <a href="/pages/calculators/margin.html">Margin</a>
                            <a href="/pages/calculators/fd.html">FD</a>
                            <a href="/pages/calculators/swp.html">SWP</a>
                            <a href="/pages/calculators/epf.html">EPF</a>
                            <a href="/pages/calculators/tds.html">TDS</a>
                            <a href="/pages/calculators/income-tax.html">Income Tax</a>
                            <a href="/pages/calculators/emi.html">EMI</a>
                            <a href="/pages/calculators/step-up-sip.html">Step-up SIP</a>
                            <a href="/pages/calculators/ppf.html">PPF</a>
                            <a href="/pages/calculators/gst.html">GST</a>
                            <a href="/pages/calculators/car-loan.html">Car Loan</a>
                        </div>
                    </div>
                </div>
                <a href="/pages/dashboard.html" class="nav-link">Dashboard</a>
            </div>
            <div class="navbar-actions">
                <button class="theme-toggle" onclick="toggleTheme()">🌙</button>
            </div>
        </div>
    </nav>

    <div class="page">
        <div class="container" style="padding-top:32px; max-width: 900px;">
            <div class="page-header text-center">
                <h1>{title} <span class="text-gradient">Calculator</span></h1>
                <p>{description}</p>
            </div>

            <div class="calc-panel active" style="display:block">
                <div class="calc-layout mt-3" style="grid-template-columns: 1fr; gap: 40px;">
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
        </div>
    </div>

    <footer class="footer">
        <div class="footer-inner">
            <div class="footer-bottom">© 2026 <span class="text-gradient">FinSight</span>. Educational platform — not investment advice.</div>
        </div>
    </footer>

    <script src="/static/js/main.js"></script>
    <script>
        {script_code}
        
        // Auto-run calculator on load and input change
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
        "file": "sip.html", "title": "SIP", "desc": "Calculate returns on your Systematic Investment Plan",
        "form": """
        <div class="form-group"><label>Monthly Investment (₹)</label><input type="number" id="inp1" value="5000" class="form-input"></div>
        <div class="form-group"><label>Expected Return (%)</label><input type="number" id="inp2" value="12" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="10" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Est. Returns</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / (12 * 100);
            let n = Number(document.getElementById('inp3').value) * 12;
            let invested = P * n;
            let total = P * (((1 + r)**n - 1) / r) * (1 + r);
            document.getElementById('res1').innerText = formatCurr(invested);
            document.getElementById('res2').innerText = formatCurr(total - invested);
            document.getElementById('res3').innerText = formatCurr(total);
        }
        """
    },
    {
        "file": "step-up-sip.html", "title": "Step-up SIP", "desc": "Calculate returns with an annually increasing SIP",
        "form": """
        <div class="form-group"><label>Initial Monthly Investment (₹)</label><input type="number" id="inp1" value="5000" class="form-input"></div>
        <div class="form-group"><label>Annual Step-up (%)</label><input type="number" id="step" value="10" class="form-input"></div>
        <div class="form-group"><label>Expected Return (%)</label><input type="number" id="inp2" value="12" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="10" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Est. Returns</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let step = Number(document.getElementById('step').value) / 100;
            let r = Number(document.getElementById('inp2').value) / (12 * 100);
            let years = Number(document.getElementById('inp3').value);
            let invested = 0; let total = 0;
            for(let y=1; y<=years; y++) {
                for(let m=1; m<=12; m++) {
                    invested += P;
                    total = (total + P) * (1 + r);
                }
                P += P * step;
            }
            document.getElementById('res1').innerText = formatCurr(invested);
            document.getElementById('res2').innerText = formatCurr(total - invested);
            document.getElementById('res3').innerText = formatCurr(total);
        }
        """
    },
    {
        "file": "lumpsum.html", "title": "Lumpsum", "desc": "Calculate returns on a one-time investment",
        "form": """
        <div class="form-group"><label>Investment Amount (₹)</label><input type="number" id="inp1" value="100000" class="form-input"></div>
        <div class="form-group"><label>Expected Return (%)</label><input type="number" id="inp2" value="12" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="10" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Est. Returns</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / 100;
            let n = Number(document.getElementById('inp3').value);
            let total = P * Math.pow((1 + r), n);
            document.getElementById('res1').innerText = formatCurr(P);
            document.getElementById('res2').innerText = formatCurr(total - P);
            document.getElementById('res3').innerText = formatCurr(total);
        }
        """
    },
    {
        "file": "fd.html", "title": "Fixed Deposit (FD)", "desc": "Calculate returns on your Fixed Deposit",
        "form": """
        <div class="form-group"><label>Total Investment (₹)</label><input type="number" id="inp1" value="100000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (%)</label><input type="number" id="inp2" value="7.5" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="5" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Interest Earned</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / 100;
            let n = Number(document.getElementById('inp3').value);
            let total = P * Math.pow((1 + r/4), 4*n); // Quarterly compounding standard for FDs
            document.getElementById('res1').innerText = formatCurr(P);
            document.getElementById('res2').innerText = formatCurr(total - P);
            document.getElementById('res3').innerText = formatCurr(total);
        }
        """
    },
    {
        "file": "rd.html", "title": "Recurring Deposit (RD)", "desc": "Calculate returns on your Recurring Deposit",
        "form": """
        <div class="form-group"><label>Monthly Investment (₹)</label><input type="number" id="inp1" value="5000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (%)</label><input type="number" id="inp2" value="7" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="5" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Interest Earned</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Value</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / 100;
            let years = Number(document.getElementById('inp3').value);
            let n = years * 12; // total months
            let total = 0;
            for(let i=0; i<n; i++) {
                total += P;
                total += total * (r/12); // monthly compounding approx for simplicity
            }
            let invested = P * n;
            document.getElementById('res1').innerText = formatCurr(invested);
            document.getElementById('res2').innerText = formatCurr(total - invested);
            document.getElementById('res3').innerText = formatCurr(total);
        }
        """
    },
    {
        "file": "ppf.html", "title": "Public Provident Fund (PPF)", "desc": "Calculate PPF maturity over 15+ years",
        "form": """
        <div class="form-group"><label>Yearly Investment (₹)</label><input type="number" id="inp1" value="150000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (%)</label><input type="number" id="inp2" value="7.1" class="form-input" readonly></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp3" value="15" class="form-input" min="15"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Invested Amount</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Interest Earned</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Maturity</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / 100;
            let years = Number(document.getElementById('inp3').value);
            let total = 0; let invested = 0;
            for(let i=0; i<years; i++) {
                total += P; invested += P;
                total += total * r;
            }
            document.getElementById('res1').innerText = formatCurr(invested);
            document.getElementById('res2').innerText = formatCurr(total - invested);
            document.getElementById('res3').innerText = formatCurr(total);
        }
        """
    },
    {
        "file": "epf.html", "title": "Employee Provident Fund (EPF)", "desc": "Calculate your EPF balance at retirement",
        "form": """
        <div class="form-group"><label>Basic Salary + DA (₹/month)</label><input type="number" id="inp1" value="50000" class="form-input"></div>
        <div class="form-group"><label>Employee Contribution (%)</label><input type="number" id="inp2" value="12" class="form-input" readonly></div>
        <div class="form-group"><label>Employer Contribution (%)</label><input type="number" id="inp4" value="3.67" class="form-input" readonly></div>
        <div class="form-group"><label>Years to Retirement</label><input type="number" id="inp3" value="25" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Your Contribution</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Employer Contribution</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Fund</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let basic = Number(document.getElementById('inp1').value);
            let years = Number(document.getElementById('inp3').value);
            let r = 8.15 / 100;
            let emp_monthly = basic * 0.12;
            let emplyr_monthly = basic * 0.0367;
            let total_emp = 0, total_emplyr = 0, fund = 0;
            
            for(let i=0; i<years*12; i++) {
                total_emp += emp_monthly;
                total_emplyr += emplyr_monthly;
                fund += (emp_monthly + emplyr_monthly);
                if (i % 12 === 11) fund += fund * r; // yearly compounding
            }
            document.getElementById('res1').innerText = formatCurr(total_emp);
            document.getElementById('res2').innerText = formatCurr(total_emplyr);
            document.getElementById('res3').innerText = formatCurr(fund);
        }
        """
    },
    {
        "file": "emi.html", "title": "EMI Calculator", "desc": "Calculate Equated Monthly Installment for loans",
        "form": """
        <div class="form-group"><label>Loan Amount (₹)</label><input type="number" id="inp1" value="1000000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (% P.A.)</label><input type="number" id="inp2" value="8.5" class="form-input"></div>
        <div class="form-group"><label>Loan Tenure (Years)</label><input type="number" id="inp3" value="5" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Monthly EMI</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Total Interest</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Payment</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / (12 * 100);
            let n = Number(document.getElementById('inp3').value) * 12;
            let emi = P * r * Math.pow(1+r, n) / (Math.pow(1+r, n) - 1);
            let totalPayment = emi * n;
            document.getElementById('res1').innerText = formatCurr(emi);
            document.getElementById('res2').innerText = formatCurr(totalPayment - P);
            document.getElementById('res3').innerText = formatCurr(totalPayment);
        }
        """
    },
    {
        "file": "home-loan.html", "title": "Home Loan EMI", "desc": "Calculate your Home Loan EMI options",
        "form": """
        <div class="form-group"><label>Home Loan Amount (₹)</label><input type="number" id="inp1" value="5000000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (% P.A.)</label><input type="number" id="inp2" value="8.5" class="form-input"></div>
        <div class="form-group"><label>Loan Tenure (Years)</label><input type="number" id="inp3" value="20" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Monthly EMI</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Total Interest</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Payment</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / (12 * 100);
            let n = Number(document.getElementById('inp3').value) * 12;
            let emi = P * r * Math.pow(1+r, n) / (Math.pow(1+r, n) - 1);
            let totalPayment = emi * n;
            document.getElementById('res1').innerText = formatCurr(emi);
            document.getElementById('res2').innerText = formatCurr(totalPayment - P);
            document.getElementById('res3').innerText = formatCurr(totalPayment);
        }
        """
    },
    {
        "file": "car-loan.html", "title": "Car Loan EMI", "desc": "Calculate Equated Monthly Installment for Car loans",
        "form": """
        <div class="form-group"><label>Car Loan Amount (₹)</label><input type="number" id="inp1" value="800000" class="form-input"></div>
        <div class="form-group"><label>Interest Rate (% P.A.)</label><input type="number" id="inp2" value="9" class="form-input"></div>
        <div class="form-group"><label>Loan Tenure (Years)</label><input type="number" id="inp3" value="5" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Monthly EMI</div></div>
            <div class="calc-stat returns"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Total Interest</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Total Payment</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / (12 * 100);
            let n = Number(document.getElementById('inp3').value) * 12;
            let emi = P * r * Math.pow(1+r, n) / (Math.pow(1+r, n) - 1);
            let totalPayment = emi * n;
            document.getElementById('res1').innerText = formatCurr(emi);
            document.getElementById('res2').innerText = formatCurr(totalPayment - P);
            document.getElementById('res3').innerText = formatCurr(totalPayment);
        }
        """
    },
    {
        "file": "swp.html", "title": "SWP (Systematic Withdrawal Plan)", "desc": "Calculate your SWP payouts",
        "form": """
        <div class="form-group"><label>Total Investment (₹)</label><input type="number" id="inp1" value="5000000" class="form-input"></div>
        <div class="form-group"><label>Withdrawal per month (₹)</label><input type="number" id="inp2" value="25000" class="form-input"></div>
        <div class="form-group"><label>Expected Return (%)</label><input type="number" id="inp3" value="10" class="form-input"></div>
        <div class="form-group"><label>Time Period (Years)</label><input type="number" id="inp4" value="10" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Total Withdrawn</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res3">—</div><div class="calc-stat-label">Final Corpus Value</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let fund = Number(document.getElementById('inp1').value);
            let w = Number(document.getElementById('inp2').value);
            let r = Number(document.getElementById('inp3').value) / (12 * 100);
            let n = Number(document.getElementById('inp4').value) * 12;
            let totalW = 0;
            for(let i=0; i<n; i++){
                fund = fund * (1 + r) - w;
                totalW += w;
            }
            document.getElementById('res1').innerText = formatCurr(totalW);
            document.getElementById('res3').innerText = formatCurr(Math.max(0, fund));
        }
        """
    },
    {
        "file": "margin.html", "title": "Margin Calculator", "desc": "Calculate required margin for trades",
        "form": """
        <div class="form-group"><label>Instrument Price (₹)</label><input type="number" id="inp1" value="2500" class="form-input"></div>
        <div class="form-group"><label>Quantity</label><input type="number" id="inp2" value="100" class="form-input"></div>
        <div class="form-group"><label>Margin Required (%)</label><input type="number" id="inp3" value="20" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Total Value</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Required Margin</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let Q = Number(document.getElementById('inp2').value);
            let M = Number(document.getElementById('inp3').value) / 100;
            let total = P * Q;
            document.getElementById('res1').innerText = formatCurr(total);
            document.getElementById('res2').innerText = formatCurr(total * M);
        }
        """
    },
    {
        "file": "brokerage.html", "title": "Brokerage Calculator", "desc": "Calculate trading costs and net P/L",
        "form": """
        <div class="form-group"><label>Buy Price (₹)</label><input type="number" id="inp1" value="100" class="form-input"></div>
        <div class="form-group"><label>Sell Price (₹)</label><input type="number" id="inp2" value="110" class="form-input"></div>
        <div class="form-group"><label>Quantity</label><input type="number" id="inp3" value="500" class="form-input"></div>
        <div class="form-group"><label>Brokerage Charge (₹ per order)</label><input type="number" id="inp4" value="20" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Total Brokerage</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Net Profit / Loss</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let B = Number(document.getElementById('inp1').value);
            let S = Number(document.getElementById('inp2').value);
            let Q = Number(document.getElementById('inp3').value);
            let Fee = Number(document.getElementById('inp4').value) * 2; // Flat fee for buy and sell
            let gross = (S - B) * Q;
            document.getElementById('res1').innerText = formatCurr(Fee);
            document.getElementById('res2').innerText = formatCurr(gross - Fee);
        }
        """
    },
    {
        "file": "gst.html", "title": "GST Calculator", "desc": "Add or Remove GST from product prices",
        "form": """
        <div class="form-group"><label>Original Price (₹)</label><input type="number" id="inp1" value="1000" class="form-input"></div>
        <div class="form-group"><label>GST Rate (%)</label><input type="number" id="inp2" value="18" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">GST Amount</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Final Price</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let gst = Number(document.getElementById('inp2').value) / 100;
            let gstAmt = P * gst;
            document.getElementById('res1').innerText = formatCurr(gstAmt);
            document.getElementById('res2').innerText = formatCurr(P + gstAmt);
        }
        """
    },
    {
        "file": "tds.html", "title": "TDS Calculator", "desc": "Calculate Tax Deducted at Source",
        "form": """
        <div class="form-group"><label>Amount (₹)</label><input type="number" id="inp1" value="50000" class="form-input"></div>
        <div class="form-group"><label>TDS Rate (%)</label><input type="number" id="inp2" value="10" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">TDS Amount</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Amount after TDS</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let P = Number(document.getElementById('inp1').value);
            let r = Number(document.getElementById('inp2').value) / 100;
            let tds = P * r;
            document.getElementById('res1').innerText = formatCurr(tds);
            document.getElementById('res2').innerText = formatCurr(P - tds);
        }
        """
    },
    {
        "file": "income-tax.html", "title": "Income Tax", "desc": "Estimate your income tax for the year (New Regime Simplified)",
        "form": """
        <div class="form-group"><label>Annual Income (₹)</label><input type="number" id="inp1" value="1200000" class="form-input"></div>
        <div class="form-group"><label>Standard Deduction (₹)</label><input type="number" id="inp2" value="75000" class="form-input" readonly></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Taxable Income</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Estimated Tax</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let inc = Number(document.getElementById('inp1').value);
            let tax_inc = Math.max(0, inc - 75000);
            let tax = 0;
            // Extremely simplified basic calculation for new regime (India)
            if(tax_inc > 400000 && tax_inc <= 800000) tax = (tax_inc - 400000) * 0.05;
            else if(tax_inc > 800000 && tax_inc <= 1200000) tax = 20000 + (tax_inc - 800000) * 0.10;
            else if(tax_inc > 1200000 && tax_inc <= 1600000) tax = 60000 + (tax_inc - 1200000) * 0.15;
            else if(tax_inc > 1600000 && tax_inc <= 2000000) tax = 120000 + (tax_inc - 1600000) * 0.20;
            else if(tax_inc > 2000000 && tax_inc <= 2400000) tax = 200000 + (tax_inc - 2000000) * 0.25;
            else if(tax_inc > 2400000) tax = 300000 + (tax_inc - 2400000) * 0.30;
            
            if(tax_inc <= 1200000) tax = 0; // Rebate
            
            document.getElementById('res1').innerText = formatCurr(tax_inc);
            document.getElementById('res2').innerText = formatCurr(tax);
        }
        """
    },
    {
        "file": "hra.html", "title": "HRA Exemption", "desc": "Calculate House Rent Allowance tax exemption",
        "form": """
        <div class="form-group"><label>Basic Salary (Yearly ₹)</label><input type="number" id="inp1" value="500000" class="form-input"></div>
        <div class="form-group"><label>HRA Received (Yearly ₹)</label><input type="number" id="inp2" value="200000" class="form-input"></div>
        <div class="form-group"><label>Total Rent Paid (Yearly ₹)</label><input type="number" id="inp3" value="180000" class="form-input"></div>
        """,
        "res": """
        <div class="calc-result-values">
            <div class="calc-stat invested"><div class="calc-stat-value" id="res1">—</div><div class="calc-stat-label">Exempted HRA</div></div>
            <div class="calc-stat total"><div class="calc-stat-value" id="res2">—</div><div class="calc-stat-label">Taxable HRA</div></div>
        </div>
        """,
        "js": """
        function runCalc() {
            let basic = Number(document.getElementById('inp1').value);
            let hra = Number(document.getElementById('inp2').value);
            let rent = Number(document.getElementById('inp3').value);
            
            let cond1 = hra;
            let cond2 = Math.max(0, rent - (0.10 * basic));
            let cond3 = 0.50 * basic; // assuming metro
            
            let exempt = Math.min(cond1, cond2, cond3);
            
            document.getElementById('res1').innerText = formatCurr(exempt);
            document.getElementById('res2').innerText = formatCurr(hra - exempt);
        }
        """
    }
]

for c in calcs:
    html = get_html(c["title"], c["desc"], c["form"], c["res"], c["js"])
    with open(os.path.join(base_dir, c["file"]), 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"Generated {c['file']}")

print(f"Generated {len(calcs)} calculators successfully.")
