import asyncio
import time
import random
from dataclasses import dataclass
from typing import Dict, Any, Tuple
import streamlit as st

# ==========================================
# 0. BRUTALIST UI / CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Project Nexus | Retail Intel", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #FAFAFA; color: #111; }
    
    .verdict-box { border: 4px solid #111; background-color: #fff; padding: 30px; box-shadow: 8px 8px 0px #111; margin-bottom: 30px; }
    .verdict-title { font-family: 'IBM Plex Mono', monospace; font-size: 14px; text-transform: uppercase; font-weight: 600; color: #555; }
    .verdict-action { font-size: 42px; font-weight: 900; letter-spacing: -1px; margin: 10px 0; }
    
    .metric-row { display: flex; gap: 20px; margin-bottom: 30px; }
    .metric-card { flex: 1; border: 2px solid #111; padding: 15px; background: #fff; }
    .metric-val { font-family: 'IBM Plex Mono', monospace; font-size: 24px; font-weight: 600; }
    .metric-lbl { font-size: 11px; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; color: #777; }
    
    .agent-trace { font-family: 'IBM Plex Mono', monospace; font-size: 13px; padding: 15px; background: #111; color: #00FF41; border-left: 5px solid #00FF41; margin-bottom: 15px;}
    .agent-trace.rag { border-left-color: #FF00FF; color: #FF00FF; }
    .agent-trace.macro { border-left-color: #00FFFF; color: #00FFFF; }
    .agent-trace.error { border-left-color: #FF0000; color: #FF0000; }
    
    .news-ticker { background: #111; color: #fff; padding: 10px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; border-left: 4px solid #FF00FF; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. 30+ INDIAN EQUITIES UNIVERSE
# ==========================================
TICKER_UNIVERSE = sorted([
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "BHARTIARTL", "INFY", "ITC", 
    "SBIN", "L&T", "BAJFINANCE", "HINDUNILVR", "MARUTI", "M&M", "ASIANPAINT", 
    "TITAN", "SUNPHARMA", "TATAMOTORS", "NTPC", "COALINDIA", "ONGC", 
    "POWERGRID", "ADANIPORTS", "ADANIENT", "KOTAKBANK", "AXISBANK", 
    "WIPRO", "BAJAJFINSV", "NESTLEIND", "ULTRACEMCO", "TECHM"
])

# ==========================================
# 2. DATA CONTRACTS
# ==========================================
@dataclass
class OrderFlowSignal:
    regime: str
    strength: float
    metrics: Dict[str, float]
    raw_output: str

@dataclass
class RegulatoryRAG:
    extracted_insight: str
    document_citation: str
    source_url: str

@dataclass
class MacroBehavioral:
    retail_sentiment: str
    institutional_flow: float
    raw_output: str

@dataclass
class RetailUser:
    strategy: str
    drawdown_limit: str

# ==========================================
# 3. PARALLEL AGENTS
# ==========================================
class OrderFlowAgent:
    async def process(self, asset: str) -> OrderFlowSignal:
        await asyncio.sleep(0.3)
        imbalance = random.uniform(-100, 100)
        velocity = random.uniform(-5, 5)
        
        regime = "EXPANSIONARY" if imbalance > 20 and velocity > 1 else "CONTRACTIONARY" if imbalance < -20 else "CONSOLIDATION"
        strength = round(min(0.99, abs(imbalance/100) + abs(velocity/5)), 2)
        
        return OrderFlowSignal(
            regime=regime, strength=strength,
            metrics={"Order_Imbalance": round(imbalance,1), "Trend_Velocity": round(velocity,2)},
            raw_output=f"[{asset}] Detected {regime} order flow. Imbalance skewed by {imbalance:.1f}%. Trend velocity at {velocity:.2f}."
        )

class GovernanceRAGAgent:
    async def process(self, asset: str, simulate_missing: bool = False) -> RegulatoryRAG:
        await asyncio.sleep(0.45)
        if simulate_missing:
            raise LookupError(f"CRITICAL: SEBI database connection timed out for {asset}.")
            
        # Simulated vector retrieval for 30+ companies
        risk_factors = ["margin compression", "supply chain bottlenecks", "regulatory scrutiny", "executive churn", "stable capex growth"]
        insight = f"Q2 filings indicate {random.choice(risk_factors)} impacting forward guidance. Institutional holding remains stable."
        
        return RegulatoryRAG(
            extracted_insight=insight, 
            document_citation=f"SEBI Quarterly Disclosures - {asset} (Form 8-K Equivalent, Sec 4)",
            source_url=f"https://www.nseindia.com/get-quotes/equity?symbol={asset}"
        )

class BehavioralAgent:
    async def process(self, asset: str, simulate_crash: bool = False) -> MacroBehavioral:
        await asyncio.sleep(0.2)
        if simulate_crash:
            raise ConnectionError("Alternative Data Webhook Failed.")
        
        fii_flow = random.uniform(-500, 500)
        sentiment = "EUPHORIC" if fii_flow < 0 else "FEARFUL"
        
        return MacroBehavioral(
            retail_sentiment=sentiment,
            institutional_flow=round(fii_flow, 2),
            raw_output=f"Social graph shows {sentiment} retail behavior. Institutional flows counter-positioned at {fii_flow:.2f}Cr."
        )

# ==========================================
# 4. SYNTHESIS LAYER
# ==========================================
class DecisionSynthesizer:
    def evaluate(self, flow: OrderFlowSignal, rag: RegulatoryRAG, macro: MacroBehavioral, user: RetailUser) -> Dict[str, str]:
        macro_state = macro.raw_output if macro else "SYSTEM DEGRADED: Running without behavioral overlay."
        
        if user.strategy == "Capital Shield":
            action = "SYSTEMATIC DIVESTMENT" if flow.regime == "CONTRACTIONARY" else "HOLD / YIELD FOCUS"
            logic = f"Capital Shield profile limits risk. {flow.regime} flow dictates a highly defensive posture."
        else: # Alpha Seeker
            action = "STRATEGIC ACCUMULATION" if flow.regime == "EXPANSIONARY" else "MAINTAIN EXPOSURE"
            logic = f"Alpha Seeker profile permits elevated risk. {flow.regime} flow aligns with current tactical accumulation."

        return {
            "Verdict": action,
            "Personalized_Rationale": logic,
            "Evidence_Flow": f"{flow.raw_output} (Confidence: {flow.strength})",
            "Evidence_RAG": rag.extracted_insight,
            "Citation": rag.document_citation,
            "Source_Link": rag.source_url,
            "Evidence_Macro": macro_state
        }

# ==========================================
# 5. ORCHESTRATION PIPELINE
# ==========================================
async def run_intel_pipeline(asset: str, user: RetailUser, fail_rag: bool, fail_macro: bool) -> Tuple:
    t0 = time.time()
    
    res = await asyncio.gather(
        OrderFlowAgent().process(asset),
        GovernanceRAGAgent().process(asset, fail_rag),
        BehavioralAgent().process(asset, fail_macro),
        return_exceptions=True
    )
    
    flow, rag, macro = res
    if isinstance(rag, Exception):
        rag = RegulatoryRAG("Filings Unavailable. Operating on quantitative flow.", "System Bypass Protocol", "#")
    if isinstance(macro, Exception):
        macro = None

    synthesis = DecisionSynthesizer().evaluate(flow, rag, macro, user)
    latency = (time.time() - t0) * 1000
    
    return flow, synthesis, f"{latency:.0f}ms", f"{flow.strength * 100:.1f}%"

# ==========================================
# 6. STREAMLIT INTERFACE
# ==========================================
st.markdown("<h1 style='font-family: \"IBM Plex Mono\"; font-weight: 900; font-size: 36px; border-bottom: 4px solid #111; padding-bottom: 10px; margin-bottom: 30px;'>PROJECT NEXUS // INTELLIGENCE LAYER</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1.5, 1.5, 2])
with c1:
    target_asset = st.selectbox("TARGET EQUITY (NIFTY 50)", TICKER_UNIVERSE)
with c2:
    user_strategy = st.selectbox("USER STRATEGY PROFILE", ["Capital Shield", "Balanced", "Alpha Seeker"], index=2)
with c3:
    st.markdown("<div style='padding-top: 30px;'>", unsafe_allow_html=True)
    trigger = st.button("EXECUTE NEURAL PIPELINE", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Live News Ticker Section
mock_news = [f"FIIs net {random.choice(['buyers', 'sellers'])} in {target_asset}", f"Block deal detected in {target_asset} options chain", f"{target_asset} hits new support volume nodes"]
st.markdown(f"<div class='news-ticker'>LIVE TERMINAL FEED >> {mock_news[0]} | {mock_news[1]} | {mock_news[2]}</div>", unsafe_allow_html=True)

with st.expander("DEGRADATION TESTING (GRACEFUL FAILURE)"):
    col_a, col_b = st.columns(2)
    with col_a: fail_rag = st.checkbox("Simulate SEBI DB Timeout")
    with col_b: fail_macro = st.checkbox("Simulate Alt-Data Webhook Crash")

if trigger:
    user = RetailUser(user_strategy, "Strict")
    
    with st.spinner("Compiling multi-agent consensus..."):
        flow_data, output, latency_str, conf_str = asyncio.run(run_intel_pipeline(target_asset, user, fail_rag, fail_macro))
    
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card"><div class="metric-lbl">Processing Latency</div><div class="metric-val">{latency_str}</div></div>
        <div class="metric-card"><div class="metric-lbl">Synthesis Confidence</div><div class="metric-val">{conf_str}</div></div>
        <div class="metric-card"><div class="metric-lbl">Strategy Beta</div><div class="metric-val">{"1.45" if user.strategy == "Alpha Seeker" else "0.82"}</div></div>
    </div>
    
    <div class="verdict-box">
        <div class="verdict-title">System Verdict for {target_asset}</div>
        <div class="verdict-action" style="color: {'#111'};">{output['Verdict']}</div>
        <div style="font-size: 16px; line-height: 1.6; font-weight: 500;">{output['Personalized_Rationale']}</div>
    </div>
    
    <h3>RAW AGENT TELEMETRY & CITATIONS</h3>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='agent-trace'>[QUANT_AGENT]: {output['Evidence_Flow']}</div>", unsafe_allow_html=True)
    
    rag_class = "error" if fail_rag else "rag"
    st.markdown(f"""
    <div class='agent-trace {rag_class}'>
        [RAG_GOVERNANCE]: {output['Evidence_RAG']}<br><br>
        <span style='font-size: 11px;'>SOURCE CITE: <a href="{output['Source_Link']}" target="_blank" style="color: #FF00FF; text-decoration: underline;">{output['Citation']}</a></span>
    </div>
    """, unsafe_allow_html=True)
    
    macro_class = "error" if fail_macro else "macro"
    st.markdown(f"<div class='agent-trace {macro_class}'>[MACRO_BEHAVIORAL]: {output['Evidence_Macro']}</div>", unsafe_allow_html=True)
