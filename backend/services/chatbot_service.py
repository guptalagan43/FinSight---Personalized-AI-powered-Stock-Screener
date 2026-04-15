"""
FinSight AI Chatbot Service – Comprehensive Rule-Based Intelligence Engine.

Provides personalized, context-aware financial insights using:
  - Full user profile (age, income, risk, experience, goals, occupation, etc.)
  - Portfolio positions (holdings, P&L, diversification)
  - Watchlist contents
  - Instrument fundamentals (PE, ROE, D/E, margins, growth)
  - Sector performance data

No external LLM API needed – all intelligence is encoded in rules and templates.
"""
import re
import random
from config import Config


# ═══════════════════════════════════════════════════════════════
#  INTENT DETECTION
# ═══════════════════════════════════════════════════════════════

INTENT_PATTERNS = {
    "greeting": [
        r"\b(hi|hello|hey|good morning|good evening|howdy|sup)\b",
        r"^(help|what can you do|how do you work|what.*you.*help)",
    ],
    "portfolio_summary": [
        r"\b(portfolio|my holdings|my stocks|my investments|how.*(my|portfolio).*doing)\b",
        r"\b(total.*value|invested.*amount|overall.*return|my p.?l|my position)\b",
    ],
    "portfolio_advice": [
        r"\b(what should i (buy|sell|invest)|rebalance|diversif|improve my portfolio)\b",
        r"\b(suggest.*buy|recommend.*stock|add.*portfolio|where.*invest)\b",
        r"\b(which.*stock|pick.*stock|new.*investment|allocation)\b",
    ],
    "risk_assessment": [
        r"\b(risk|too.*risky|safe enough|volatil|danger|exposure)\b",
        r"\b(concentrated|overweight|underweight|beta|drawdown)\b",
    ],
    "watchlist_insight": [
        r"\b(watchlist|tracked|watching|my list|stocks i.*track)\b",
    ],
    "stock_analysis": [
        r"\b(tell me about|analyze|analysis|overview|details|about)\b",
        r"\b(how.*is|what.*think.*about|what.*know.*about)\b",
        r"\b(research|deep.?dive|breakdown|review|evaluate|assess.*stock)\b",
        r"\b(give me.*(info|detail|data|insight)|summarize|summary)\b",
    ],
    "stock_comparison": [
        r"\b(compare|versus|which.*better|pick.*between)\b",
        r"\b(differ|stronger|weaker|prefer)\b",
        r"(\w+)\s+vs\s+(\w+)",
    ],
    "suitability_check": [
        r"\b(suitable|good for me|should i (buy|invest in)|right for me|fit.*profile)\b",
        r"\b(worth (buying|investing)|recommend.*for me|match.*profile)\b",
    ],
    "price_query": [
        r"\b(current price|stock price|share price|how much.*cost|quote|what price)\b",
        r"\b(52.?week|52w|all.?time|day.*change|trading at|priced at|latest.*price|live.*price)\b",
    ],
    "valuation_analysis": [
        r"\b(overvalued|undervalued|fair value|intrinsic|cheap|expensive|valuation)\b",
        r"\b(worth.*price|price.*justified|premium|discount|peg ratio)\b",
        r"\b(bubble|overpriced|bargain|steal|attractive price)\b",
    ],
    "growth_analysis": [
        r"\b(growth|growing|revenue growth|profit growth|sales growth|cagr)\b",
        r"\b(fast.?grow|slow.?grow|growth rate|expansion|scaling|momentum)\b",
        r"\b(top.?line|bottom.?line|yoy|year.?over|quarterly)\b",
    ],
    "profitability_query": [
        r"\b(profit|profitab|margin|net profit|operating profit|ebitda)\b",
        r"\b(making money|loss.?making|breakeven|bottom.?line|cash flow)\b",
        r"\b(net income|pat|operating margin|gross margin)\b",
    ],
    "dividend_query": [
        r"\b(dividend|yield|payout|dividend.?pay|dividend.?yield|income.*stock)\b",
        r"\b(passive income|regular income|cash return|distribution)\b",
    ],
    "promoter_query": [
        r"\b(promoter|management|ownership|holding|stake|insider|fii|dii)\b",
        r"\b(who owns|governance|board|leadership|ceo|founder)\b",
    ],
    "sector_analysis": [
        r"\b(sector|industry|segment|it sector|banking sector|pharma|auto|fmcg)\b",
        r"\b(which sector|sector.*(good|bad|hot|cold)|sector.*perform)\b",
        r"\b(technology|financial|healthcare|energy|consumer|real estate)\b",
    ],
    "debt_analysis": [
        r"\b(debt|leverage|borrow|loan|d.?e ratio|interest coverage)\b",
        r"\b(leveraged|balance sheet|liabilit|solven|credit)\b",
    ],
    "fundamentals_query": [
        r"\b(pe ratio|p.?e|p.?b|roe|roce|eps|fundamental)\b",
        r"\b(book value|face value|market cap|enterprise value)\b",
        r"\b(ratio|metric|indicator|financial health|financial data)\b",
    ],
    "goal_planning": [
        r"\b(goal|retirement|wealth|saving|target|financial plan|future|long.?term)\b",
        r"\b(how.*reach|achieve|plan for|build.*corpus|fire|freedom)\b",
        r"\b(child|education.*fund|house|car|marriage|emergency)\b",
    ],
    "income_advice": [
        r"\b(income|salary|earning|afford|budget|monthly.*invest|sip)\b",
        r"\b(how much.*invest|investment capacity|saving.*rate)\b",
    ],
    "screener_suggestion": [
        r"\b(find|screen|filter|search.*stock|high roe|low pe|undervalued)\b",
        r"\b(best stock|top pick|hidden gem|value pick|multi.?bagger)\b",
        r"\b(penny stock|blue.?chip|large.?cap|mid.?cap|small.?cap)\b",
    ],
    "market_overview": [
        r"\b(market|nifty|sensex|today.*market|market.*today|bull|bear|trend)\b",
        r"\b(index|indices|bse|nse|market.*crash|market.*rally|correction)\b",
    ],
    "investment_timing": [
        r"\b(when.*buy|right time|good time|entry|exit|timing|dip|correction)\b",
        r"\b(buy the dip|wait|hold|sell now|book profit|stop loss)\b",
        r"\b(entry point|exit point|target price|support|resistance)\b",
    ],
    "etf_fund_query": [
        r"\b(etf|mutual fund|index fund|nfo|nav|expense ratio|aum)\b",
        r"\b(fund house|fund manager|scheme|elss|liquid fund)\b",
    ],
    "tax_query": [
        r"\b(tax|stcg|ltcg|capital gain|80c|section|deduction|taxable)\b",
        r"\b(tax.*sav|tax.*benefit|tax.*free|exempt)\b",
    ],
    "ipo_query": [
        r"\b(ipo|listing|debut|upcoming ipo|subscribe|allotment|grey market)\b",
    ],
}


def detect_intent(message: str) -> str:
    """Classify user message into an intent category with weighted scoring."""
    msg = message.lower().strip()
    scores = {}
    for intent, patterns in INTENT_PATTERNS.items():
        score = 0
        for pattern in patterns:
            if re.search(pattern, msg):
                score += 1
        if score > 0:
            scores[intent] = score
    if not scores:
        # If we have no match at all, check if it's a question about something on page
        if any(w in msg for w in ['?', 'what', 'how', 'why', 'when', 'is', 'are', 'does', 'do', 'can', 'will', 'tell']):
            return "dynamic_instrument"  # generative fallback with instrument context
        return "general"
    return max(scores, key=scores.get)


def extract_stock_mention(message: str, instruments: list) -> dict | None:
    """Try to find a mentioned stock name/symbol in the message."""
    msg = message.upper().strip()
    for inst in instruments:
        sym = inst.get("symbol", "").upper()
        name = inst.get("name", "").upper()
        if sym and (f" {sym} " in f" {msg} " or msg.startswith(sym + " ") or msg.endswith(" " + sym)):
            return inst
        if name and len(name) > 3 and name in msg:
            return inst
    return None


# ═══════════════════════════════════════════════════════════════
#  PERSONALIZATION HELPERS
# ═══════════════════════════════════════════════════════════════

def _fmt_currency(val):
    """Format number as ₹ currency."""
    if val is None:
        return "N/A"
    v = float(val)
    if abs(v) >= 10000000:
        return f"₹{v / 10000000:.2f} Cr"
    if abs(v) >= 100000:
        return f"₹{v / 100000:.2f} L"
    if abs(v) >= 1000:
        return f"₹{v / 1000:.1f}K"
    return f"₹{v:,.2f}"


def _fmt_pct(val):
    if val is None:
        return "N/A"
    return f"{float(val):+.2f}%"


def _risk_label(profile):
    risk = (profile.get("risk_profile") or "Moderate").lower()
    if risk == "aggressive":
        return "aggressive"
    elif risk == "conservative":
        return "conservative"
    return "moderate"


def _experience_label(profile):
    exp = (profile.get("experience_level") or "Beginner").lower()
    if exp == "professional":
        return "experienced"
    elif exp == "intermediate":
        return "intermediate"
    return "beginner"


def _income_label(profile):
    val = profile.get("income_range")
    if not val:
        return None
    n = int(val) if str(val).isdigit() else 0
    if n >= 5000000:
        return "high-income"
    if n >= 1000000:
        return "mid-income"
    if n >= 250000:
        return "modest-income"
    return None


def _age_bracket(profile):
    age = profile.get("age")
    if not age:
        return None
    age = int(age)
    if age < 25:
        return "young"
    if age < 35:
        return "early-career"
    if age < 50:
        return "mid-career"
    return "pre-retirement"


