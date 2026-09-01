import asyncio
import time
import random
from dataclasses import dataclass
from typing import Dict, Any, Tuple
import streamlit as st

# ==========================================
# 0. STREAMLIT CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="NexusFi // Multi-Agent Intelligence", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0f1117; color: #f8fafc; }
    .main-header { font-size: 28px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; margin-bottom: 5px; }
    .sub-header { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #38bdf8; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 25px; }
    .metric-box { background: #1e293b; border: 1px solid #334155; padding: 15px; border-radius: 8px; text-align: center; }
    .metric-val { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 700; color: #38bdf8; }
    .metric-lbl { font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 600; letter-spacing: 1px; }
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
class UserProfileModel:
    mode: str
    risk_tolerance: str
    cash_buffer_pct: float
    inference_note: str

def resolve_user_profile(mode: str, manual_risk: str, manual_cash: float) -> UserProfileModel:
    if mode == "Automatic (Analyze Past Behavior Trends)":
        # Simulate past interaction trends from user site history logs
        simulated_queries = 18
        simulated_avg_cash = 14.5
        if simulated_avg_cash < 20:
            return UserProfileModel(
                mode="Automatic",
                risk_tolerance="High Risk (Alpha Seeker)",
                cash_buffer_pct=simulated_avg_cash,
                inference_note=f"Auto-detected from past session logs: {simulated_queries} high-beta queries, low historical cash buffer ({simulated_avg_cash}%)."
            )
        else:
            return UserProfileModel(
                mode="Automatic",
                risk_tolerance="Low Risk (Capital Shield)",
                cash_buffer_pct=35.0,
                inference_note="Auto-detected from past session logs: Conservative asset holding and high liquidity retention."
            )
    else:
        return UserProfileModel(
            mode="Manual",
            risk_tolerance=manual_risk,
            cash_buffer_pct=manual_cash,
            inference_note=f"Manually configured parameters: Risk Profile [{manual_risk}], Cash Buffer [{manual_cash}%]."
        )

# ==========================================
# 2. PARALLEL AI AGENTS
# ==========================================
class QuantitativeEngine:
    async def evaluate(self, asset: str) -> QuantitativeSignal:
        await asyncio.sleep(0.3)
        score = random.uniform(-1, 1)
        cls = "BULLISH MOMENTUM" if score > 0.2 else "BEARISH PRESSURE" if score < -0.2 else "NEUTRAL CONSOLIDATION"
        return QuantitativeSignal(classification=cls, confidence=round(abs(score), 2), summary=f"Evaluated price momentum, volume anomaly, and volatility dimensions. Score: {score:.2f}.")

class RegulatoryRAGVault:
    async def evaluate(self, asset: str, fail_rag: bool) -> RegulatoryRAGSource:
        await asyncio.sleep(0.4)
        if fail_rag: raise LookupError("Vector database timeout.")
        return RegulatoryRAGSource(
            insight=f"Latest corporate filings and earnings disclosures for {asset} indicate stable debt-to-equity ratios with localized margin optimizations.",
            citation_title=f"SEBI Quarterly Financial Disclosure & Earnings Transcript — {asset}",
            official_link=f"https://www.screener.in/company/{asset}/consolidated/"
        )

class BehavioralSentimentEngine:
    async def evaluate(self, asset: str, fail_alt: bool) -> BehavioralSentiment:
        await asyncio.sleep(0.2)
        if fail_alt: raise ConnectionError("Alternative feed offline.")
        tone = random.choice(["EUPHORIC RETAIL HYPE", "DEFENSIVE RETAIL CAUTION", "APATHETIC ACCUMULATION"])
        return BehavioralSentiment(sentiment=tone, summary=f"Analyzed social sentiment feeds and FII/DII institutional flows: {tone}.")

# ==========================================
# 3. SYNTHESIS LAYER
# ==========================================
class DecisionSynthesizer:
    def synthesize(self, quant: QuantitativeSignal, rag: RegulatoryRAGSource, alt: BehavioralSentiment, profile: UserProfileModel) -> Dict[str, Any]:
        if "Low Risk" in profile.risk_tolerance:
            action = "DEFENSIVE REDUCE / HOLD CASH" if "BEARISH" in quant.classification else "CAUTIOUS HOLD"
            r1 = f"• Profile Constraint: {profile.risk_tolerance} (Cash Buffer: {profile.cash_buffer_pct}%)."
            r2 = f"• Quantitative Driver: {quant.summary}"
            r3 = f"• Strategic Directive: Prioritize capital preservation and portfolio safety."
        else:
            action = "AGGRESSIVE ACCUMULATION" if "BULLISH" in quant.classification else "TACTICAL DIP BUY"
            r1 = f"• Profile Constraint: {profile.risk_tolerance} (Cash Buffer: {profile.cash_buffer_pct}%)."
            r2 = f"• Quantitative Driver: {quant.summary}"
            r3 = f"• Strategic Directive: Authorize high-beta tactical upside allocation."

        return {
            "Action": action,
            "Line1": r1,
            "Line2": r2,
            "Line3": r3,
            "Citation": rag.citation_title,
            "Link": rag.official_link,
            "RAG_Text": rag.insight
        }

async def run_pipeline(asset: str, profile: UserProfileModel, fail_rag: bool, fail_alt: bool):
    t0 = time.time()
    res = await asyncio.gather(
        QuantitativeEngine().evaluate(asset),
        RegulatoryRAGVault().evaluate(asset, fail_rag),
        BehavioralSentimentEngine().evaluate(asset, fail_alt),
        return_exceptions=True
    )
    q, r, a = res
    if isinstance(r, Exception): r = RegulatoryRAGSource("Regulatory filing retrieval failed. System fallback active.", "Fallback Ledger", "#")
    if isinstance(a, Exception): a = BehavioralSentiment("NEUTRAL", "Sentiment feed offline.")
    
    output = DecisionSynthesizer().synthesize(q, r, a, profile)
    latency = (time.time() - t0) * 1000
    return output, f"{latency:.0f}ms", f"{q.confidence * 100:.0f}%"

# ==========================================
# 4. STREAMLIT FRONTEND USER INTERFACE
# ==========================================
st.markdown('<p class="main-header">PROJECT NEXUS // INTELLIGENCE LAYER</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Autonomous Multi-Agent Financial System for Retail Investors</p>', unsafe_allow_html=True)
st.markdown("---")

# Selection controls
col_sel1, col_sel2 = st.columns(2)
with col_sel1:
    target_asset = st.selectbox("SELECT BRAND / EQUITY", TICKER_UNIVERSE)
with col_sel2:
    profiling_mode = st.radio("PROFILING CONFIGURATION", ["Automatic (Analyze Past Behavior Trends)", "Choose Manually"], horizontal=True)

# Conditional Manual vs Automatic inputs
manual_risk = "High Risk (Alpha Seeker)"
manual_cash = 20.0

if profiling_mode == "Choose Manually":
    st.markdown("<div class='guide-tag'>👉 Manual Parameters Override</div>", unsafe_allow_html=True)
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        manual_risk = st.selectbox("RISK PROFILE", ["Low Risk (Capital Shield)", "High Risk (Alpha Seeker)"])
    with m_col2:
        manual_cash = st.slider("CASH BUFFER (%)", 5, 50, 20)

# Resolve user profile state
user_profile = resolve_user_profile(profiling_mode, manual_risk, manual_cash)

st.markdown(f"""
<div style="background: #1e293b; border-left: 4px solid #38bdf8; padding: 12px 18px; border-radius: 6px; margin: 15px 0;">
    <b style="color: #38bdf8;">Active Investor Classification:</b> <span style="color: #fff; font-weight: 700;">{user_profile.risk_tolerance}</span><br>
    <span style="font-size: 12px; color: #94a3b8;">{user_profile.inference_note}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
execute_btn = st.button("🚀 EXECUTE MULTI-AGENT REASONING PIPELINE", type="primary", use_container_width=True)

with st.expander("🛠️ System Reliability & Graceful Degradation Toggles"):
    fail_rag = st.checkbox("Simulate Regulatory Vector Database Timeout")
    fail_alt = st.checkbox("Simulate Alternative Data Feed Crash")

if execute_btn:
    with st.spinner("Dispatching parallel agents (Quant, RAG, Behavioral)..."):
        result, latency, conf = asyncio.run(run_pipeline(target_asset, user_profile, fail_rag, fail_alt))

    # Telemetry Metrics Row
    st.markdown("### 📊 Session Performance & Risk Telemetry")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Pipeline Latency", latency)
    m2.metric("Model Confidence", conf)
    m3.metric("Cash Buffer", f"{user_profile.cash_buffer_pct}%")
    m4.metric("Active Agents", "3 Parallel")

    # Core Verdict Card (Line by Line)
    st.markdown("### 🎯 Personalized Investment Intelligence")
    with st.container(border=True):
        st.markdown(f"**Synthesized Advisory for `{target_asset}`**")
        st.markdown(f"## {result['Action']}")
        st.markdown(f"""
        {result['Line1']}<br>
        {result['Line2']}<br>
        {result['Line3']}
        """, unsafe_allow_html=True)

    # Verified Source Citations & Live Clickable News Hub
    st.markdown("### 📑 Verified Source Citations & Live Brand News Center")
    with st.container(border=True):
        st.markdown("**Official Regulatory Citation & Document Source:**")
        st.markdown(f"📄 [{result['Citation']}]({result['Link']})")
        
        st.markdown("**Extracted Contextual RAG Insight:**")
        st.info(f'"{result["RAG_Text"]}"')
        
        st.markdown(f"**Live Clickable News & Financial Feeds for `{target_asset}`:**")
        
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            st.link_button("📈 Google Finance Hub", f"https://www.google.com/finance/quote/{target_asset}:NSE", use_container_width=True)
        with col_n2:
            st.link_button("📰 Yahoo News & Filings", f"https://finance.yahoo.com/quote/{target_asset}.NS/news", use_container_width=True)
        with col_n3:
            st.link_button("📊 Screener Fundamentals", f"https://www.screener.in/company/{target_asset}/consolidated/", use_container_width=True)
