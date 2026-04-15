import os
import glob

html_files = glob.glob(r'd:\WD Lab Project\frontend\pages\*.html')

dropdown_html = """                <div class="nav-item-dropdown">
                    <a href="#" class="nav-link">Calculators ▾</a>
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
                </div>"""

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '<div class="nav-item-dropdown">' not in content:
        content = content.replace('<a href="/pages/calculators.html" class="nav-link">Calculators</a>', dropdown_html)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")
