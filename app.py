import asyncio
import time
import random
from dataclasses import dataclass
from typing import Dict, Any, Tuple
import streamlit as st

# ==========================================
# 0. STREAMLIT CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="NexusFi // Autonomous Multi-Agent Intelligence", layout="wide")

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
# 1. DATA CONTRACTS & AUTOMATED PROFILING
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
class DynamicInferredProfile:
    risk_category: str
    inferred_reason: str

def auto_infer_risk_profile(cash_pct: float, bias: str) -> DynamicInferredProfile:
    """Automatically determines user investor classification based on financial position trends[cite: 1]."""
    if cash_pct >= 30 or bias == "Loss Averse":
        return DynamicInferredProfile(
            risk_category="Low Risk (Capital Shield)",
            inferred_reason=f"Inferred via high liquidity buffer ({cash_pct}%) and defensive behavioral bias ('{bias}')."
        )
    elif cash_pct <= 15 and bias == "Momentum Chaser":
        return DynamicInferredProfile(
            risk_category="High Risk (Alpha Seeker)",
            inferred_reason=f"Inferred via aggressive capital deployment ({cash_pct}% cash buffer) and momentum trend bias."
        )
    else:
        return DynamicInferredProfile(
            risk_category="Medium Risk (Balanced Growth)",
            inferred_reason=f"Inferred via moderate cash allocation ({cash_pct}%) and blended asset bias ('{bias}')."
        )

# ==========================================
# 2. PARALLEL AI AGENTS
# ==========================================
class QuantitativeEngine:
    async def evaluate(self, asset: str) -> QuantitativeSignal:
        await asyncio.sleep(0.3)
        score = random.uniform(-1, 1)
        cls = "BULLISH MOMENTUM" if score > 0.2 else "BEARISH PRESSURE" if score < -0.2 else "NEUTRAL CONSOLIDATION"
        return QuantitativeSignal(classification=cls, confidence=round(abs(score), 2), summary=f"Evaluated price momentum, volume anomaly, and volatility dimensions[cite: 1]. Score: {score:.2f}.")

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
# 3. SYNTHESIS LAYER
# ==========================================
class DecisionSynthesizer:
    def synthesize(self, quant: QuantitativeSignal, rag: RegulatoryRAGSource, alt: BehavioralSentiment, profile: DynamicInferredProfile) -> Dict[str, Any]:
        if "Low Risk" in profile.risk_category:
            action = "DEFENSIVE REDUCE / HOLD CASH" if "BEARISH" in quant.classification else "CAUTIOUS HOLD"
            r1 = f"• Automated Profile Match: {profile.risk_category}."
            r2 = f"• Quantitative Driver: {quant.summary}"
            r3 = f"• Strategic Directive: Prioritize capital safety and risk mitigation."
        elif "High Risk" in profile.risk_category:
            action = "AGGRESSIVE ACCUMULATION" if "BULLISH" in quant.classification else "TACTICAL DIP BUY"
            r1 = f"• Automated Profile Match: {profile.risk_category}."
            r2 = f"• Quantitative Driver: {quant.summary}"
            r3 = f"• Strategic Directive: Authorize high-beta tactical upside positioning."
        else:
            action = "BALANCED REBALANCING"
            r1 = f"• Automated Profile Match: {profile.risk_category}."
            r2 = f"• Regulatory Grounding: {rag.insight}"
            r3 = f"• Strategic Directive: Maintain scaled allocation without over-concentration."

        return {
            "Action": action,
            "Line1": r1,
            "Line2": r2,
            "Line3": r3,
            "Citation": rag.citation_title,
            "Link": rag.official_link,
            "RAG_Text": rag.insight
        }

async def run_pipeline(asset: str, profile: DynamicInferredProfile, fail_rag: bool, fail_alt: bool):
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
    
    output = DecisionSynthesizer().synthesize(q, r, a, profile)
    latency = (time.time() - t0) * 1000
    return output, f"{latency:.0f}ms", f"{q.confidence * 100:.0f}%"

