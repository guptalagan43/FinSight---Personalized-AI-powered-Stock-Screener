import os
import glob
import re

html_files = glob.glob(r'd:\WD Lab Project\frontend\pages\*.html')

mega_menu_inner = """
                    <a href="#" class="nav-link">Calculators ▾</a>
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

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regex to replace the inner contents of <div class="nav-item-dropdown">
    # Note: re.sub with DOTALL
    pattern = r'(<div class="nav-item-dropdown">).*?(</div>\s*<a href="/pages/dashboard.html" class="nav-link">)'
    
    new_content = re.sub(pattern, r'\1' + mega_menu_inner + r'\2', content, flags=re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)
    print(f"Updated megamenu in {os.path.basename(f)}")