def _portfolio_stats(positions: list) -> dict:
    """Calculate portfolio summary statistics."""
    if not positions:
        return {"count": 0, "total_invested": 0, "current_value": 0, "total_pl": 0, "return_pct": 0}
    total_invested = sum(p.get("buy_price", 0) * p.get("quantity", 0) for p in positions)
    current_value = sum(p.get("current_price", 0) * p.get("quantity", 0) for p in positions)
    total_pl = current_value - total_invested
    return_pct = (total_pl / total_invested * 100) if total_invested > 0 else 0

    # Sector concentration
    sectors = {}
    for p in positions:
        s = p.get("sector") or "Unknown"
        val = p.get("current_price", 0) * p.get("quantity", 0)
        sectors[s] = sectors.get(s, 0) + val
    top_sector = max(sectors, key=sectors.get) if sectors else "N/A"
    top_sector_pct = (sectors.get(top_sector, 0) / current_value * 100) if current_value > 0 else 0

    return {
        "count": len(positions),
        "total_invested": total_invested,
        "current_value": current_value,
        "total_pl": total_pl,
        "return_pct": return_pct,
        "sectors": sectors,
        "top_sector": top_sector,
        "top_sector_pct": top_sector_pct,
        "winners": [p for p in positions if p.get("unrealized_pl", 0) > 0],
        "losers": [p for p in positions if p.get("unrealized_pl", 0) < 0],
    }


def _suitability_score(instrument_data: dict, fundamentals: dict, user_profile: dict) -> dict:
    """Score how suitable a stock is for this user's profile."""
    score = 50  # Base score
    reasons = []
    warnings = []

    risk = _risk_label(user_profile)
    exp = _experience_label(user_profile)

    pe = fundamentals.get("pe") if fundamentals else None
    roe = fundamentals.get("roe") if fundamentals else None
    de = fundamentals.get("debt_to_equity") if fundamentals else None
    mcap = instrument_data.get("market_cap")
    npm = fundamentals.get("net_profit_margin") if fundamentals else None
    sg = fundamentals.get("sales_growth") if fundamentals else None

    # PE valuation check
    if pe is not None:
        if pe < 15:
            score += 10
            reasons.append("Reasonably valued (PE < 15)")
        elif pe > 50:
            score -= 15
            warnings.append(f"High valuation risk (PE: {pe:.1f})")
        elif pe > 30:
            score -= 5
            warnings.append(f"Somewhat expensive (PE: {pe:.1f})")

    # ROE quality check
    if roe is not None:
        if roe > 20:
            score += 15
            reasons.append(f"Strong returns on equity (ROE: {roe:.1f}%)")
        elif roe > 12:
            score += 5
            reasons.append(f"Decent ROE ({roe:.1f}%)")
        elif roe < 5:
            score -= 10
            warnings.append(f"Low ROE ({roe:.1f}%) suggests poor capital efficiency")

    # Debt check vs risk profile
    if de is not None:
        if risk == "conservative" and de > 1.0:
            score -= 15
            warnings.append(f"High debt (D/E: {de:.2f}) – may not suit your conservative profile")
        elif de < 0.3:
            score += 10
            reasons.append(f"Low debt (D/E: {de:.2f}) – strong balance sheet")
        elif de > 2.0:
            score -= 10
            warnings.append(f"Very high leverage (D/E: {de:.2f})")

    # Market cap vs experience
    if mcap is not None:
        if exp == "beginner" and mcap < 5000:
            score -= 10
            warnings.append("Small-cap stock – higher risk for beginners")
        elif mcap > 100000:
            score += 5
            reasons.append("Large-cap stock – relatively stable")

    # Profit margin check
    if npm is not None:
        if npm > 20:
            score += 5
            reasons.append(f"High profit margins ({npm:.1f}%)")
        elif npm < 0:
            score -= 10
            warnings.append("Company is not profitable")

    # Growth check
    if sg is not None:
        if sg > 15:
            score += 5
            reasons.append(f"Strong revenue growth ({sg:.1f}%)")

    # Risk profile adjustment
    if risk == "aggressive":
        score += 5
    elif risk == "conservative":
        score -= 5

    score = max(0, min(100, score))
    if score >= 70:
        verdict = "Well-Suited"
    elif score >= 45:
        verdict = "Moderately Suitable"
    else:
        verdict = "May Not Be Ideal"

    return {"score": score, "verdict": verdict, "reasons": reasons, "warnings": warnings}


# ═══════════════════════════════════════════════════════════════
#  RESPONSE GENERATORS (per intent)
# ═══════════════════════════════════════════════════════════════

DISCLAIMER = (
    "\n\n⚠️ *Disclaimer: This is AI-generated educational information only, "
    "not investment advice. Please consult a qualified financial advisor "
    "before making investment decisions.*"
)


def _greet(user_profile: dict, context: dict) -> str:
    name = user_profile.get("name", "").split()[0] if user_profile.get("name") else "there"
    portfolio_count = len(context.get("positions", []))
    watchlist_count = sum(len(w.get("items", [])) for w in context.get("watchlists", []))

    lines = [f"👋 **Hi {name}!** I'm your FinSight AI assistant.\n"]
    lines.append("I can help you with:\n")
    lines.append("📊 **Portfolio Analysis** – Check how your investments are doing")
    lines.append("🔍 **Stock Research** – Deep-dive into any stock's fundamentals")
    lines.append("✅ **Suitability Check** – See if a stock matches your profile")
    lines.append("📈 **Market Insights** – Sector trends and market overview")
    lines.append("🎯 **Goal Planning** – Advice based on your investment goals")
    lines.append("⭐ **Watchlist Analysis** – Insights on stocks you're tracking\n")

    if portfolio_count > 0:
        lines.append(f"You currently have **{portfolio_count} stocks** in your portfolio. Ask me how they're performing!")
    if watchlist_count > 0:
        lines.append(f"You're watching **{watchlist_count} stocks**. I can analyze them for you.")

    return "\n".join(lines)


def _portfolio_summary(user_profile: dict, context: dict) -> str:
    positions = context.get("positions", [])
    if not positions:
        return ("📭 **Your portfolio is empty.**\n\n"
                "You haven't added any holdings yet. Go to your Dashboard to add positions, "
                f"or ask me to suggest stocks based on your **{user_profile.get('risk_profile', 'Moderate')}** risk profile!"
                + DISCLAIMER)

    stats = _portfolio_stats(positions)
    name = (user_profile.get("name") or "").split()[0] or "there"
    pl_emoji = "📈" if stats["total_pl"] >= 0 else "📉"

    lines = [f"📊 **Portfolio Summary for {name}**\n"]
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Holdings | **{stats['count']} stocks** |")
    lines.append(f"| Total Invested | **{_fmt_currency(stats['total_invested'])}** |")
    lines.append(f"| Current Value | **{_fmt_currency(stats['current_value'])}** |")
    lines.append(f"| Unrealized P&L | {pl_emoji} **{_fmt_currency(stats['total_pl'])}** ({_fmt_pct(stats['return_pct'])}) |")
    lines.append("")

    # Top performers
    winners = sorted(stats["winners"], key=lambda p: p.get("return_pct", 0), reverse=True)
    if winners:
        best = winners[0]
        lines.append(f"🏆 **Top Performer**: {best.get('name', best.get('symbol', 'N/A'))} ({_fmt_pct(best.get('return_pct', 0))})")

    losers = sorted(stats["losers"], key=lambda p: p.get("return_pct", 0))
    if losers:
        worst = losers[0]
        lines.append(f"⚠️ **Needs Attention**: {worst.get('name', worst.get('symbol', 'N/A'))} ({_fmt_pct(worst.get('return_pct', 0))})")

    # Diversification insight
    if stats["top_sector_pct"] > 50:
        lines.append(f"\n⚡ **Concentration Alert**: {stats['top_sector_pct']:.0f}% of your portfolio is in **{stats['top_sector']}**. Consider diversifying across sectors.")
    else:
        lines.append(f"\n✅ Your portfolio has reasonable sector diversification (largest: {stats['top_sector']} at {stats['top_sector_pct']:.0f}%).")

    risk = _risk_label(user_profile)
    if risk == "conservative" and any(p.get("return_pct", 0) < -15 for p in positions):
        lines.append(f"\n💡 Given your **conservative** risk profile, you might consider reviewing loss-making positions.")

    return "\n".join(lines) + DISCLAIMER


def _portfolio_advice(user_profile: dict, context: dict) -> str:
    positions = context.get("positions", [])
    risk = _risk_label(user_profile)
    exp = _experience_label(user_profile)
    income = _income_label(user_profile)
    goals = user_profile.get("goals", "")

    lines = ["🧠 **Personalized Portfolio Advice**\n"]

    if not positions:
        lines.append("You don't have any holdings yet. Here's how to get started:\n")
        if risk == "conservative":
            lines.append("• Start with **large-cap blue-chips** like Reliance, HDFC Bank, TCS")
            lines.append("• Consider **index funds** tracking NIFTY 50 for diversification")
            lines.append("• Avoid small-cap and high-volatility stocks initially")
        elif risk == "aggressive":
            lines.append("• Mix of **large-cap** (60%) and **mid-cap** (40%) can work")
            lines.append("• Look at **growth stocks** with strong ROE and revenue growth")
            lines.append("• Consider sector leaders in IT, Banking, and Pharma")
        else:
            lines.append("• Start with a **balanced mix** of large-cap (70%) and mid-cap (30%)")
            lines.append("• Focus on companies with consistent dividend history")
            lines.append("• Use the Screener to find stocks matching your criteria")

        if income:
            monthly = user_profile.get("monthly_investment_capacity")
            if monthly:
                lines.append(f"\n💰 With your monthly capacity of **{_fmt_currency(monthly)}**, consider SIP-based investing for disciplined wealth creation.")

        return "\n".join(lines) + DISCLAIMER

    stats = _portfolio_stats(positions)

    # Diversification advice
    sector_count = len(stats["sectors"])
    if sector_count < 3:
        lines.append(f"⚠️ **Diversification**: You're only in **{sector_count} sectors**. Aim for at least 4-5 sectors to reduce risk.\n")
    else:
        lines.append(f"✅ **Diversification**: Good spread across {sector_count} sectors.\n")

    # Position sizing
    if stats["current_value"] > 0:
        for p in positions:
            val = p.get("current_price", 0) * p.get("quantity", 0)
            pct = val / stats["current_value"] * 100
            if pct > 40:
                lines.append(f"⚡ **{p.get('symbol', 'N/A')}** makes up {pct:.0f}% of your portfolio – consider trimming to reduce concentration risk.")

    # Loss management
    big_losers = [p for p in positions if p.get("return_pct", 0) < -20]
    if big_losers:
        lines.append("\n📉 **Loss Review**:")
        for p in big_losers:
            lines.append(f"• {p.get('symbol', 'N/A')} is down {_fmt_pct(p.get('return_pct', 0))} – review if the fundamentals still support holding.")

    # Goal-aligned advice
    if goals:
        lines.append(f"\n🎯 Based on your goal of **{goals}**:")
        goal_lower = goals.lower()
        if "retirement" in goal_lower:
            lines.append("• Focus on compounding and long-term growth stocks")
            lines.append("• Increase allocation to stable dividend-paying stocks over time")
        elif "wealth" in goal_lower:
            lines.append("• Balance growth stocks with some value picks")
            lines.append("• Reinvest dividends for compounding")
        elif "tax" in goal_lower:
            lines.append("• Consider ELSS mutual funds for Section 80C benefits")
            lines.append("• Long-term equity holdings (>1 year) get favorable tax treatment")
        elif "education" in goal_lower:
            lines.append("• Set a target amount and timeline")
            lines.append("• SIP into diversified equity funds works well for 5+ year goals")

    return "\n".join(lines) + DISCLAIMER


