


async function initCategory(slug, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (slug === 'market-calendar') {
        renderCalendar(container);
        return;
    }
    if (slug === 'stocks-feed') {
        renderFeed(container);
        return;
    }

    try {
        const res = await fetch('/api/instruments/all');
        let data = await res.json();

        // Sort Data based on slug
        if (slug === 'top-gainers') {
            data.sort((a, b) => (b.day_change_pct || 0) - (a.day_change_pct || 0));
        } else if (slug === 'top-losers') {
            data.sort((a, b) => (a.day_change_pct || 0) - (b.day_change_pct || 0));
        } else if (slug === '52-weeks-high') {
            data.sort((a, b) => ((b.current_price / (b.high_52w || 1)) || 0) - ((a.current_price / (a.high_52w || 1)) || 0));
        } else if (slug === '52-weeks-low') {
            data.sort((a, b) => ((a.current_price / (a.low_52w || 1)) || 0) - ((b.current_price / (b.low_52w || 1)) || 0));
        } else if (slug === 'most-traded') {
            data.sort((a, b) => (b.market_cap || 0) - (a.market_cap || 0));
        }

        data = data.slice(0, 30); // Show top 30
        
        let html = '';
        data.forEach(inst => {
            const isUp = inst.day_change >= 0;
            const dirClass = isUp ? 'up' : 'down';
            const arrow = isUp ? '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-bottom: 2px; margin-right: 2px;"><polyline points="18 15 12 9 6 15"></polyline></svg> +' : '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-bottom: 2px; margin-right: 2px;"><polyline points="6 9 12 15 18 9"></polyline></svg> -';
            html += `
                <div class="market-card-mini glow-card" onclick="window.location.href='/pages/instrument_detail.html?id=${inst.id}'" 
                     style="cursor:pointer; background: var(--surface); border-radius: var(--radius-lg); padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border: 1.5px solid var(--gray-200); box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: all 0.25s ease;"
                     onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 24px rgba(0,0,0,0.08)'; this.style.borderColor='var(--gray-200)'"
                     onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 4px rgba(0,0,0,0.04)'; this.style.borderColor='var(--gray-200)'">
                    <div class="market-info" style="flex: 1; z-index: 2;">
                        <div class="market-label" style="font-weight:700; font-size:1.1em; color:var(--text);">${inst.symbol}</div>
                        <div class="market-desc" style="font-size:0.85em; color:var(--text-light); margin-bottom: 8px;">${inst.name}</div>
                        <div class="market-value" style="font-size:1.4em; color:var(--text); font-weight: 600;">₹${parseFloat(inst.current_price).toFixed(2)}</div>
                        <div class="market-change ${dirClass}" style="font-size:0.9em; font-weight: 600; color: ${isUp ? 'var(--success)' : 'var(--danger)'};">
                            ${arrow} ${Math.abs(inst.day_change).toFixed(2)} (${Math.abs(inst.day_change_pct).toFixed(2)}%)
                        </div>
                    </div>
                    <div class="market-extra" style="text-align:right; font-size:0.85em; color:var(--text-muted); z-index: 2;">
                        <div>52w H: ₹${parseFloat(inst.high_52w).toFixed(2)}</div>
                        <div>52w L: ₹${parseFloat(inst.low_52w).toFixed(2)}</div>
                        <div style="margin-top:4px;">MCap: ${inst.market_cap ? (inst.market_cap / 1000).toFixed(1) + 'k Cr' : '-'}</div>
                    </div>
                </div>
            `;
        });
        
        container.style.display = 'grid';
        container.style.gridTemplateColumns = 'repeat(auto-fill, minmax(300px, 1fr))';
        container.style.gap = '20px';
        container.innerHTML = html;

    } catch (e) {
        console.error(e);
        container.innerHTML = '<div style="color:var(--danger); text-align:center;">Failed to load data.</div>';
    }
}

