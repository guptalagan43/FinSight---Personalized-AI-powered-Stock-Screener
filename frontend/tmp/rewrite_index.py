
import re

with open('d:/Claude Projects/WD Lab Project/frontend/pages/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update 500+ to 1000+
html = html.replace('data-value="500"', 'data-value="1000"')

# 2. Extract sections by string splitting

# We want everything before LIVE MARKET PREVIEW
p1_end = html.find('<!-- ═══════════════════════════════════════════════════════\n     LIVE MARKET PREVIEW')
p1 = html[:p1_end]

# We want everything after FINSIGHT PRO (PROMOTIVE)
# Actually, the user wants FinSight Pro removed, but the CTA section is after that? Wait! Let's check where the footer starts
p_footer_start = html.find('<!-- ═══════════════════════════════════════════════════════\n     FOOTER')
p2 = html[p_footer_start:]

# But CTA might still be there. Did I overwrite CTA previously? Let's check if CTA is still there. Wait, my previous rewrite kept CTA.
p_cta_start = html.find('<!-- ═══════════════════════════════════════════════════════\n     CTA')
if p_cta_start != -1:
    p2 = html[p_cta_start:]

# Now reconstruct the middle blocks
# 12 items for Live Market
market_items = """
        <div class="market-grid" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;">
            <!-- Nifty 50 -->
            <div class="market-card-mini glow-card reveal-section" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">NIFTY 50</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">NIFTY 50 Index</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹22,514.20</div>
                    <div class="market-change up" style="font-size:0.9em; font-weight: 600; color:var(--success);">▲ + 101.25 (0.45%)</div>
                </div>
            </div>
            <!-- Sensex -->
            <div class="market-card-mini glow-card reveal-section reveal-delay-1" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">SENSEX</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">SENSEX Index</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹73,400.10</div>
                    <div class="market-change down" style="font-size:0.9em; font-weight: 600; color:var(--danger);">▼ - 88.50 (-0.12%)</div>
                </div>
            </div>
            <!-- Banknifty -->
            <div class="market-card-mini glow-card reveal-section reveal-delay-2" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">BANKNIFTY</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">BANKNIFTY Index</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹48,930.55</div>
                    <div class="market-change up" style="font-size:0.9em; font-weight: 600; color:var(--success);">▲ + 388.20 (0.80%)</div>
                </div>
            </div>
            <!-- Finnifty -->
             <div class="market-card-mini glow-card reveal-section reveal-delay-3" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">FINNIFTY</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">FINNIFTY Index</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹21,830.55</div>
                    <div class="market-change up" style="font-size:0.9em; font-weight: 600; color:var(--success);">▲ + 110.20 (0.50%)</div>
                </div>
            </div>
            <!-- Reliance -->
            <div class="market-card-mini glow-card reveal-section" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">RELIANCE</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">EQ</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹2,895.10</div>
                    <div class="market-change down" style="font-size:0.9em; font-weight: 600; color:var(--danger);">▼ - 10.15 (-0.35%)</div>
                </div>
            </div>
            <!-- TCS -->
            <div class="market-card-mini glow-card reveal-section reveal-delay-1" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">TCS</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">EQ</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹3,925.00</div>
                    <div class="market-change up" style="font-size:0.9em; font-weight: 600; color:var(--success);">▲ + 46.50 (1.20%)</div>
                </div>
            </div>
            <!-- HDFC BANK -->
            <div class="market-card-mini glow-card reveal-section reveal-delay-2" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">HDFC BANK</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">EQ</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹1,510.45</div>
                    <div class="market-change up" style="font-size:0.9em; font-weight: 600; color:var(--success);">▲ + 10.15 (0.65%)</div>
                </div>
            </div>
            <!-- INFY -->
             <div class="market-card-mini glow-card reveal-section reveal-delay-3" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">INFY</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">EQ</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹1,425.20</div>
                    <div class="market-change down" style="font-size:0.9em; font-weight: 600; color:var(--danger);">▼ - 15.80 (1.10%)</div>
                </div>
            </div>
            <!-- NIFTY IT -->
             <div class="market-card-mini glow-card reveal-section" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">NIFTY IT</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">NIFTY IT Index</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹35,210.20</div>
                    <div class="market-change up" style="font-size:0.9em; font-weight: 600; color:var(--success);">▲ + 315.80 (0.95%)</div>
                </div>
            </div>
            <!-- NIFTY MIDCAP 100 -->
             <div class="market-card-mini glow-card reveal-section reveal-delay-1" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">NIFTY MIDCAP</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">MIDCAP Index</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹49,425.20</div>
                    <div class="market-change up" style="font-size:0.9em; font-weight: 600; color:var(--success);">▲ + 515.80 (1.10%)</div>
                </div>
            </div>
            <!-- NIFTY AUTO -->
             <div class="market-card-mini glow-card reveal-section reveal-delay-2" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">NIFTY AUTO</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">NIFTY AUTO Index</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹21,425.20</div>
                    <div class="market-change down" style="font-size:0.9em; font-weight: 600; color:var(--danger);">▼ - 110.80 (-0.50%)</div>
                </div>
            </div>
            <!-- NIFTY METAL -->
             <div class="market-card-mini glow-card reveal-section reveal-delay-3" style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;">
                <div class="market-info" style="flex: 1; z-index: 2;">
                    <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0;">NIFTY METAL</div>
                    <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">NIFTY METAL Index</div>
                    <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600; margin-bottom:0px;">₹8,425.20</div>
                    <div class="market-change down" style="font-size:0.9em; font-weight: 600; color:var(--danger);">▼ - 30.80 (-0.35%)</div>
                </div>
            </div>
        </div>
"""

new_middle = """
<!-- ═══════════════════════════════════════════════════════
     LIVE MARKET PREVIEW
     ═══════════════════════════════════════════════════════ -->
<section class="section market-preview" style="padding-top: 40px;">
    <div class="container">
        <div class="text-center reveal-section" style="margin-bottom: 48px;">
            <span class="section-tag">Market Intelligence</span>
            <h2 class="section-title">Live Market <span class="text-gradient">Overview</span></h2>
        </div>
""" + market_items + """
        <div style="text-align:center; margin-top:32px;">
            <a href="/pages/market-overview.html" class="btn" style="border:1px solid var(--primary); color:var(--primary); background:transparent;">View Full Market Dashboard</a>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════════════
     MARKET NEWS (3x2 Grid)
     ═══════════════════════════════════════════════════════ -->
<section class="section">
    <div class="container" style="max-width: 1400px; padding: 0 16px;">
        <div class="text-center reveal-section" style="margin-bottom: 48px;">
            <span class="section-tag">Latest Updates</span>
            <h2 class="section-title">Market <span class="text-gradient">News</span></h2>
        </div>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:20px;">
            <div class="glow-card reveal-section" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:24px; cursor:pointer;">
                <div style="font-size:0.75rem; color:var(--primary); font-weight:700; margin-bottom:8px; text-transform:uppercase;">Economy</div>
                <h3 style="font-size:1.1rem; margin-bottom:12px; color:var(--text);">RBI keeps repo rate unchanged at 6.5%, maintains 'withdrawal of accommodation' stance</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.5;">The central bank decided to keep the benchmark interest rate unchanged for the seventh consecutive time amid strong economic growth.</p>
                <div style="margin-top:16px; font-size:0.8rem; color:var(--text-muted);">2 hours ago</div>
            </div>
            <div class="glow-card reveal-section reveal-delay-1" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:24px; cursor:pointer;">
                <div style="font-size:0.75rem; color:var(--emerald); font-weight:700; margin-bottom:8px; text-transform:uppercase;">Markets</div>
                <h3 style="font-size:1.1rem; margin-bottom:12px; color:var(--text);">Nifty crosses 22,500 mark for the first time, IT and Auto stocks lead the rally</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.5;">Benchmark indices hit fresh all-time highs driven by sustained foreign capital inflows and strong corporate earnings expectations.</p>
                <div style="margin-top:16px; font-size:0.8rem; color:var(--text-muted);">4 hours ago</div>
            </div>
            <div class="glow-card reveal-section reveal-delay-2" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:24px; cursor:pointer;">
                <div style="font-size:0.75rem; color:var(--blue); font-weight:700; margin-bottom:8px; text-transform:uppercase;">Corporate</div>
                <h3 style="font-size:1.1rem; margin-bottom:12px; color:var(--text);">TCS Q4 Results Preview: IT major expected to report single-digit revenue growth</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.5;">Analysts expect India's largest IT services firm to report modest sequential revenue growth ahead of its quarterly earnings announcement.</p>
                <div style="margin-top:16px; font-size:0.8rem; color:var(--text-muted);">5 hours ago</div>
            </div>
            <div class="glow-card reveal-section" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:24px; cursor:pointer;">
                <div style="font-size:0.75rem; color:var(--magenta); font-weight:700; margin-bottom:8px; text-transform:uppercase;">Global</div>
                <h3 style="font-size:1.1rem; margin-bottom:12px; color:var(--text);">Federal Reserve signals one rate cut this year despite inflation concerns</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.5;">US central bank officials maintained aggressive stance against inflation but left door open for late-year reduction in borrowing costs.</p>
                <div style="margin-top:16px; font-size:0.8rem; color:var(--text-muted);">7 hours ago</div>
            </div>
            <div class="glow-card reveal-section reveal-delay-1" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:24px; cursor:pointer;">
                <div style="font-size:0.75rem; color:var(--cyan); font-weight:700; margin-bottom:8px; text-transform:uppercase;">IPO</div>
                <h3 style="font-size:1.1rem; margin-bottom:12px; color:var(--text);">Upcoming IPO: Tech startup sets price band at ₹300-320 per share</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.5;">The highly anticipated tech offering will open for subscription next week, aiming to raise over ₹5,000 crore from markets.</p>
                <div style="margin-top:16px; font-size:0.8rem; color:var(--text-muted);">8 hours ago</div>
            </div>
            <div class="glow-card reveal-section reveal-delay-2" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:24px; cursor:pointer;">
                <div style="font-size:0.75rem; color:var(--primary); font-weight:700; margin-bottom:8px; text-transform:uppercase;">Commodities</div>
                <h3 style="font-size:1.1rem; margin-bottom:12px; color:var(--text);">Gold prices hit record high as geopolitical tensions spur safe-haven demand</h3>
                <p style="font-size:0.9rem; color:var(--text-light); line-height:1.5;">Precious metals continue their upward trajectory alongside industrial commodities as global market uncertainties persist.</p>
                <div style="margin-top:16px; font-size:0.8rem; color:var(--text-muted);">10 hours ago</div>
            </div>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════════════
     TODAY'S TOP STOCKS (4x2 Grid)
     ═══════════════════════════════════════════════════════ -->
<section class="section" style="background:var(--bg-alt);">
    <div class="container">
        <div class="text-center reveal-section" style="margin-bottom: 48px;">
            <span class="section-tag">Movers & Shakers</span>
            <h2 class="section-title">Today's <span class="text-gradient">Top Stocks</span></h2>
        </div>
        <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:16px;">
            <!-- Row 1 -->
            <div class="glow-card reveal-section" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <h3 style="font-size:1.1rem; color:var(--text);">TATA STEEL</h3>
                    <span style="background:rgba(34, 197, 94, 0.1); color:var(--success); padding:4px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">+ 4.2%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:1.3rem; font-weight:700; color:var(--text);">₹165.40</div>
                    </div>
                </div>
            </div>
            
            <div class="glow-card reveal-section reveal-delay-1" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <h3 style="font-size:1.1rem; color:var(--text);">ZOMATO</h3>
                    <span style="background:rgba(34, 197, 94, 0.1); color:var(--success); padding:4px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">+ 3.5%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:1.3rem; font-weight:700; color:var(--text);">₹185.90</div>
                    </div>
                </div>
            </div>

            <div class="glow-card reveal-section reveal-delay-2" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <h3 style="font-size:1.1rem; color:var(--text);">MARUTI</h3>
                    <span style="background:rgba(34, 197, 94, 0.1); color:var(--success); padding:4px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">+ 2.1%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:1.3rem; font-weight:700; color:var(--text);">₹12,650.00</div>
                    </div>
                </div>
            </div>

            <div class="glow-card reveal-section reveal-delay-3" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <h3 style="font-size:1.1rem; color:var(--text);">ITC</h3>
                    <span style="background:rgba(34, 197, 94, 0.1); color:var(--success); padding:4px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">+ 1.8%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:1.3rem; font-weight:700; color:var(--text);">₹435.50</div>
                    </div>
                </div>
            </div>

            <!-- Row 2 -->
            <div class="glow-card reveal-section" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <h3 style="font-size:1.1rem; color:var(--text);">WIPRO</h3>
                    <span style="background:rgba(239, 68, 68, 0.1); color:var(--danger); padding:4px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">- 2.8%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:1.3rem; font-weight:700; color:var(--text);">₹460.25</div>
                    </div>
                </div>
            </div>
            
            <div class="glow-card reveal-section reveal-delay-1" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <h3 style="font-size:1.1rem; color:var(--text);">INFY</h3>
                    <span style="background:rgba(239, 68, 68, 0.1); color:var(--danger); padding:4px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">- 1.5%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:1.3rem; font-weight:700; color:var(--text);">₹1,425.20</div>
                    </div>
                </div>
            </div>

            <div class="glow-card reveal-section reveal-delay-2" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <h3 style="font-size:1.1rem; color:var(--text);">TITAN</h3>
                    <span style="background:rgba(239, 68, 68, 0.1); color:var(--danger); padding:4px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">- 1.2%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:1.3rem; font-weight:700; color:var(--text);">₹3,450.15</div>
                    </div>
                </div>
            </div>

            <div class="glow-card reveal-section reveal-delay-3" style="background:#fff; border-radius:var(--radius-lg); border:1px solid var(--gray-200); padding:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                    <h3 style="font-size:1.1rem; color:var(--text);">M&M</h3>
                    <span style="background:rgba(34, 197, 94, 0.1); color:var(--success); padding:4px 8px; border-radius:4px; font-size:0.85rem; font-weight:600;">+ 0.8%</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                    <div>
                        <div style="font-size:1.3rem; font-weight:700; color:var(--text);">₹2,105.80</div>
                    </div>
                </div>
            </div>
        </div>
        <div style="text-align:center; margin-top:32px;">
            <a href="/pages/categories/top-gainers.html" class="btn" style="border:1px solid var(--primary); color:var(--primary); background:transparent;">View Top Movers</a>
        </div>
    </div>
</section>

<!-- ═══════════════════════════════════════════════════════
     TECHNICAL INDICATORS (TECHNICAL)
     ═══════════════════════════════════════════════════════ -->
<section class="section">
    <div class="container">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:40px;">
            <div style="flex:1; min-width:300px;" class="reveal-section">
                <span class="section-tag">Advanced Analysis</span>
                <h2 class="section-title">Technical <span class="text-gradient">Indicators</span></h2>
                <p class="section-desc" style="margin-left:0; margin-top:16px; margin-bottom:24px;">
                    Go beyond basic charts. Identify overbought/oversold conditions, momentum shifts, and trend reversals with our suite of built-in technical indicators.
                </p>
                <ul style="list-style:none; padding:0; display:grid; gap:12px; color:var(--text-light);">
                    <li style="display:flex; align-items:center; gap:8px;"><span style="color:var(--primary);">✔</span> Relative Strength Index (RSI)</li>
                    <li style="display:flex; align-items:center; gap:8px;"><span style="color:var(--primary);">✔</span> Moving Averages (SMA & EMA)</li>
                    <li style="display:flex; align-items:center; gap:8px;"><span style="color:var(--primary);">✔</span> Moving Average Convergence Divergence (MACD)</li>
                    <li style="display:flex; align-items:center; gap:8px;"><span style="color:var(--primary);">✔</span> Bollinger Bands Support</li>
                </ul>
                <div style="margin-top:32px;">
                    <a href="/pages/screeners.html" class="btn btn-primary">Try Technical Screeners</a>
                </div>
            </div>
            <div style="flex:1; min-width:300px; padding:24px; background:var(--glass-bg); backdrop-filter:var(--glass-blur); border:1px solid var(--glass-border); border-radius:var(--radius-xl);" class="reveal-section reveal-delay-2">
                <div style="display:flex; justify-content:space-between; margin-bottom:16px;">
                    <span style="font-weight:700;">RSI Alert</span>
                    <span style="color:var(--danger); font-size:0.85rem; padding:2px 8px; border-radius:4px; background:rgba(239,68,68,0.1);">Oversold (25.4)</span>
                </div>
                <div style="width:100%; height:8px; background:var(--gray-200); border-radius:4px; overflow:hidden; margin-bottom:24px;">
                    <div style="width:25.4%; height:100%; background:var(--danger);"></div>
                </div>
                
                <div style="display:flex; justify-content:space-between; margin-bottom:16px;">
                    <span style="font-weight:700;">MACD Crossover</span>
                    <span style="color:var(--success); font-size:0.85rem; padding:2px 8px; border-radius:4px; background:rgba(34,197,94,0.1);">Bullish Trigger</span>
                </div>
                <div style="width:100%; height:40px; display:flex; align-items:flex-end; gap:4px; margin-bottom:8px;">
                    <div style="flex:1; background:rgba(239,68,68,0.5); height:80%;"></div>
                    <div style="flex:1; background:rgba(239,68,68,0.3); height:60%;"></div>
                    <div style="flex:1; background:rgba(239,68,68,0.1); height:30%;"></div>
                    <div style="flex:1; background:rgba(34,197,94,0.3); height:40%;"></div>
                    <div style="flex:1; background:rgba(34,197,94,0.6); height:70%;"></div>
                    <div style="flex:1; background:rgba(34,197,94,0.8); height:100%;"></div>
                </div>
            </div>
        </div>
    </div>
</section>
"""

new_html = p1 + new_middle + p2
with open('d:/Claude Projects/WD Lab Project/frontend/pages/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("done")
