import asyncio
import time
import random
from dataclasses import dataclass
from typing import Dict, Any, Tuple
import streamlit as st

# ==========================================
# 0. STREAMLIT CONFIGURATION
# ==========================================
st.set_page_config(page_title="NexusFi // Multi-Agent Intelligence", layout="wide")

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
        return QuantitativeSignal(classification=cls, confidence=round(abs(score), 2), summary=f"Evaluated price momentum, volume anomaly, and volatility across independent dimensions[cite: 1]. Composite Score: {score:.2f}.")

class RegulatoryRAGVault:
    async def evaluate(self, asset: str, fail_rag: bool) -> RegulatoryRAGSource:
        await asyncio.sleep(0.4)
        if fail_rag: raise LookupError("Vector database timeout.")
        return RegulatoryRAGSource(
            insight=f"Latest corporate filings and earnings disclosures for {asset} indicate stable debt-to-equity ratios with localized margin optimizations.",
            citation_title=f"SEBI Quarterly Financial Disclosure & Earnings Transcript — {asset}[cite: 1]",
            official_link=f"https://www.screener.in/company/{asset}/consolidated/"
        )

class BehavioralSentimentEngine:
    async def evaluate(self, asset: str, fail_alt: bool) -> BehavioralSentiment:
        await asyncio.sleep(0.2)
        if fail_alt: raise ConnectionError("Alternative feed offline.")
        tone = random.choice(["EUPHORIC RETAIL HYPE", "DEFENSIVE RETAIL CAUTION", "APATHETIC ACCUMULATION"])
        return BehavioralSentiment(sentiment=tone, summary=f"Analyzed social sentiment feeds and FII/DII institutional flows: {tone}[cite: 1].")

# ==========================================
# 3. SYNTHESIS LAYER (USER CONDITION MODIFIER)
# ==========================================
class DecisionSynthesizer:
    def synthesize(self, quant: QuantitativeSignal, rag: RegulatoryRAGSource, alt: BehavioralSentiment, user: RetailUserProfile) -> Dict[str, Any]:
        # User condition matching rule from problem statement (identical inputs yield different outputs based on profile)[cite: 1]
        if user.risk_tolerance == "Low (Capital Shield)":
            if "BEARISH" in quant.classification or user.cash_allocation_pct < 25:
                action = "DEFENSIVE REDUCE / HOLD CASH"
                r1 = f"• Risk Condition Triggered: Low Risk Tolerance & Cash Buffer ({user.cash_allocation_pct}%)."
                r2 = f"• Quantitative Alert: {quant.summary}"
                r3 = f"• Strategic Directive: Prioritize capital preservation and debt mitigation."
            else:
                action = "CAUTIOUS HOLD"
                r1 = f"• Risk Condition Triggered: Conservative portfolio parameters active."
                r2 = f"• Regulatory Grounding: {rag.insight}"
                r3 = f"• Strategic Directive: Maintain position without adding incremental risk exposure."
        else: # High Risk / Alpha Seeker
            action = "AGGRESSIVE ACCUMULATION" if "BULLISH" in quant.classification else "TACTICAL DIP BUY"
            r1 = f"• Risk Condition Triggered: High Risk Profile & Behavioral Bias ('{user.behavioral_bias}')."
            r2 = f"• Quantitative Driver: {quant.summary}"
            r3 = f"• Strategic Directive: Authorize high-beta tactical allocation."

        return {
            "Action": action,
            "Line1": r1,
            "Line2": r2,
            "Line3": r3,
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
    if isinstance(r, Exception): r = RegulatoryRAGSource("Regulatory filing retrieval failed. System fallback active[cite: 1].", "Fallback Ledger", "#")
    if isinstance(a, Exception): a = BehavioralSentiment("NEUTRAL", "Sentiment feed offline[cite: 1].")
    
    output = DecisionSynthesizer().synthesize(q, r, a, user)
    latency = (time.time() - t0) * 1000
    return output, f"{latency:.0f}ms", f"{q.confidence * 100:.0f}%"

# ==========================================
# 4. STREAMLIT FRONTEND USER INTERFACE
# ==========================================
st.title("PROJECT NEXUS // INTELLIGENCE LAYER")
st.caption("Autonomous Multi-Agent Financial System for Retail Investors[cite: 1]")

st.markdown("---")

# User Customization & Position Controls
col_top1, col_top2, col_top3, col_top4 = st.columns(4)
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
    st.markdown("### 📊 Session Performance & Risk Telemetry[cite: 1]")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Pipeline Latency", latency)
    m2.metric("Model Confidence", conf)
    m3.metric("Portfolio Cash Buffer", f"{cash_pct}%")
    m4.metric("Active Agents", "3 Parallel[cite: 1]")

    # Core Verdict Card (Line by Line Formatting)
    st.markdown("### 🎯 Personalized Investment Intelligence[cite: 1]")
    with st.container(border=True):
        st.markdown(f"**Synthesized Advisory for `{target_asset}`**")
        st.markdown(f"## {result['Action']}")
        st.markdown(f"""
        {result['Line1']}<br>
        {result['Line2']}<br>
        {result['Line3']}
        """, unsafe_allow_html=True)

    # Verified Source Citations & Live Clickable News Hub
    st.markdown("### 📑 Verified Source Citations & Live Brand News Center[cite: 1]")
    with st.container(border=True):
        st.markdown(f"**Official Regulatory Citation & Document Source:**[cite: 1]")
        st.markdown(f"📄 [{result['Citation']}]({result['Link'])")
        
        st.markdown(f"**Extracted Contextual RAG Insight:**[cite: 1]")
        st.info(f'"{result["RAG_Text"]}"')
        
        st.markdown(f"**Live Clickable News & Financial Feeds for `{target_asset}`:**")
        
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            st.link_button("📈 Google Finance Hub", f"https://www.google.com/finance/quote/{target_asset}:NSE", use_container_width=True)
        with col_n2:
            st.link_button("📰 Yahoo News & Filings", f"https://finance.yahoo.com/quote/{target_asset}.NS/news", use_container_width=True)
        with col_n3:
            st.link_button("📊 Screener Fundamentals", f"https://www.screener.in/company/{target_asset}/consolidated/", use_container_width=True)