function renderCalendar(container) {
    const events = [
        { date: "Tomorrow, 09:00 AM", title: "TCS Q4 Earnings Call", type: "Earnings", impact: "High", desc: "Expected strong margin expansion..." },
        { date: "Next Mon, 10:00 AM", title: "RBI Policy Announcement", type: "Macro", impact: "High", desc: "No rate cut anticipated, outlook matters." },
        { date: "Next Tue, EOD", title: "Reliance Dividend Ex-Date", type: "Corporate Action", impact: "Medium", desc: "₹10 per share special dividend." },
        { date: "24 Apr 2026", title: "HDFC Bank AGM", type: "Meeting", impact: "Low", desc: "Annual general meeting for stakeholders." },
        { date: "25 Apr 2026", title: "Infosys Board Meeting", type: "Corporate", impact: "High", desc: "Considering share buyback program." },
        { date: "28 Apr 2026", title: "Federal Reserve Minutes", type: "Global", impact: "High", desc: "US Fed releases policy meeting details." },
        { date: "1 May 2026", title: "Auto Sales Data", type: "Sectoral", impact: "Medium", desc: "Monthly dispatch numbers for May." }
    ];
    
    let leftCol = '<div style="display:flex; flex-direction:column; gap:16px;">';
    let rightCol = '<div style="display:flex; flex-direction:column; gap:16px;">';
    
    events.forEach((ev, index) => {
        let color = ev.impact === 'High' ? 'var(--primary)' : (ev.impact === 'Medium' ? '#f59e0b' : 'var(--text-light)');
        let card = `
            <div class="glow-card" style="background: var(--surface); padding: 20px; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm);" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; position:relative; z-index:2;">
                    <div>
                        <div style="color: var(--primary); font-weight: 600; margin-bottom: 4px;">${ev.date}</div>
                        <div style="font-size: 1.25em; font-weight: 600; color: var(--text);">${ev.title}</div>
                    </div>
                    <div style="text-align:right;">
                        <span style="background: var(--surface-hover); color: var(--text); padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: 500; border: 1px solid var(--border);">${ev.type}</span>
                        <div style="margin-top: 8px; font-size:0.85em; font-weight: 600; color: ${color};">Impact: ${ev.impact}</div>
                    </div>
                </div>
                <div style="color: var(--text-light); font-size: 0.95em; position:relative; z-index:2;">${ev.desc}</div>
            </div>
        `;
        if (index % 2 === 0) leftCol += card;
        else rightCol += card;
    });
    
    leftCol += '</div>';
    rightCol += '</div>';
    
    const trendingViews = `
        <div style="background: var(--surface); border: 1px solid var(--border); padding: 20px; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm);">
            <h3 style="font-size: 1.2em; color: var(--text); margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 12px;">Trending Themes</h3>
            <ul style="list-style: none; padding: 0; margin: 0; color: var(--text-light);">
                <li style="margin-bottom: 12px; display:flex; align-items:center; gap: 8px;"><span style="color: var(--primary);">🔥</span> <span>IT Sector Q4 Resurgence</span></li>
                <li style="margin-bottom: 12px; display:flex; align-items:center; gap: 8px;"><span style="color: var(--primary);"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg></span> <span>Rate Cut Expectations Delayed</span></li>
                <li style="margin-bottom: 12px; display:flex; align-items:center; gap: 8px;"><span style="color: var(--primary);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width: 1em; height: 1em; vertical-align: middle;"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg></span> <span>EV Subsidies Expansion</span></li>
                <li style="margin-bottom: 12px; display:flex; align-items:center; gap: 8px;"><span style="color: var(--primary);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width: 1em; height: 1em; vertical-align: middle;"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><path d="M9 22v-4h6v4"></path></svg></span> <span>PSU Bank Privatization</span></li>
                <li style="display:flex; align-items:center; gap: 8px;"><span style="color: var(--primary);"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width: 1em; height: 1em; vertical-align: middle;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg></span> <span>Green Energy Transition</span></li>
            </ul>
        </div>
    `;

    container.style.display = 'grid';
    container.style.gridTemplateColumns = '2fr 1fr';
    container.style.gap = '24px';
    container.innerHTML = `
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            ${leftCol}
            ${rightCol}
        </div>
        <div style="display: flex; flex-direction: column; gap: 16px;">
            ${trendingViews}
            <div style="background: var(--surface); border: 1px solid var(--border); padding: 20px; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm);">
                <h3 style="font-size: 1.2em; color: var(--text); margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 12px;">Weekly Highlights</h3>
                <div style="color: var(--text-light); font-size: 0.95em; line-height: 1.5;">
                    <p style="margin-bottom: 8px;">Expect high volatility this week due to upcoming central bank meetings globally.</p>
                    <p>Keep an eye on metal stocks as spot prices reflect slight uptrends.</p>
                </div>
            </div>
        </div>
    `;
}