def _risk_assessment(user_profile: dict, context: dict) -> str:
    positions = context.get("positions", [])
    risk = _risk_label(user_profile)
    exp = _experience_label(user_profile)

    lines = [f"🛡️ **Risk Assessment** (Profile: **{risk.title()}** | Experience: **{exp.title()}**)\n"]

    if not positions:
        lines.append("No holdings found. Add your portfolio positions to get a detailed risk analysis.")
        return "\n".join(lines) + DISCLAIMER

    stats = _portfolio_stats(positions)

    # Portfolio risk metrics
    risk_score = 0
    risk_factors = []

    # Concentration risk
    if stats.get("top_sector_pct", 0) > 50:
        risk_score += 25
        risk_factors.append(f"High sector concentration ({stats['top_sector']}: {stats['top_sector_pct']:.0f}%)")
    elif stats.get("top_sector_pct", 0) > 35:
        risk_score += 10
        risk_factors.append(f"Moderate sector concentration ({stats['top_sector']}: {stats['top_sector_pct']:.0f}%)")

    # Number of stocks
    if stats["count"] < 3:
        risk_score += 20
        risk_factors.append(f"Too few stocks ({stats['count']}) – low diversification")
    elif stats["count"] > 15:
        risk_score += 5
        risk_factors.append(f"Many holdings ({stats['count']}) – may be over-diversified")

    # Loss exposure
    loss_pct = abs(sum(p.get("unrealized_pl", 0) for p in stats.get("losers", [])))
    if stats["current_value"] > 0 and loss_pct / stats["current_value"] > 0.1:
        risk_score += 15
        risk_factors.append(f"Significant unrealized losses ({_fmt_currency(loss_pct)})")

    # Overall assessment
    if risk_score <= 10:
        emoji, label = "📈", "Low Risk"
    elif risk_score <= 30:
        emoji, label = "📌", "Moderate Risk"
    elif risk_score <= 50:
        emoji, label = "🟠", "Elevated Risk"
    else:
        emoji, label = "📉", "High Risk"

    lines.append(f"**Overall Risk Level**: {emoji} **{label}** (Score: {risk_score}/100)\n")

    if risk_factors:
        lines.append("**Risk Factors Identified**:")
        for rf in risk_factors:
            lines.append(f"• {rf}")

    # Profile alignment
    if risk == "conservative" and risk_score > 30:
        lines.append(f"\n⚠️ Your portfolio risk ({label}) is **higher** than your conservative profile suggests. Consider rebalancing toward large-cap, low-debt stocks.")
    elif risk == "aggressive" and risk_score < 15:
        lines.append(f"\n💡 Your portfolio is quite conservative for an aggressive investor. You could consider adding some growth-oriented mid-cap positions.")
    else:
        lines.append(f"\n✅ Your portfolio risk level aligns with your **{risk}** profile.")

    return "\n".join(lines) + DISCLAIMER


def _watchlist_insight(user_profile: dict, context: dict) -> str:
    watchlists = context.get("watchlists", [])
    if not watchlists or all(len(w.get("items", [])) == 0 for w in watchlists):
        return ("⭐ **Your watchlists are empty.**\n\n"
                "Start tracking stocks by adding them to your watchlist from any stock detail page. "
                "I'll then provide analysis on the stocks you're watching!" + DISCLAIMER)

    risk = _risk_label(user_profile)
    lines = ["⭐ **Watchlist Analysis**\n"]

    for wl in watchlists:
        items = wl.get("items", [])
        if not items:
            continue
        lines.append(f"**{wl.get('name', 'Watchlist')}** ({len(items)} stocks):\n")
        lines.append(f"| Stock | Price | Day Change |")
        lines.append(f"|-------|-------|------------|")
        for item in items:
            pct = item.get("day_change_pct", 0)
            emoji = "📈" if pct >= 0 else "📉"
            lines.append(f"| {item.get('symbol', 'N/A')} | {_fmt_currency(item.get('current_price'))} | {emoji} {_fmt_pct(pct)} |")
        lines.append("")

    # Quick insight
    all_items = [item for wl in watchlists for item in wl.get("items", [])]
    gainers = [i for i in all_items if (i.get("day_change_pct") or 0) > 0]
    losers = [i for i in all_items if (i.get("day_change_pct") or 0) < 0]

    if gainers:
        best = max(gainers, key=lambda x: x.get("day_change_pct", 0))
        lines.append(f"📈 **Best today**: {best.get('symbol', 'N/A')} ({_fmt_pct(best.get('day_change_pct', 0))})")
    if losers:
        worst = min(losers, key=lambda x: x.get("day_change_pct", 0))
        lines.append(f"📉 **Weakest today**: {worst.get('symbol', 'N/A')} ({_fmt_pct(worst.get('day_change_pct', 0))})")

    return "\n".join(lines) + DISCLAIMER