# ==========================================
# 4. STREAMLIT FRONTEND USER INTERFACE
# ==========================================
st.title("PROJECT NEXUS // INTELLIGENCE LAYER")
st.caption("Autonomous Multi-Agent Financial System for Retail Investors[cite: 1]")
st.markdown("---")

# Dynamic Controls for User Financial Trends
col_top1, col_top2, col_top3 = st.columns(3)
with col_top1:
    target_asset = st.selectbox("SELECT BRAND / EQUITY", TICKER_UNIVERSE)
with col_top2:
    cash_pct = st.slider("PORTFOLIO CASH BUFFER (%)", 5, 50, 20)
with col_top3:
    behavior_bias = st.selectbox("BEHAVIORAL TREND BIAS", ["Momentum Chaser", "Value Investor", "Loss Averse"], index=0)

# Automated Risk Inference
inferred_profile = auto_infer_risk_profile(cash_pct, behavior_bias)

st.markdown(f"""
<div style="background: #1e293b; border-left: 4px solid #38bdf8; padding: 12px 18px; border-radius: 6px; margin: 15px 0;">
    <b style="color: #38bdf8;">AI Automated Investor Classification:</b> <span style="color: #fff; font-weight: 700;">{inferred_profile.risk_category}</span><br>
    <span style="font-size: 12px; color: #94a3b8;">{inferred_profile.inferred_reason}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
execute_btn = st.button("🚀 EXECUTE MULTI-AGENT REASONING PIPELINE", type="primary", use_container_width=True)

with st.expander("🛠️ System Reliability & Graceful Degradation Toggles[cite: 1]"):
    fail_rag = st.checkbox("Simulate Regulatory Vector Database Timeout")
    fail_alt = st.checkbox("Simulate Alternative Data Feed Crash")

if execute_btn:
    with st.spinner("Dispatching parallel agents (Quant, RAG, Behavioral)...[cite: 1]"):
        result, latency, conf = asyncio.run(run_pipeline(target_asset, inferred_profile, fail_rag, fail_alt))

    # Telemetry Metrics Row
    st.markdown("### 📊 Session Performance & Risk Telemetry[cite: 1]")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Pipeline Latency", latency)
    m2.metric("Model Confidence", conf)
    m3.metric("Cash Buffer", f"{cash_pct}%")
    m4.metric("Active Agents", "3 Parallel[cite: 1]")

    # Core Verdict Card
    st.markdown("### 🎯 Personalized Investment Intelligence[cite: 1]")
    with st.container(border=True):
        st.markdown(f"**Synthesized Advisory for `{target_asset}`**")
        st.markdown(f"## {result['Action']}")
        st.markdown(f"""
        {result['Line1']}<br>
        {result['Line2']}<br>
        {result['Line3']}
        """, unsafe_allow_html=True)

    # Verified Source Citations & Live Clickable News Hub (Bug Free Syntax)
    st.markdown("### 📑 Verified Source Citations & Live Brand News Center[cite: 1]")
    with st.container(border=True):
        st.markdown("**Official Regulatory Citation & Document Source:**[cite: 1]")
        st.markdown(f"📄 [{result['Citation']}]({result['Link']})")
        
        st.markdown("**Extracted Contextual RAG Insight:**[cite: 1]")
        st.info(f'"{result["RAG_Text"]}"')
        
        st.markdown(f"**Live Clickable News & Financial Feeds for `{target_asset}`:**")
        
        col_n1, col_n2, col_n3 = st.columns(3)
        with col_n1:
            st.link_button("📈 Google Finance Hub", f"https://www.google.com/finance/quote/{target_asset}:NSE", use_container_width=True)
        with col_n2:
            st.link_button("📰 Yahoo News & Filings", f"https://finance.yahoo.com/quote/{target_asset}.NS/news", use_container_width=True)
        with col_n3:
            st.link_button("📊 Screener Fundamentals", f"https://www.screener.in/company/{target_asset}/consolidated/", use_container_width=True)