function renderFeed(container) {
    const news = [
        { time: "10 mins ago", src: "Bloomberg", headline: "Indian Tech Stocks Surge Ahead of Quarter Results", sentiment: "Positive", content: "Key IT players rally context clues hint at better-than-expected margins for Q4." },
        { time: "1 hour ago", src: "Reuters", headline: "Oil Prices Dip Contextualizing Market Rebounds", sentiment: "Neutral", content: "Global crude prices fall by 2% amid easing geopolitical tensions, boosting aviation stocks." },
        { time: "2 hours ago", src: "Mint", headline: "RBI Keeps Repo Rate Unchanged in Surprise Move", sentiment: "Mixed", content: "The central bank maintained status quo on rates while modifying its liquidity stance." },
        { time: "5 hours ago", src: "CNBC", headline: "FIIs Turn Net Buyers Over the Last 5 Trading Sessions", sentiment: "Positive", content: "Foreign institutions poured over ₹5,000 Cr into domestic equities this past week." },
        { time: "7 hours ago", src: "ET", headline: "New Semiconductor Plants Approved in Gujarat", sentiment: "Positive", content: "Cabinet approves ₹30k Cr subsidies for the latest ecosystem hub." },
        { time: "12 hours ago", src: "Business Standard", headline: "Retail Inflation Rises Marginally to 5.2%", sentiment: "Negative", content: "Food prices remain sticky, pushing the headline inflation numbers slightly past estimates." },
        { time: "1 day ago", src: "Moneycontrol", headline: "Markets Scale New All-Time Highs", sentiment: "Positive", content: "NIFTY breaches 22,500 amid broad-based buying across large-caps and mid-caps." },
        { time: "1 day ago", src: "Forbes", headline: "Startups See Funding Winter Thawing", sentiment: "Neutral", content: "Late-stage VC deals pick up momentum in the enterprise SaaS tier." }
    ];
    
    let rows = '';
    news.forEach(n => {
        let sentColor = n.sentiment === 'Positive' ? 'var(--success)' : (n.sentiment === 'Negative' ? 'var(--danger)' : '#f59e0b');
        let link = `https://news.google.com/search?q=${encodeURIComponent(n.headline)}`;
        rows += `
            <div class="glow-card" style="background: var(--surface); border-left: 4px solid var(--primary); padding: 20px; border-radius: var(--radius-lg); margin-bottom: 20px; box-shadow: var(--shadow-sm);" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="display:flex; justify-content: space-between; font-size: 0.85em; color: var(--text-light); margin-bottom: 8px; font-weight: 500; position:relative; z-index:2;">
                    <span style="color: var(--primary); font-weight: 600;">${n.src}</span>
                    <span>${n.time} &nbsp;•&nbsp; <span style="color: ${sentColor}; font-weight: 600;">${n.sentiment}</span></span>
                </div>
                <div style="font-size: 1.25em; font-weight: 600; color: var(--text); margin-bottom: 8px; position:relative; z-index:2;">${n.headline}</div>
                <div style="font-size: 0.95em; color: var(--text-light); line-height: 1.5; position:relative; z-index:2;">${n.content}</div>
                <div style="margin-top: 16px; position:relative; z-index:2;">
                    <a href="${link}" target="_blank" style="color: var(--primary); text-decoration: none; font-size: 0.85em; font-weight: 600;">Read Full Article ➜</a>
                </div>
            </div>
        `;
    });
    
    const sentimentPanel = `
        <div style="background: var(--surface); border: 1px solid var(--border); padding: 24px; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); padding-bottom: 30px;">
            <h3 style="font-size: 1.3em; color: var(--text); margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--border);">Market Sentiment</h3>
            <div style="text-align: center; margin-bottom: 24px;">
                <div style="font-size: 3em; font-weight: 800; color: var(--success);">72</div>
                <div style="color: var(--text-light); font-weight: 600; text-transform: uppercase; font-size: 0.8em; letter-spacing: 1px;">Greed Zone</div>
            </div>
            
            <h4 style="font-size: 1em; color: var(--text); margin-bottom: 16px;">Top Trending Tags</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span style="background: var(--surface-hover); color: var(--text); border: 1px solid var(--border); padding: 6px 12px; border-radius: 20px; font-size: 0.8em; font-weight: 500;">#Q4Results</span>
                <span style="background: var(--surface-hover); color: var(--text); border: 1px solid var(--border); padding: 6px 12px; border-radius: 20px; font-size: 0.8em; font-weight: 500;">#RateCuts</span>
                <span style="background: var(--surface-hover); color: var(--text); border: 1px solid var(--border); padding: 6px 12px; border-radius: 20px; font-size: 0.8em; font-weight: 500;">#Nifty50</span>
                <span style="background: var(--surface-hover); color: var(--text); border: 1px solid var(--border); padding: 6px 12px; border-radius: 20px; font-size: 0.8em; font-weight: 500;">#Banks</span>
                <span style="background: var(--surface-hover); color: var(--text); border: 1px solid var(--border); padding: 6px 12px; border-radius: 20px; font-size: 0.8em; font-weight: 500;">#EV</span>
            </div>
            
            <h4 style="font-size: 1em; color: var(--text); margin-top: 32px; margin-bottom: 16px;">Sector Heatmap</h4>
            <div style="display: flex; flex-direction: column; gap: 12px; font-size: 0.85em; font-weight: 500;">
                <div style="display: flex; justify-content: space-between; color: var(--success);"><text>IT</text><text>+2.4%</text></div>
                <div style="display: flex; justify-content: space-between; color: var(--success);"><text>Automobile</text><text>+1.2%</text></div>
                <div style="display: flex; justify-content: space-between; color: var(--text-light);"><text>Banking</text><text>0.0%</text></div>
                <div style="display: flex; justify-content: space-between; color: var(--danger);"><text>FMCG</text><text>-0.8%</text></div>
            </div>
        </div>
    `;

    container.style.display = 'grid';
    container.style.gridTemplateColumns = '2.5fr 1fr';
    container.style.gap = '32px';
    
    container.innerHTML = `
        <div style="display: flex; flex-direction: column;">
            <h2 style="font-size: 1.5em; color: var(--text); margin-bottom: 24px; text-align: center;">Latest Market Updates</h2>
            ${rows}
        </div>
        <div>
            ${sentimentPanel}
        </div>
    `;
}
