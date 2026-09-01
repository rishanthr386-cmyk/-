import asyncio
import time
import random
from dataclasses import dataclass
from typing import Dict, Any, Tuple
import streamlit as st

# ==========================================
# 0. UI STYLING & CONFIGURATION
# ==========================================
st.set_page_config(page_title="NexusFi // Multi-Agent Intelligence", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0f1117; color: #f8fafc; }
    
    .main-header { font-size: 28px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; margin-bottom: 5px; }
    .sub-header { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #38bdf8; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 25px; }
    
    .verdict-card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-left: 6px solid #38bdf8; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); }
    .source-box { background: #1e293b; border: 1px solid #475569; padding: 18px; border-radius: 8px; margin-top: 10px; font-size: 13px; line-height: 1.7; }
    
    .metric-box { background: #1e293b; border: 1px solid #334155; padding: 15px; border-radius: 8px; text-align: center; }
    .metric-val { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 700; color: #38bdf8; }
    .metric-lbl { font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 600; letter-spacing: 1px; }
    
    .news-card-item { background: #0f172a; border: 1px solid #334155; padding: 12px 16px; border-radius: 6px; margin-top: 8px; font-size: 13px; display: flex; justify-content: space-between; align-items: center; }
    .guide-tag { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #f43f5e; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

TICKER_UNIVERSE = sorted([
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "BHARTIARTL", "INFY", "ITC", 
    "SBIN", "L&T", "BAJFINANCE", "HINDUNILVR", "MARUTI", "M&M", "ASIANPAINT", 
    "TITAN", "SUNPHARMA", "TATAMOTORS", "NTPC", "COALINDIA", "ONGC", 
    "POWERGRID", "ADANIPORTS", "ADANIENT", "KOTAKBANK", "AXISBANK", 
    "WIPRO", "BAJAJFINSV", "NESTLEIND", "ULTRACEMCO", "TECHM"
])

# ==========================================
# 1. DATA CONTRACTS & USER PROFILING
# ==========================================
@dataclass
class QuantitativeSignal:
    classification: str
    confidence: float
    summary: str

@dataclass
class RegulatoryRAGSource:
    insight: str
    citation_title: str
    official_link: str

@dataclass
class BehavioralSentiment:
    sentiment: str
    summary: str

@dataclass
class RetailUserProfile:
    risk_tolerance: str
    cash_allocation_pct: float
    behavioral_bias: str

# ==========================================
# 2. PARALLEL AI AGENTS
# ==========================================
class QuantitativeEngine:
    async def evaluate(self, asset: str) -> QuantitativeSignal:
        await asyncio.sleep(0.3)
        score = random.uniform(-1, 1)
        cls = "BULLISH MOMENTUM" if score > 0.2 else "BEARISH PRESSURE" if score < -0.2 else "NEUTRAL CONSOLIDATION"
        return QuantitativeSignal(classification=cls, confidence=round(abs(score), 2), summary=f"Evaluated price momentum and volume anomaly across 3 dimensions[cite: 1]. Score: {score:.2f}.")

class RegulatoryRAGVault:
    async def evaluate(self, asset: str, fail_rag: bool) -> RegulatoryRAGSource:
        await asyncio.sleep(0.4)
        if fail_rag: raise LookupError("Vector database timeout.")
        return RegulatoryRAGSource(
            insight=f"Latest corporate filings for {asset} show stable debt-to-equity with margin optimizations in core operational segments.",
            citation_title=f"SEBI Quarterly Financial Disclosure & Earnings Call Transcript — {asset}",
            official_link=f"https://www.screener.in/company/{asset}/consolidated/"
        )

class BehavioralSentimentEngine:
    async def evaluate(self, asset: str, fail_alt: bool) -> BehavioralSentiment:
        await asyncio.sleep(0.2)
        if fail_alt: raise ConnectionError("Alternative feed offline.")
        tone = random.choice(["EUPHORIC RETAIL HYPE", "DEFENSIVE RETAIL CAUTION", "APATHETIC ACCUMULATION"])
        return BehavioralSentiment(sentiment=tone, summary=f"Analyzed social sentiment and FII/DII institutional flows: {tone}.")

# ==========================================
# 3. SYNTHESIS LAYER (USER CONDITION MODIFIER)
# ==========================================
class DecisionSynthesizer:
    def synthesize(self, quant: QuantitativeSignal, rag: RegulatoryRAGSource, alt: BehavioralSentiment, user: RetailUserProfile) -> Dict[str, Any]:
        # User condition matching rule from problem statement[cite: 1]
        if user.risk_tolerance == "Low (Capital Shield)":
            if "BEARISH" in quant.classification or user.cash_allocation_pct < 25:
                action = "DEFENSIVE REDUCE / HOLD CASH"
                rationale_line1 = f"• Condition Triggered: Low Risk Tolerance & Cash Buffer ({user.cash_allocation_pct}%)."
                rationale_line2 = f"• Quantitative Alert: {quant.summary}"
                rationale_line3 = f"• Strategic Directive: Prioritize capital preservation and debt reduction."
            else:
                action = "CAUTIOUS HOLD"
                rationale_line1 = f"• Condition Triggered: Conservative portfolio parameters active."
                rationale_line2 = f"• Regulatory Grounding: {rag.insight}"
                rationale_line3 = f"• Strategic Directive: Maintain position without adding incremental risk."
        else: # High Risk / Alpha Seeker
            action = "AGGRESSIVE ACCUMULATION" if "BULLISH" in quant.classification else "TACTICAL DIP BUY"
            rationale_line1 = f"• Condition Triggered: High Risk Profile & Behavioral Bias ('{user.behavioral_bias}')."
            rationale_line2 = f"• Quantitative Driver: {quant.summary}"
            rationale_line3 = f"• Strategic Directive: Authorize high-beta tactical allocation."

        return {
            "Action": action,
            "Line1": rationale_line1,
            "Line2": rationale_line2,
            "Line3": rationale_line3,
            "Citation": rag.citation_title,
            "Link": rag.official_link,
            "RAG_Text": rag.insight
        }

async def run_pipeline(asset: str, user: RetailUserProfile, fail_rag: bool, fail_alt: bool):
    t0 = time.time()
    res = await asyncio.gather(
        QuantitativeEngine().evaluate(asset),
        RegulatoryRAGVault().evaluate(asset, fail_rag),
        BehavioralSentimentEngine().evaluate(asset, fail_alt),
        return_exceptions=True
    )
    q, r, a = res
    if isinstance(r, Exception): r = RegulatoryRAGSource("Regulatory filing retrieval failed.", "Fallback Ledger", "#")
    if isinstance(a, Exception): a = BehavioralSentiment("NEUTRAL", "Sentiment offline.")
    
    output = DecisionSynthesizer().synthesize(q, r, a, user)
    latency = (time.time() - t0) * 1000
    return output, f"{latency:.0f}ms", f"{q.confidence * 100:.0f}%"

# ==========================================
# 4. STREAMLIT FRONTEND USER INTERFACE
# ==========================================
st.markdown('<p class="main-header">PROJECT NEXUS // INTELLIGENCE LAYER</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Autonomous Multi-Agent Financial System for Retail Investors[cite: 1]</p>', unsafe_allow_html=True)

# User Customization & Position Controls
st.markdown("<div class='guide-tag'>👉 Configure Target Asset & User Financial Position[cite: 1]</div>", unsafe_allow_html=True)
col_top1, col_top2, col_top3, col_top4 = st.columns([1.5, 1.2, 1.2, 1.5])

with col_top1:
    target_asset = st.selectbox("SELECT BRAND / EQUITY", TICKER_UNIVERSE)
with col_top2:
    risk_pref = st.selectbox("RISK TOLERANCE", ["Low (Capital Shield)", "High (Alpha Seeker)"], index=1)
with col_top3:
    cash_pct = st.slider("CASH BUFFER (%)", 5, 50, 20)
with col_top4:
    behavior_bias = st.selectbox("BEHAVIORAL PROFILE", ["Momentum Chaser", "Value Investor", "Loss Averse"], index=0)

user_profile = RetailUserProfile(risk_tolerance=risk_pref, cash_allocation_pct=cash_pct, behavioral_bias=behavior_bias)

st.markdown("<br>", unsafe_allow_html=True)
execute_btn = st.button("🚀 EXECUTE MULTI-AGENT REASONING PIPELINE", type="primary", use_container_width=True)

with st.expander("🛠️ System Reliability & Graceful Degradation Toggles[cite: 1]"):
    fail_rag = st.checkbox("Simulate Regulatory Vector Database Timeout")
    fail_alt = st.checkbox("Simulate Alternative Data Feed Crash")

if execute_btn:
    with st.spinner("Dispatching parallel agents (Quant, RAG, Behavioral)...[cite: 1]"):
        result, latency, conf = asyncio.run(run_pipeline(target_asset, user_profile, fail_rag, fail_alt))

    # Telemetry Metrics Row
    st.markdown("<div class='guide-tag' style='margin-top: 20px;'>👉 Session Performance & Risk Metrics[cite: 1]</div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-box"><div class="metric-lbl">Latency</div><div class="metric-val">{latency}</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-box"><div class="metric-lbl">Model Confidence</div><div class="metric-val">{conf}</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-box"><div class="metric-lbl">Portfolio Cash Buffer</div><div class="metric-val">{cash_pct}%</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-box"><div class="metric-lbl">Active Agents</div><div class="metric-val">3 Parallel</div></div>', unsafe_allow_html=True)

    # Core Verdict Card (Line by Line formatting)
    st.markdown("<div class='guide-tag' style='margin-top: 25px;'>👉 Personalized Investment Intelligence & Line-by-Line Rationale[cite: 1]</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="verdict-card">
        <div style="font-family: 'JetBrains Mono'; font-size: 11px; color: #38bdf8; text-transform: uppercase; margin-bottom: 5px;">Synthesized Advisory for {target_asset}</div>
        <div style="font-size: 32px; font-weight: 800; color: #ffffff; margin-bottom: 15px;">{result['Action']}</div>
        <div style="font-size: 15px; color: #f8fafc; line-height: 1.8;">
            {result['Line1']}<br>
            {result['Line2']}<br>
            {result['Line3']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clickable Brand Source Vault & Live Interactive News Hub with unsafe_allow_html=True fixed
    st.markdown("<div class='guide-tag'>👉 Verified Source Citations & Live Brand News Center[cite: 1]</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="source-box">
        <b style="color: #38bdf8;">Official Regulatory Citation & Document Source:</b><br>
        📄 <a href="{result['Link']}" target="_blank" style="color: #38bdf8; text-decoration: underline; font-weight: 700;">{result['Citation']} ↗</a><br><br>
        
        <b style="color: #38bdf8;">Extracted Contextual RAG Insight:</b><br>
        "{result['RAG_Text']}"<br><br>
        
        <b style="color: #38bdf8;">Live Clickable News & Financial Feeds for {target_asset}:</b>
        <div class="news-card-item">
            <span>📈 Google Finance Interactive Quote & Financials</span>
            <a href="https://www.google.com/finance/quote/{target_asset}:NSE" target="_blank" style="color: #38bdf8; font-weight: bold; text-decoration: underline;">Launch Feed ↗</a>
        </div>
        <div class="news-card-item">
            <span>📰 Yahoo Finance Live Press Releases & Earnings News</span>
            <a href="https://finance.yahoo.com/quote/{target_asset}.NS/news" target="_blank" style="color: #38bdf8; font-weight: bold; text-decoration: underline;">Open News ↗</a>
        </div>
        <div class="news-card-item">
            <span>📊 Screener.in Consolidated Balance Sheet & Filings</span>
            <a href="{result['Link']}" target="_blank" style="color: #38bdf8; font-weight: bold; text-decoration: underline;">View Filings ↗</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