def _stock_analysis(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "I need to know which stock you're asking about. Please specify a stock name or ask from a stock detail page." + DISCLAIMER

    name = instrument_data.get("name", "This stock")
    symbol = instrument_data.get("symbol", "")
    sector = instrument_data.get("sector", "N/A")
    price = instrument_data.get("current_price")
    change_pct = instrument_data.get("day_change_pct", 0)
    mcap = instrument_data.get("market_cap")
    high52 = instrument_data.get("high_52w")
    low52 = instrument_data.get("low_52w")

    lines = [f"📊 **{name}** ({symbol})\n"]
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Current Price | **{_fmt_currency(price)}** ({_fmt_pct(change_pct)} today) |")
    lines.append(f"| Market Cap | {_fmt_currency(mcap)} |")
    lines.append(f"| Sector | {sector} |")
    if high52:
        lines.append(f"| 52W High | {_fmt_currency(high52)} |")
    if low52:
        lines.append(f"| 52W Low | {_fmt_currency(low52)} |")

    if fundamentals:
        lines.append(f"\n**Key Fundamentals**:\n")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        pairs = [
            ("PE Ratio", "pe"), ("PB Ratio", "pb"), ("ROE", "roe"),
            ("ROCE", "roce"), ("Debt/Equity", "debt_to_equity"),
            ("Net Margin", "net_profit_margin"), ("Sales Growth", "sales_growth"),
            ("Profit Growth", "profit_growth"), ("Promoter Holding", "promoter_holding"),
        ]
        for label, key in pairs:
            val = fundamentals.get(key)
            if val is not None:
                suffix = "%" if key in ("roe", "roce", "net_profit_margin", "sales_growth", "profit_growth", "promoter_holding") else ""
                lines.append(f"| {label} | {float(val):.2f}{suffix} |")

    # Quick assessment
    lines.append(f"\n**Quick Assessment**:")
    if fundamentals:
        pe = fundamentals.get("pe")
        roe = fundamentals.get("roe")
        de = fundamentals.get("debt_to_equity")
        if pe and pe < 20 and roe and roe > 15:
            lines.append("✅ Attractively valued with strong returns")
        elif pe and pe > 40:
            lines.append("⚠️ Premium valuation – growth expectations are high")
        if de and de < 0.3:
            lines.append("✅ Very low debt – strong balance sheet")
        elif de and de > 1.5:
            lines.append("⚠️ High leverage – monitor debt servicing ability")

    # 52-week position
    if price and high52 and low52:
        range_pct = ((price - low52) / (high52 - low52) * 100) if high52 != low52 else 50
        if range_pct > 80:
            lines.append(f"📈 Trading near 52W highs ({range_pct:.0f}% of range)")
        elif range_pct < 20:
            lines.append(f"📉 Trading near 52W lows ({range_pct:.0f}% of range)")

    return "\n".join(lines) + DISCLAIMER


def _suitability_check(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify which stock you'd like me to evaluate for your profile, or ask from a stock detail page." + DISCLAIMER

    name = instrument_data.get("name", "This stock")
    symbol = instrument_data.get("symbol", "")
    result = _suitability_score(instrument_data, fundamentals or {}, user_profile)

    risk = user_profile.get("risk_profile", "Moderate")
    exp = user_profile.get("experience_level", "Beginner")
    goals = user_profile.get("goals", "")

    score_bar = "█" * (result["score"] // 10) + "░" * (10 - result["score"] // 10)

    lines = [f"✅ **Suitability Analysis: {name}** ({symbol})\n"]
    lines.append(f"**Your Profile**: {risk} risk | {exp} | {goals or 'No specific goals'}\n")
    lines.append(f"**Suitability Score**: [{score_bar}] **{result['score']}/100** – {result['verdict']}\n")

    if result["reasons"]:
        lines.append("**Positive Factors**:")
        for r in result["reasons"]:
            lines.append(f"  ✅ {r}")

    if result["warnings"]:
        lines.append("\n**Concerns**:")
        for w in result["warnings"]:
            lines.append(f"  ⚠️ {w}")

    # Personalized recommendation
    lines.append("\n**Recommendation**:")
    if result["score"] >= 70:
        lines.append(f"This stock aligns well with your **{risk.lower()}** profile. "
                      "Consider doing additional research on recent quarterly results before investing.")
    elif result["score"] >= 45:
        lines.append(f"This stock has some merits but also concerns for your profile. "
                      "Consider starting with a small position and monitoring closely.")
    else:
        lines.append(f"This stock may not be the best fit for your **{risk.lower()}** profile. "
                      "Look at alternatives using the Stock Screener for better matches.")

    return "\n".join(lines) + DISCLAIMER


def _sector_analysis(instrument_data: dict, user_profile: dict, context: dict) -> str:
    sector = instrument_data.get("sector") if instrument_data else None
    sectors_data = context.get("sectors", [])

    lines = ["📈 **Sector Overview**\n"]

    if sectors_data:
        lines.append(f"| Sector | Stocks | Avg Change |")
        lines.append(f"|--------|--------|------------|")
        sorted_sectors = sorted(sectors_data, key=lambda s: s.get("avg_day_change_pct", 0), reverse=True)
        for s in sorted_sectors[:10]:
            pct = s.get("avg_day_change_pct", 0)
            emoji = "📈" if pct >= 0 else "📉"
            lines.append(f"| {s.get('sector', 'N/A')} | {s.get('instrument_count', 0)} | {emoji} {_fmt_pct(pct)} |")
        lines.append("")

        gainers = [s for s in sorted_sectors if s.get("avg_day_change_pct", 0) > 0]
        losers = [s for s in sorted_sectors if s.get("avg_day_change_pct", 0) < 0]

        if gainers:
            lines.append(f"🏆 **Top Sector**: {gainers[0].get('sector')} ({_fmt_pct(gainers[0].get('avg_day_change_pct', 0))})")
        if losers:
            lines.append(f"📉 **Weakest Sector**: {losers[-1].get('sector')} ({_fmt_pct(losers[-1].get('avg_day_change_pct', 0))})")

    if sector:
        lines.append(f"\n📌 Currently viewing the **{sector}** sector.")

    return "\n".join(lines) + DISCLAIMER


def _debt_analysis(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify which company's debt you'd like to analyze." + DISCLAIMER

    name = instrument_data.get("name", "This company")
    risk = _risk_label(user_profile)

    lines = [f"💳 **Debt Analysis: {name}**\n"]

    if not fundamentals:
        lines.append("No fundamental data available for this instrument.")
        return "\n".join(lines) + DISCLAIMER

    de = fundamentals.get("debt_to_equity")
    debt = fundamentals.get("debt")
    equity = fundamentals.get("equity")
    npm = fundamentals.get("net_profit_margin")

    if de is not None:
        lines.append(f"**Debt-to-Equity Ratio**: {float(de):.2f}")
        if de < 0.1:
            lines.append("→ ✅ Almost debt-free! Very strong balance sheet.")
        elif de < 0.5:
            lines.append("→ ✅ Low leverage – manageable debt levels.")
        elif de < 1.0:
            lines.append("→ 📌 Moderate debt – within acceptable norms for most sectors.")
        elif de < 2.0:
            lines.append("→ 🟠 High leverage – monitor interest coverage and cash flows.")
        else:
            lines.append("→ 📉 Very high debt – significant risk if earnings decline.")

    if debt is not None:
        lines.append(f"\n**Total Debt**: {_fmt_currency(debt)}")
    if equity is not None:
        lines.append(f"**Total Equity**: {_fmt_currency(equity)}")

    # Risk profile alignment
    lines.append(f"\n**For Your {risk.title()} Profile**:")
    if risk == "conservative":
        if de and de > 0.5:
            lines.append("⚠️ With a conservative approach, prefer companies with D/E below 0.5.")
        else:
            lines.append("✅ Debt levels are within your comfort zone.")
    elif risk == "aggressive":
        if de and de < 1.5:
            lines.append("✅ Leverage is acceptable for growth-oriented investing.")
        else:
            lines.append("⚠️ Even for aggressive investors, D/E above 1.5 warrants caution.")
    else:
        if de and de < 1.0:
            lines.append("✅ Moderate risk investors should be comfortable with this debt level.")
        else:
            lines.append("⚠️ Consider if the company's earnings can comfortably service this debt.")

    return "\n".join(lines) + DISCLAIMER


def _fundamentals_query(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify which stock's fundamentals you'd like to check." + DISCLAIMER

    return _stock_analysis(instrument_data, fundamentals, user_profile)


def _goal_planning(user_profile: dict, context: dict) -> str:
    goals = user_profile.get("goals", "")
    risk = _risk_label(user_profile)
    age = _age_bracket(user_profile)
    income = _income_label(user_profile)
    monthly = user_profile.get("monthly_investment_capacity")
    yearly = user_profile.get("yearly_investment_capacity")

    lines = ["🎯 **Goal-Based Investment Planning**\n"]
    lines.append(f"**Your Profile**: {risk.title()} risk | Age: {age or 'N/A'} | Goals: {goals or 'Not specified'}\n")

    if monthly:
        lines.append(f"💰 **Monthly Investment Capacity**: {_fmt_currency(monthly)}")
    if yearly:
        lines.append(f"📅 **Yearly Investment Capacity**: {_fmt_currency(yearly)}")
    lines.append("")

    # Goal-specific advice
    if goals:
        goal_lower = goals.lower()
        if "retirement" in goal_lower:
            lines.append("**Retirement Planning**:")
            lines.append("• Start early – compounding is your best friend")
            if age == "young":
                lines.append("• At your age, you can afford 70-80% equity allocation")
                lines.append("• SIP into NIFTY 50 index funds for core allocation")
            elif age == "mid-career":
                lines.append("• Shift gradually: 60% equity, 30% debt, 10% gold")
                lines.append("• Focus on dividend-paying large-caps for stability")
            elif age == "pre-retirement":
                lines.append("• Prioritize capital preservation: 40% equity, 50% debt, 10% gold")
                lines.append("• Focus on low-volatility dividend aristocrats")
            if monthly:
                sip_15yr = float(monthly) * 12 * 15 * 1.12  # rough estimate
                lines.append(f"• With {_fmt_currency(monthly)}/month SIP at ~12% returns, you could build ~{_fmt_currency(sip_15yr)} in 15 years")

        elif "wealth" in goal_lower:
            lines.append("**Wealth Creation**:")
            lines.append("• Diversify across large, mid, and small caps (60/25/15)")
            lines.append("• Reinvest dividends for compounding")
            lines.append("• Review and rebalance portfolio quarterly")

        elif "tax" in goal_lower:
            lines.append("**Tax Saving**:")
            lines.append("• ELSS mutual funds – 3-year lock-in, Section 80C deduction up to ₹1.5L")
            lines.append("• NPS – Additional ₹50K deduction under 80CCD(1B)")
            lines.append("• Hold equity investments >1 year for LTCG tax rate of 10%")

        elif "education" in goal_lower:
            lines.append("**Education Fund**:")
            lines.append("• Set specific target amount and timeline")
            lines.append("• For 5+ year goals: equity-heavy SIP approach")
            lines.append("• For <3 year goals: debt funds or FDs for safety")
    else:
        lines.append("💡 **Set your investment goals** in your Profile to get personalized planning advice!")
        lines.append("\nCommon goals to consider:")
        lines.append("• Wealth creation • Retirement planning")
        lines.append("• Tax saving • Education fund • Emergency fund")

    return "\n".join(lines) + DISCLAIMER


def _income_advice(user_profile: dict, context: dict) -> str:
    income = _income_label(user_profile)
    monthly = user_profile.get("monthly_investment_capacity")
    yearly = user_profile.get("yearly_investment_capacity")
    risk = _risk_label(user_profile)
    occupation = user_profile.get("occupation", "")

    lines = ["💰 **Investment Advice Based on Your Income**\n"]

    if monthly:
        lines.append(f"**Monthly Capacity**: {_fmt_currency(monthly)}")
    if yearly:
        lines.append(f"**Yearly Capacity**: {_fmt_currency(yearly)}")
    if income:
        lines.append(f"**Income Bracket**: {income.title()}")
    if occupation:
        lines.append(f"**Occupation**: {occupation.title()}")
    lines.append("")

    if monthly:
        m = float(monthly)
        lines.append("**Suggested Monthly Allocation**:\n")
        if income == "high-income":
            lines.append(f"• Equity SIP: {_fmt_currency(m * 0.5)} (50%) – diversified equity funds")
            lines.append(f"• Direct Stocks: {_fmt_currency(m * 0.25)} (25%) – research-backed picks")
            lines.append(f"• Debt/FD: {_fmt_currency(m * 0.15)} (15%) – stability")
            lines.append(f"• Gold/International: {_fmt_currency(m * 0.1)} (10%) – hedge")
        elif income == "mid-income":
            lines.append(f"• Equity SIP: {_fmt_currency(m * 0.6)} (60%) – index + flexi-cap funds")
            lines.append(f"• Direct Stocks: {_fmt_currency(m * 0.2)} (20%) – blue-chips only")
            lines.append(f"• Emergency Fund: {_fmt_currency(m * 0.2)} (20%) – liquid fund or savings")
        else:
            lines.append(f"• Equity SIP: {_fmt_currency(m * 0.5)} (50%) – NIFTY 50 index fund")
            lines.append(f"• RD/FD: {_fmt_currency(m * 0.3)} (30%) – guaranteed returns")
            lines.append(f"• Emergency Buffer: {_fmt_currency(m * 0.2)} (20%)")
    else:
        lines.append("💡 Update your **Monthly Investment Capacity** in your Profile for personalized allocation advice!")

    if occupation and occupation.lower() == "student":
        lines.append("\n🎓 **Student-Specific Tips**:")
        lines.append("• Start small – even ₹500/month SIP builds the habit")
        lines.append("• Focus on learning stock analysis alongside investing")
        lines.append("• Use FinSight screeners to practice fundamental analysis")

    return "\n".join(lines) + DISCLAIMER


def _screener_suggestion(user_profile: dict, context: dict) -> str:
    risk = _risk_label(user_profile)
    exp = _experience_label(user_profile)

    lines = ["🔍 **Stock Screener Suggestions for Your Profile**\n"]
    lines.append(f"Based on your **{risk}** risk / **{exp}** experience level:\n")

    if risk == "conservative":
        lines.append("**Recommended Screeners**:")
        lines.append("• 🏦 **High ROE Blue Chips** – Large-caps with ROE > 20%")
        lines.append("• 🛡️ **Debt-Free Compounders** – Minimal debt, high ROCE")
        lines.append("• 💎 **Value Picks** – PE < 15, ROE > 15%")
        lines.append("\n*Focus on quality over growth for capital preservation.*")
    elif risk == "aggressive":
        lines.append("**Recommended Screeners**:")
        lines.append("• 🚀 **Growth Champions** – Sales & profit growth > 15%")
        lines.append("• 🌟 **Midcap Growth Stars** – Mid-caps with strong momentum")
        lines.append("• 💰 **Rapid Profit Growers** – Profit growth > 30%")
        lines.append("\n*Higher growth = higher potential but also higher volatility.*")
    else:
        lines.append("**Recommended Screeners**:")
        lines.append("• 📊 **Large Cap Compounders** – Stable growth with high ROE")
        lines.append("• 🎯 **Low Debt Growth Stocks** – Growth with safety margin")
        lines.append("• 🏆 **High Margin Leaders** – Net margin > 20%")
        lines.append("\n*Balanced approach combining growth and value.*")

    lines.append("\n👉 Visit the **Screeners** page to run these filters and discover matching stocks!")

    return "\n".join(lines) + DISCLAIMER


def _market_overview(user_profile: dict, context: dict) -> str:
    sectors_data = context.get("sectors", [])

    lines = ["📈 **Market Overview**\n"]

    if sectors_data:
        positive = sum(1 for s in sectors_data if s.get("avg_day_change_pct", 0) > 0)
        negative = len(sectors_data) - positive

        if positive > negative:
            lines.append(f"📈 **Market Sentiment**: Broadly Positive ({positive} of {len(sectors_data)} sectors in green)\n")
        elif negative > positive:
            lines.append(f"📉 **Market Sentiment**: Broadly Negative ({negative} of {len(sectors_data)} sectors in red)\n")
        else:
            lines.append(f"📌 **Market Sentiment**: Mixed ({positive} green, {negative} red sectors)\n")

        sorted_sectors = sorted(sectors_data, key=lambda s: s.get("avg_day_change_pct", 0), reverse=True)
        if sorted_sectors:
            top3 = sorted_sectors[:3]
            bottom3 = sorted_sectors[-3:]
            lines.append("**Top Performing Sectors**:")
            for s in top3:
                lines.append(f"  📈 {s.get('sector', 'N/A')}: {_fmt_pct(s.get('avg_day_change_pct', 0))}")
            lines.append("\n**Weakest Sectors**:")
            for s in bottom3:
                lines.append(f"  📉 {s.get('sector', 'N/A')}: {_fmt_pct(s.get('avg_day_change_pct', 0))}")

    risk = _risk_label(user_profile)
    lines.append(f"\n💡 **For Your {risk.title()} Profile**:")
    if risk == "conservative":
        lines.append("Focus on defensive sectors like FMCG, Pharma, and IT during volatility.")
    elif risk == "aggressive":
        lines.append("Consider momentum plays in leading sectors, but maintain stop-losses.")
    else:
        lines.append("A balanced approach across sectors helps navigate market cycles.")

    return "\n".join(lines) + DISCLAIMER


def _stock_comparison(instrument_data: dict, user_profile: dict) -> str:
    # Without two explicit instruments, provide guidance
    lines = ["⚖️ **Stock Comparison**\n"]
    if instrument_data:
        name = instrument_data.get("name", "this stock")
        lines.append(f"I can see you're looking at **{name}**.")
        lines.append("To compare it with another stock, try asking:")
        lines.append(f'• "Compare {name} with [other stock]"')
        lines.append('• "Is HDFC better than ICICI?"')
        lines.append("\nFor now, here's a quick suitability check:")
        return "\n".join(lines) + "\n\n" + _suitability_check(instrument_data, None, user_profile)

    lines.append("To compare stocks, you can:")
    lines.append("• Open a stock detail page and ask me to compare it")
    lines.append("• Use the **Screener** to filter and compare stocks side by side")
    lines.append('• Try asking: "Compare TCS with Infosys"')

    return "\n".join(lines) + DISCLAIMER


def _price_query(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify a stock or navigate to a stock detail page to get price information." + DISCLAIMER
    name = instrument_data.get("name", "This stock")
    symbol = instrument_data.get("symbol", "")
    price = instrument_data.get("current_price")
    change = instrument_data.get("day_change", 0)
    change_pct = instrument_data.get("day_change_pct", 0)
    high52 = instrument_data.get("high_52w")
    low52 = instrument_data.get("low_52w")
    mcap = instrument_data.get("market_cap")

    emoji = "📈" if change_pct >= 0 else "📉"
    lines = [f"💰 **{name}** ({symbol}) – Price Overview\n"]
    lines.append(f"**Current Price**: {_fmt_currency(price)} {emoji} {_fmt_pct(change_pct)} today ({_fmt_currency(abs(change))} {'up' if change >= 0 else 'down'})\n")
    if high52 and low52:
        lines.append(f"| Range | Value |")
        lines.append(f"|-------|-------|")
        lines.append(f"| 52-Week High | {_fmt_currency(high52)} |")
        lines.append(f"| 52-Week Low | {_fmt_currency(low52)} |")
        if price and high52 != low52:
            from_high = ((high52 - price) / high52 * 100)
            from_low = ((price - low52) / low52 * 100)
            range_pos = ((price - low52) / (high52 - low52) * 100)
            lines.append(f"| Distance from High | {from_high:.1f}% below |")
            lines.append(f"| Distance from Low | {from_low:.1f}% above |")
            lines.append(f"\n📏 **52W Range Position**: {'▓' * int(range_pos // 10)}{'░' * (10 - int(range_pos // 10))} {range_pos:.0f}%")
            if range_pos > 85:
                lines.append("📈 Trading near 52-week highs — strong momentum but watch for resistance.")
            elif range_pos < 15:
                lines.append("📉 Trading near 52-week lows — potential value opportunity or distress signal. Check fundamentals.")
    if mcap:
        lines.append(f"\n**Market Cap**: {_fmt_currency(mcap)}")
        if mcap > 100000:
            lines.append("Category: **Large Cap** 🏢")
        elif mcap > 20000:
            lines.append("Category: **Mid Cap** 🏗️")
        else:
            lines.append("Category: **Small Cap** 🏠")
    return "\n".join(lines) + DISCLAIMER


def _valuation_analysis(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify a stock to get valuation analysis." + DISCLAIMER
    name = instrument_data.get("name", "This stock")
    lines = [f"📐 **Valuation Analysis: {name}**\n"]
    if not fundamentals:
        lines.append("No fundamental data available to assess valuation.")
        return "\n".join(lines) + DISCLAIMER
    pe = fundamentals.get("pe")
    pb = fundamentals.get("pb")
    roe = fundamentals.get("roe")
    sg = fundamentals.get("sales_growth")
    pg = fundamentals.get("profit_growth")
    npm = fundamentals.get("net_profit_margin")
    signals = []
    lines.append("| Metric | Value | Signal |")
    lines.append("|--------|-------|--------|")
    if pe is not None:
        if pe < 12: sig = "📈 Cheap"
        elif pe < 20: sig = "📈 Fair"
        elif pe < 35: sig = "📌 Moderate"
        elif pe < 60: sig = "🟠 Pricey"
        else: sig = "📉 Expensive"
        lines.append(f"| PE Ratio | {pe:.1f} | {sig} |")
        signals.append(("PE", pe < 25))
    if pb is not None:
        if pb < 1.5: sig = "📈 Undervalued"
        elif pb < 3: sig = "📌 Fair"
        elif pb < 6: sig = "🟠 Premium"
        else: sig = "📉 Very High"
        lines.append(f"| PB Ratio | {pb:.1f} | {sig} |")
        signals.append(("PB", pb < 3))
    if roe is not None:
        if roe > 20: sig = "📈 Strong"
        elif roe > 12: sig = "📌 Decent"
        else: sig = "📉 Weak"
        lines.append(f"| ROE | {roe:.1f}% | {sig} |")
        signals.append(("ROE", roe > 15))
    # PEG-style check
    if pe and pg and pg > 0:
        peg = pe / pg
        if peg < 1: sig = "📈 Growth at reasonable price"
        elif peg < 2: sig = "📌 Fair for growth"
        else: sig = "📉 Overpriced for growth"
        lines.append(f"| PEG (PE/Growth) | {peg:.1f} | {sig} |")
        signals.append(("PEG", peg < 1.5))
    # Verdict
    positive = sum(1 for _, v in signals if v)
    total = len(signals)
    lines.append("")
    if total > 0:
        if positive >= total * 0.7:
            lines.append(f"✅ **Verdict**: Appears **attractively valued** ({positive}/{total} positive signals). Fundamentals support current or lower price levels.")
        elif positive >= total * 0.4:
            lines.append(f"📌 **Verdict**: **Fairly valued** ({positive}/{total} positive). Neither cheap nor expensive at current levels.")
        else:
            lines.append(f"⚠️ **Verdict**: Appears **richly valued** ({positive}/{total} positive). Premium pricing may already reflect growth expectations.")
    risk = _risk_label(user_profile)
    if risk == "conservative" and pe and pe > 30:
        lines.append(f"\n💡 For your **conservative** profile, high-PE stocks carry more downside risk during corrections.")
    return "\n".join(lines) + DISCLAIMER


def _growth_analysis(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify a stock to analyze its growth." + DISCLAIMER
    name = instrument_data.get("name", "This stock")
    lines = [f"📈 **Growth Analysis: {name}**\n"]
    if not fundamentals:
        lines.append("No fundamental data available.")
        return "\n".join(lines) + DISCLAIMER
    sg = fundamentals.get("sales_growth")
    pg = fundamentals.get("profit_growth")
    roe = fundamentals.get("roe")
    npm = fundamentals.get("net_profit_margin")
    rev = fundamentals.get("revenue")
    np_val = fundamentals.get("net_profit")
    lines.append("| Metric | Value | Assessment |")
    lines.append("|--------|-------|------------|")
    if sg is not None:
        a = "📈 Strong" if sg > 15 else ("📌 Moderate" if sg > 5 else "📉 Slow/Negative")
        lines.append(f"| Revenue Growth | {sg:.1f}% | {a} |")
    if pg is not None:
        a = "📈 Strong" if pg > 20 else ("📌 Moderate" if pg > 5 else "📉 Weak/Negative")
        lines.append(f"| Profit Growth | {pg:.1f}% | {a} |")
    if rev:
        lines.append(f"| Revenue | {_fmt_currency(rev)} | |")
    if np_val:
        lines.append(f"| Net Profit | {_fmt_currency(np_val)} | |")
    if roe:
        lines.append(f"| ROE | {roe:.1f}% | {'Efficient' if roe > 15 else 'Average'} |")
    if npm:
        lines.append(f"| Net Margin | {npm:.1f}% | {'Strong' if npm > 15 else 'Average'} |")
    lines.append("")
    if sg is not None and pg is not None:
        if sg > 15 and pg > 20:
            lines.append("🚀 **Growth Rating**: ⭐⭐⭐⭐⭐ **Exceptional** – Both top-line and bottom-line growing rapidly.")
        elif sg > 10 and pg > 10:
            lines.append("📈 **Growth Rating**: ⭐⭐⭐⭐ **Strong** – Solid and consistent growth trajectory.")
        elif sg > 0 and pg > 0:
            lines.append("📊 **Growth Rating**: ⭐⭐⭐ **Moderate** – Growing but at a measured pace.")
        else:
            lines.append("📉 **Growth Rating**: ⭐⭐ **Slow** – Growth has stalled or is declining.")
        if pg and sg and sg > 0 and pg > sg:
            lines.append(f"✅ Profit growing faster than revenue ({pg:.0f}% vs {sg:.0f}%) — margins are expanding!")
        elif pg and sg and sg > 0 and pg < sg:
            lines.append(f"⚠️ Revenue growing faster than profit — margins may be under pressure.")
    return "\n".join(lines) + DISCLAIMER


def _profitability_query(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify a stock to check profitability." + DISCLAIMER
    name = instrument_data.get("name", "This stock")
    lines = [f"💰 **Profitability Analysis: {name}**\n"]
    if not fundamentals:
        lines.append("No fundamental data available.")
        return "\n".join(lines) + DISCLAIMER
    npm = fundamentals.get("net_profit_margin")
    roe = fundamentals.get("roe")
    roce = fundamentals.get("roce")
    np_val = fundamentals.get("net_profit")
    rev = fundamentals.get("revenue")
    lines.append("| Metric | Value | Rating |")
    lines.append("|--------|-------|--------|")
    if npm is not None:
        r = "📈 Excellent" if npm > 20 else ("📈 Good" if npm > 10 else ("📌 Average" if npm > 0 else "📉 Loss-making"))
        lines.append(f"| Net Profit Margin | {npm:.1f}% | {r} |")
    if roe is not None:
        r = "📈 Excellent" if roe > 20 else ("📌 Average" if roe > 10 else "📉 Poor")
        lines.append(f"| Return on Equity | {roe:.1f}% | {r} |")
    if roce is not None:
        r = "📈 Excellent" if roce > 25 else ("📌 Good" if roce > 12 else "📉 Weak")
        lines.append(f"| Return on Capital | {roce:.1f}% | {r} |")
    if rev: lines.append(f"| Revenue | {_fmt_currency(rev)} | |")
    if np_val: lines.append(f"| Net Profit | {_fmt_currency(np_val)} | {'Profitable ✅' if np_val > 0 else 'Loss-making ❌'} |")
    lines.append("")
    if npm and npm > 15 and roe and roe > 18:
        lines.append("🏆 This company has **excellent profitability** — high margins + high returns on equity. A quality compounder.")
    elif npm and npm > 0 and roe and roe > 10:
        lines.append("✅ Decent profitability. The company generates healthy returns for shareholders.")
    elif npm and npm < 0:
        lines.append("⚠️ The company is **currently unprofitable**. Evaluate if it's a turnaround play or a structural issue.")
    return "\n".join(lines) + DISCLAIMER


def _dividend_query(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify a stock to check dividend information." + DISCLAIMER
    name = instrument_data.get("name", "This stock")
    lines = [f"💸 **Dividend Insights: {name}**\n"]
    # We don't have explicit dividend data in the model, but we can infer
    npm = fundamentals.get("net_profit_margin") if fundamentals else None
    roe = fundamentals.get("roe") if fundamentals else None
    de = fundamentals.get("debt_to_equity") if fundamentals else None
    lines.append("*Note: Detailed dividend history is not currently tracked in our database. Here's what we can infer from fundamentals:*\n")
    if npm and npm > 15 and de is not None and de < 0.5:
        lines.append("✅ **High dividend potential** — Strong margins and low debt suggest capacity to pay regular dividends.")
    elif npm and npm > 5:
        lines.append("📌 **Moderate dividend capacity** — Company is profitable but may prioritize reinvestment.")
    else:
        lines.append("⚠️ **Low dividend likelihood** — Thin margins suggest limited dividend capacity.")
    lines.append("\n**Tips for dividend investors**:")
    lines.append("• Look for consistent dividend history (check annual reports)")
    lines.append("• Dividend yield = Annual Dividend / Current Price × 100")
    lines.append("• High D/E companies may cut dividends during downturns")
    risk = _risk_label(user_profile)
    if risk == "conservative":
        lines.append(f"\n💡 For your **conservative** profile, dividend stocks provide steady income and lower volatility.")
    return "\n".join(lines) + DISCLAIMER


def _promoter_query(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    if not instrument_data:
        return "Please specify a stock to check promoter/ownership info." + DISCLAIMER
    name = instrument_data.get("name", "This stock")
    ph = fundamentals.get("promoter_holding") if fundamentals else None
    lines = [f"👥 **Ownership Analysis: {name}**\n"]
    if ph is not None:
        lines.append(f"**Promoter Holding**: {ph:.1f}%")
        if ph > 70: lines.append("→ ✅ Very high promoter confidence — strong insider alignment.")
        elif ph > 50: lines.append("→ ✅ Healthy promoter stake — management has significant skin in the game.")
        elif ph > 30: lines.append("→ 📌 Moderate promoter holding — institutional and public investors hold significant stakes.")
        else: lines.append("→ ⚠️ Low promoter holding — higher risk of management changes or hostile actions.")
        lines.append(f"\n**Approximate Public/Institutional**: {100-ph:.1f}%")
    else:
        lines.append("Promoter holding data is not available for this instrument.")
    lines.append("\n**Key ownership signals to watch**:")
    lines.append("• Rising promoter holding = Positive (management buying their own stock)")
    lines.append("• Falling promoter holding = Caution (could signal lack of confidence)")
    lines.append("• Pledging of promoter shares = Red flag (high risk)")
    return "\n".join(lines) + DISCLAIMER


def _investment_timing(instrument_data: dict, fundamentals: dict, user_profile: dict) -> str:
    lines = ["⏰ **Investment Timing Insights**\n"]
    lines.append("**Key Principle**: *Time in the market beats timing the market.*\n")
    if instrument_data:
        name = instrument_data.get("name", "This stock")
        price = instrument_data.get("current_price", 0)
        high52 = instrument_data.get("high_52w", 0)
        low52 = instrument_data.get("low_52w", 0)
        if high52 and low52 and high52 != low52:
            range_pos = ((price - low52) / (high52 - low52) * 100) if price else 50
            lines.append(f"**{name}** is currently at **{range_pos:.0f}%** of its 52-week range.\n")
            if range_pos < 25:
                lines.append("📉 Near 52W lows — could be a value entry if fundamentals are strong.")
                lines.append("• Check if the drop is due to temporary or structural issues")
                lines.append("• Consider a staggered entry (buy in 3-4 tranches)")
            elif range_pos > 75:
                lines.append("📈 Near 52W highs — momentum is strong but risk of pullback exists.")
                lines.append("• Wait for a 5-10% correction for a better entry point")
                lines.append("• Or use SIP approach to average out volatility")
            else:
                lines.append("📊 Mid-range — neither at extremes.")
                lines.append("• Good time for a partial position if fundamentals support it")
    lines.append("\n**General timing strategies**:")
    lines.append("• **SIP** (Systematic Investment Plan) — Best for most investors, removes timing risk")
    lines.append("• **Staggered entry** — Split your investment into 3-4 equal parts over weeks")
    lines.append("• **Correction buying** — Keep cash ready, deploy during 5-10% market dips")
    lines.append("• **Avoid** — Buying in FOMO during rapid rallies or panic selling during crashes")
    return "\n".join(lines) + DISCLAIMER


def _etf_fund_query(instrument_data: dict, user_profile: dict) -> str:
    risk = _risk_label(user_profile)
    lines = ["📦 **ETFs & Mutual Fund Guide**\n"]
    if instrument_data and instrument_data.get("type") in ("etf", "fund"):
        name = instrument_data.get("name", "This fund")
        lines.append(f"**{name}** is a {instrument_data.get('type', 'fund').upper()}.\n")
    lines.append("**Types of Funds for You**:\n")
    if risk == "conservative":
        lines.append("| Fund Type | Risk | Suggestion |")
        lines.append("|-----------|------|------------|")
        lines.append("| Liquid/Overnight | 📈 Very Low | Park emergency fund |")
        lines.append("| Debt/Gilt | 📈 Low | Stable returns, low risk |")
        lines.append("| Large Cap Index | 📌 Moderate | NIFTY 50 for equity exposure |")
        lines.append("| ELSS | 📌 Moderate | Tax saving with 3-year lock-in |")
    elif risk == "aggressive":
        lines.append("| Fund Type | Risk | Suggestion |")
        lines.append("|-----------|------|------------|")
        lines.append("| Small Cap Fund | 📉 High | High growth potential |")
        lines.append("| Mid Cap Fund | 🟠 Medium-High | Growth with moderate risk |")
        lines.append("| Sectoral/Thematic | 🟠 High | Concentrated bets on sectors |")
        lines.append("| International | 📌 Moderate | Geographic diversification |")
    else:
        lines.append("| Fund Type | Risk | Suggestion |")
        lines.append("|-----------|------|------------|")
        lines.append("| Flexi Cap | 📌 Moderate | Fund manager picks across caps |")
        lines.append("| Large & Mid Cap | 📌 Moderate | Balanced growth + stability |")
        lines.append("| NIFTY Next 50 | 📌 Moderate | Emerging large caps |")
        lines.append("| Balanced Advantage | 📈 Low-Med | Auto equity-debt allocation |")
    lines.append("\n💡 **Pro Tips**: Start with SIP, prefer Direct plans over Regular, check expense ratio (lower is better).")
    return "\n".join(lines) + DISCLAIMER


def _tax_query(user_profile: dict) -> str:
    lines = ["🧾 **Tax Guide for Investors**\n"]
    lines.append("| Holding Period | Tax Type | Rate |")
    lines.append("|---------------|----------|------|")
    lines.append("| Equity < 1 year | STCG | 15% |")
    lines.append("| Equity > 1 year | LTCG | 10% (above ₹1L) |")
    lines.append("| Debt Fund < 3 years | STCG | As per slab |")
    lines.append("| Debt Fund > 3 years | LTCG | 20% with indexation |")
    lines.append("")
    lines.append("**Tax-Saving Investments (Section 80C)**:")
    lines.append("• **ELSS Funds** — 3-year lock-in, up to ₹1.5L deduction")
    lines.append("• **PPF** — 15-year, guaranteed returns, exempt-exempt-exempt")
    lines.append("• **NPS** — Additional ₹50K under 80CCD(1B)")
    lines.append("\n**Tax Optimization Tips**:")
    lines.append("• Hold equity investments for >1 year to get LTCG benefits")
    lines.append("• Harvest losses before March 31 to offset gains")
    lines.append("• Use ₹1L LTCG exemption each year (sell and rebuy winners)")
    return "\n".join(lines) + DISCLAIMER


def _ipo_query(user_profile: dict) -> str:
    lines = ["🎯 **IPO Guide**\n"]
    lines.append("*Note: Live IPO data is not currently tracked. Here are general guidelines:*\n")
    lines.append("**Should you invest in IPOs?**\n")
    risk = _risk_label(user_profile)
    if risk == "conservative":
        lines.append("⚠️ As a **conservative** investor, be selective with IPOs. Prefer established companies with proven track records.")
    elif risk == "aggressive":
        lines.append("✅ IPOs can offer listing gains, but research the company thoroughly before subscribing.")
    lines.append("\n**IPO Checklist**:")
    lines.append("• Read the DRHP (Draft Red Herring Prospectus)")
    lines.append("• Check promoter background and track record")
    lines.append("• Compare PE with listed peers — is it priced at a premium?")
    lines.append("• Review financials — revenue growth, profitability, debt")
    lines.append("• Grey market premium (GMP) indicates market sentiment")
    lines.append("• Don't subscribe just for listing gains — think long-term")
    return "\n".join(lines) + DISCLAIMER


# ═══════════════════════════════════════════════════════════════
#  GENERATIVE RESPONSE COMPOSER (Dynamic Fallback)
# ═══════════════════════════════════════════════════════════════

def _dynamic_instrument_response(instrument_data: dict, fundamentals: dict, user_profile: dict, message: str) -> str:
    """
    Generative-style response composer: dynamically builds an intelligent
    answer from ALL available instrument data for any unrecognized question.
    """
    if not instrument_data:
        return _general_response(instrument_data, fundamentals, user_profile, message)

    name = instrument_data.get("name", "This stock")
    symbol = instrument_data.get("symbol", "")
    msg = message.lower()
    risk = _risk_label(user_profile)

    # Dynamically compose a comprehensive answer from available data
    lines = [f"📊 **About {name}** ({symbol})\n"]
    lines.append(f"*Based on your question: \"{message}\"*\n")

    # Always include current price context
    price = instrument_data.get("current_price")
    pct = instrument_data.get("day_change_pct", 0)
    if price:
        emoji = "📈" if pct >= 0 else "📉"
        lines.append(f"**Current Price**: {_fmt_currency(price)} {emoji} {_fmt_pct(pct)} today\n")

    # Build data sections based on what's available
    data_sections = []

    if fundamentals:
        metrics = []
        for label, key, suffix in [
            ("PE Ratio", "pe", ""), ("PB Ratio", "pb", ""), ("ROE", "roe", "%"),
            ("ROCE", "roce", "%"), ("EPS", "eps", ""), ("Debt/Equity", "debt_to_equity", ""),
            ("Net Margin", "net_profit_margin", "%"), ("Sales Growth", "sales_growth", "%"),
            ("Profit Growth", "profit_growth", "%"), ("Promoter Holding", "promoter_holding", "%"),
        ]:
            val = fundamentals.get(key)
            if val is not None:
                metrics.append((label, f"{float(val):.2f}{suffix}"))
        if metrics:
            data_sections.append("**Key Fundamentals**:")
            data_sections.append("| Metric | Value |")
            data_sections.append("|--------|-------|")
            for label, val in metrics:
                data_sections.append(f"| {label} | {val} |")

    # Add intelligent commentary based on available data
    commentary = []
    if fundamentals:
        pe = fundamentals.get("pe")
        roe = fundamentals.get("roe")
        de = fundamentals.get("debt_to_equity")
        sg = fundamentals.get("sales_growth")
        pg = fundamentals.get("profit_growth")
        npm = fundamentals.get("net_profit_margin")

        if pe: commentary.append(f"{'Attractively' if pe < 20 else 'Expensively' if pe > 40 else 'Fairly'} valued at PE {pe:.1f}")
        if roe: commentary.append(f"{'Excellent' if roe > 20 else 'Good' if roe > 12 else 'Weak'} returns on equity ({roe:.1f}%)")
        if de is not None: commentary.append(f"{'Very low' if de < 0.3 else 'Moderate' if de < 1 else 'High'} debt levels (D/E: {de:.2f})")
        if sg: commentary.append(f"Revenue {'growing strongly' if sg > 15 else 'growing steadily' if sg > 0 else 'declining'} at {sg:.1f}%")
        if npm: commentary.append(f"{'Strong' if npm > 15 else 'Moderate' if npm > 5 else 'Thin'} profit margins ({npm:.1f}%)")

    if data_sections:
        lines.extend(data_sections)
        lines.append("")

    if commentary:
        lines.append("**My Assessment**:")
        for c in commentary:
            lines.append(f"• {c}")

    # Personalized suitability note
    lines.append(f"\n**For Your Profile** ({risk.title()} risk, {_experience_label(user_profile).title()}):")
    suit = _suitability_score(instrument_data, fundamentals or {}, user_profile)
    lines.append(f"Suitability: **{suit['verdict']}** ({suit['score']}/100)")
    if suit["reasons"]:
        lines.append(f"  ✅ {suit['reasons'][0]}")
    if suit["warnings"]:
        lines.append(f"  ⚠️ {suit['warnings'][0]}")

    return "\n".join(lines) + DISCLAIMER


def _general_response(instrument_data: dict, fundamentals: dict, user_profile: dict, message: str) -> str:
    """Ultimate fallback – conversational and helpful guidance without an instrument context."""
    name = (user_profile.get("name") or "").split()[0] or "there"
    
    # Try to provide a conversational answer instead of just a menu
    msg = message.lower()
    
    if any(w in msg for w in ['hello', 'hi', 'hey', 'morning']):
        return f"Hi {name}! I'm FinSight AI. I can analyze stocks, review your portfolio, or explain financial concepts. How can I assist you today?"
        
    if 'you' in msg and ('are' in msg or 'who' in msg):
        return f"I'm FinSight AI, your personal financial assistant. While I'm currently running in basic mode, I can still analyze fundamental metrics for any stock on our platform. Just ask me about a specific company or open a stock detail page!"
        
    if 'market' in msg:
        return "The market is constantly moving! While I don't have live intraday commentary at the moment, you can check the 'Market Overview' on your dashboard to see top gainers, losers, and NIFTY 50 performance."

    lines = [f"I understand you're asking about **\"{message}\"**.\n"]
    lines.append(f"To give you the best analysis, I work best when you ask about specific stocks or your portfolio. For example, you can try:")
    lines.append("• *\"How is my portfolio doing?\"*")
    lines.append("• *\"Tell me about Reliance Industries\"*")
    lines.append("• *\"Is TCS undervalued right now?\"*")
    lines.append("\nTip: Navigate to any stock's detail page and ask me questions there. I'll automatically analyze its fundamentals for you!")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  MAIN SERVICE CLASS
# ═══════════════════════════════════════════════════════════════

class StubChatbotService:
    """
    Comprehensive rule-based AI engine with generative-style response
    composition. Handles 25+ intent categories and dynamically composes
    intelligent answers from available data for any unrecognized question.
    """

    def get_response(
        self,
        instrument_data: dict,
        user_profile: dict,
        message: str,
        context: dict | None = None,
    ) -> str:
        """Generate a personalized response based on intent, user profile, and context."""
        context = context or {}
        fundamentals = context.get("fundamentals")
        intent = detect_intent(message)

        # Route to appropriate handler
        handlers = {
            "greeting": lambda: _greet(user_profile, context),
            "portfolio_summary": lambda: _portfolio_summary(user_profile, context),
            "portfolio_advice": lambda: _portfolio_advice(user_profile, context),
            "risk_assessment": lambda: _risk_assessment(user_profile, context),
            "watchlist_insight": lambda: _watchlist_insight(user_profile, context),
            "stock_analysis": lambda: _stock_analysis(instrument_data, fundamentals, user_profile),
            "stock_comparison": lambda: _stock_comparison(instrument_data, user_profile),
            "suitability_check": lambda: _suitability_check(instrument_data, fundamentals, user_profile),
            "price_query": lambda: _price_query(instrument_data, fundamentals, user_profile),
            "valuation_analysis": lambda: _valuation_analysis(instrument_data, fundamentals, user_profile),
            "growth_analysis": lambda: _growth_analysis(instrument_data, fundamentals, user_profile),
            "profitability_query": lambda: _profitability_query(instrument_data, fundamentals, user_profile),
            "dividend_query": lambda: _dividend_query(instrument_data, fundamentals, user_profile),
            "promoter_query": lambda: _promoter_query(instrument_data, fundamentals, user_profile),
            "sector_analysis": lambda: _sector_analysis(instrument_data, user_profile, context),
            "debt_analysis": lambda: _debt_analysis(instrument_data, fundamentals, user_profile),
            "fundamentals_query": lambda: _fundamentals_query(instrument_data, fundamentals, user_profile),
            "goal_planning": lambda: _goal_planning(user_profile, context),
            "income_advice": lambda: _income_advice(user_profile, context),
            "screener_suggestion": lambda: _screener_suggestion(user_profile, context),
            "market_overview": lambda: _market_overview(user_profile, context),
            "investment_timing": lambda: _investment_timing(instrument_data, fundamentals, user_profile),
            "etf_fund_query": lambda: _etf_fund_query(instrument_data, user_profile),
            "tax_query": lambda: _tax_query(user_profile),
            "ipo_query": lambda: _ipo_query(user_profile),
            "dynamic_instrument": lambda: _dynamic_instrument_response(instrument_data, fundamentals, user_profile, message),
        }

        handler = handlers.get(intent)
        if handler:
            return handler()
        return _dynamic_instrument_response(instrument_data, fundamentals, user_profile, message)

    def get_suggestions(
        self,
        user_profile: dict,
        instrument_data: dict | None = None,
        context: dict | None = None,
    ) -> list[str]:
        """Return context-aware suggestion chips covering all question categories."""
        context = context or {}
        pool = []

        # Portfolio suggestions (always)
        pool.append("How is my portfolio doing?")

        if instrument_data:
            name = instrument_data.get("name", "this stock")
            short = name if len(name) < 25 else instrument_data.get("symbol", name)
            # Instrument-specific suggestions
            inst_ideas = [
                f"Is {short} good for me?",
                f"Is {short} overvalued or undervalued?",
                f"Show {short}'s growth analysis",
                f"Is {short} profitable?",
                f"Check {short}'s debt level",
                f"What's the price of {short}?",
                f"Who owns {short}?",
                f"When should I buy {short}?",
                f"Does {short} pay dividends?",
                f"Analyze {short}'s fundamentals",
            ]
            random.shuffle(inst_ideas)
            pool.extend(inst_ideas[:4])
        else:
            pool.append("Analyze my watchlist")
            pool.append("Assess my portfolio risk")

        # Profile-driven suggestions
        risk = _risk_label(user_profile)
        if risk == "conservative":
            pool.append("Find me safe blue-chip stocks")
        elif risk == "aggressive":
            pool.append("Find me high-growth stocks")
        else:
            pool.append("Suggest stocks for me")

        # Rotating general suggestions
        general = [
            "How's the market today?",
            "How to save tax on investments?",
            "Best mutual funds for me",
            "When is the right time to invest?",
            "What are IPOs?",
        ]
        random.shuffle(general)
        pool.extend(general[:2])

        goals = user_profile.get("goals", "")
        if goals:
            pool.append(f"Help me plan for {goals.split(',')[0].strip()}")

        return pool[:8]  # Show up to 8 suggestions


class GeminiChatbotService:
    """
    Real AI chatbot using Google Gemini API (free tier).
    Builds a rich system prompt from user context and sends to Gemini.
    Falls back to StubChatbotService on any API error.
    """

    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model = Config.GEMINI_MODEL
        self._stub = StubChatbotService()

    def _build_system_prompt(self, instrument_data, user_profile, context):
        """Build a comprehensive system prompt with all available context."""
        parts = [
            "You are FinSight AI, an expert financial assistant for Indian stock markets.",
            "You provide personalized, educational financial insights. You NEVER give buy/sell recommendations — only analysis and education.",
            "Always end with a brief disclaimer that this is educational only, not investment advice.",
            "Format your responses in markdown with **bold**, tables, and bullet points for readability.",
            "Keep responses concise but informative (max 300 words). Use emojis sparingly for visual indicators (📈📉✅⚠️).",
            ""
        ]

        # User profile context
        if user_profile:
            name = user_profile.get("name", "User")
            parts.append(f"## User Profile")
            parts.append(f"- Name: {name}")
            if user_profile.get("age"): parts.append(f"- Age: {user_profile['age']}")
            if user_profile.get("risk_profile"): parts.append(f"- Risk Profile: {user_profile['risk_profile']}")
            if user_profile.get("experience_level"): parts.append(f"- Experience: {user_profile['experience_level']}")
            if user_profile.get("goals"): parts.append(f"- Investment Goals: {user_profile['goals']}")
            if user_profile.get("occupation"): parts.append(f"- Occupation: {user_profile['occupation']}")
            if user_profile.get("monthly_investment_capacity"):
                parts.append(f"- Monthly Investment Capacity: ₹{user_profile['monthly_investment_capacity']}")
            parts.append("")

        # Instrument context
        if instrument_data:
            parts.append(f"## Current Instrument Context")
            for key in ["name", "symbol", "sector", "current_price", "day_change_pct",
                         "market_cap", "high_52w", "low_52w", "pe", "pb", "roe", "roce",
                         "debt_to_equity", "net_profit_margin", "sales_growth", "profit_growth",
                         "promoter_holding", "eps"]:
                val = instrument_data.get(key)
                if val is not None:
                    parts.append(f"- {key}: {val}")
            parts.append("")

        # Portfolio context
        context = context or {}
        positions = context.get("positions", [])
        if positions:
            parts.append(f"## User's Portfolio ({len(positions)} holdings)")
            for p in positions[:10]:  # Limit to avoid token overflow
                sym = p.get("symbol", p.get("name", "N/A"))
                qty = p.get("quantity", 0)
                buy = p.get("buy_price", 0)
                cur = p.get("current_price", 0)
                pl = p.get("unrealized_pl", 0)
                parts.append(f"- {sym}: {qty} shares, buy ₹{buy}, current ₹{cur}, P&L ₹{pl}")
            parts.append("")

        # Watchlist context
        watchlists = context.get("watchlists", [])
        if watchlists:
            all_items = [item for wl in watchlists for item in wl.get("items", [])]
            if all_items:
                parts.append(f"## User's Watchlist ({len(all_items)} stocks)")
                for item in all_items[:8]:
                    parts.append(f"- {item.get('symbol', 'N/A')}: ₹{item.get('current_price', 'N/A')} ({item.get('day_change_pct', 0):+.2f}%)")
                parts.append("")

        # Sector overview
        sectors = context.get("sectors", [])
        if sectors:
            top3 = sorted(sectors, key=lambda s: s.get("avg_day_change_pct", 0), reverse=True)[:3]
            if top3:
                parts.append("## Top Sectors Today")
                for s in top3:
                    parts.append(f"- {s.get('sector', 'N/A')}: {s.get('avg_day_change_pct', 0):+.2f}%")
                parts.append("")

        return "\n".join(parts)

    def get_response(
        self, instrument_data: dict, user_profile: dict, message: str,
        context: dict | None = None,
    ) -> str:
        import urllib.request
        import json as _json

        try:
            system_prompt = self._build_system_prompt(instrument_data, user_profile, context)

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": system_prompt + "\n\n---\n\nUser question: " + message}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                },
                "safetySettings": [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            }

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            req = urllib.request.Request(
                url,
                data=_json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                result = _json.loads(resp.read().decode("utf-8"))

            # Extract text from response
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "I couldn't generate a response. Please try again.")

            return "I couldn't generate a response. Please try again."

        except Exception as e:
            print(f"[Gemini API Error] {e} — falling back to rule-based engine")
            return self._stub.get_response(instrument_data, user_profile, message, context)

    def get_suggestions(self, user_profile, instrument_data=None, context=None):
        return self._stub.get_suggestions(user_profile, instrument_data, context)


class RealChatbotService:
    """
    Placeholder for real LLM integration (OpenAI / Anthropic).
    Implement using httpx to call OpenAI / Anthropic API.
    """

    def __init__(self):
        self.api_key = Config.LLM_API_KEY
        self.model = Config.LLM_MODEL
        self.base_url = Config.LLM_API_BASE_URL

    def get_response(
        self, instrument_data: dict, user_profile: dict, message: str,
        context: dict | None = None,
    ) -> str:
        raise NotImplementedError("Connect a real LLM provider")

    def get_suggestions(self, user_profile, instrument_data=None, context=None):
        return StubChatbotService().get_suggestions(user_profile, instrument_data, context)


def get_chatbot_service():
    """Factory: return the configured chatbot service."""
    # Auto-detect Gemini if key is present
    if Config.GEMINI_API_KEY:
        return GeminiChatbotService()
    if Config.LLM_PROVIDER == "gemini" and Config.GEMINI_API_KEY:
        return GeminiChatbotService()
    if Config.LLM_PROVIDER == "stub":
        return StubChatbotService()
    return RealChatbotService()
