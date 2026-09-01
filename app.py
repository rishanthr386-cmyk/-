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
    /* High-contrast, minimalist brutalist aesthetic */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FAFAFA;
        color: #111;
    }
    
    .verdict-box {
        border: 4px solid #111;
        background-color: #fff;
        padding: 30px;
        box-shadow: 8px 8px 0px #111;
        margin-bottom: 30px;
    }
    
    .verdict-title { font-family: 'IBM Plex Mono', monospace; font-size: 14px; text-transform: uppercase; font-weight: 600; color: #555; }
    .verdict-action { font-size: 42px; font-weight: 900; letter-spacing: -1px; margin: 10px 0; }
    
    .metric-row { display: flex; gap: 20px; margin-bottom: 30px; }
    .metric-card {
        flex: 1;
        border: 2px solid #111;
        padding: 15px;
        background: #fff;
        border-radius: 0px;
    }
    .metric-val { font-family: 'IBM Plex Mono', monospace; font-size: 24px; font-weight: 600; }
    .metric-lbl { font-size: 11px; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; color: #777; }
    
    .agent-trace { font-family: 'IBM Plex Mono', monospace; font-size: 13px; padding: 15px; background: #111; color: #00FF41; border-left: 5px solid #00FF41; margin-bottom: 15px;}
    .agent-trace.rag { border-left-color: #FF00FF; color: #FF00FF; }
    .agent-trace.macro { border-left-color: #00FFFF; color: #00FFFF; }
    .agent-trace.error { border-left-color: #FF0000; color: #FF0000; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. NEW DATA CONTRACTS & TERMINOLOGY
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

@dataclass
class MacroBehavioral:
    retail_sentiment: str
    institutional_flow: float
    raw_output: str

@dataclass
class RetailUser:
    alias: str
    strategy: str
    holdings: Dict[str, float]

# ==========================================
# 2. REDESIGNED PARALLEL AGENTS
# ==========================================
class OrderFlowAgent:
    """Evaluates 3 independent dimensions: Order Imbalance, Trend Velocity, Volatility Squeeze[cite: 1]."""
    async def process(self, asset: str) -> OrderFlowSignal:
        await asyncio.sleep(0.3)
        imbalance = random.uniform(-100, 100)
        velocity = random.uniform(-5, 5)
        vol_squeeze = random.uniform(0.1, 1.0)
        
        regime = "EXPANSIONARY" if imbalance > 20 and velocity > 1 else "CONTRACTIONARY" if imbalance < -20 else "CONSOLIDATION"
        strength = round(min(0.99, abs(imbalance/100) + vol_squeeze), 2)
        
        return OrderFlowSignal(
            regime=regime, strength=strength,
            metrics={"Order_Imbalance": round(imbalance,1), "Trend_Velocity": round(velocity,2), "Vol_Squeeze_Factor": round(vol_squeeze,2)},
            raw_output=f"Detected {regime} order flow regime. Imbalance skewed by {imbalance:.1f}%. Trend velocity at {velocity:.2f}."
        )

class GovernanceRAGAgent:
    """Retrieves document chunks based on natural language context[cite: 1]."""
    def __init__(self):
        self.corpus = {
            "TATAMOTORS": ("EV penetration crossed 12% of total portfolio; margin realization up 110bps.", "SEBI Q4 Earnings Presentation, Slide 12"),
            "ITC": ("FMCG segment margins expanded despite inflationary pressures; agri-business faces export curbs.", "Corporate Filing 8-K Equivalent, Pg 4"),
            "INFY": ("Discretionary tech spending remains muted. TCV of large deals stands at $3.2B.", "Management Commentary - Q2 Transcript")
        }

    async def process(self, asset: str, simulate_missing: bool = False) -> RegulatoryRAG:
        await asyncio.sleep(0.45)
        if simulate_missing:
            raise LookupError(f"CRITICAL: SEBI regulatory database connection timed out for {asset}.")
        data, cite = self.corpus.get(asset, ("No major regulatory red flags detected in last 90 days.", "System Aggregate DB"))
        return RegulatoryRAG(extracted_insight=data, document_citation=cite)

class BehavioralAgent:
    async def process(self, asset: str, simulate_crash: bool = False) -> MacroBehavioral:
        await asyncio.sleep(0.2)
        if simulate_crash:
            raise ConnectionError("Alternative Data Webhook Failed.")
        fii_flow = random.uniform(-500, 500)
        return MacroBehavioral(
            retail_sentiment="EUPHORIC" if fii_flow < 0 else "FEARFUL",
            institutional_flow=round(fii_flow, 2),
            raw_output=f"Retail skew is divergent from Institutional flows ({fii_flow:.2f}Cr detected)."
        )

# ==========================================
# 3. UNIQUE SYNTHESIS LAYER
# ==========================================
class DecisionSynthesizer:
    def evaluate(self, flow: OrderFlowSignal, rag: RegulatoryRAG, macro: MacroBehavioral, user: RetailUser) -> Dict[str, str]:
        macro_state = macro.raw_output if macro else "SYSTEM DEGRADED: Running without behavioral overlay."
        
        # User profiling demonstrably alters output[cite: 1]
        if user.strategy == "Capital Shield":
            if flow.regime == "CONTRACTIONARY":
                action = "SYSTEMATIC DIVESTMENT"
                logic = "Your Capital Shield strategy mandates strict drawdown limits. Contractionary order flow triggers immediate risk-off protocols."
            else:
                action = "HOLD / YIELD FOCUS"
                logic = "Order flow is stable, but fundamental context requires waiting for deeper value entry points to protect capital."
        
        elif user.strategy == "Alpha Seeker":
            if flow.regime == "EXPANSIONARY":
                action = "STRATEGIC ACCUMULATION"
                logic = "Expansionary regime aligns with your Alpha Seeker profile. Momentum and liquidity support aggressive positioning."
            elif flow.regime == "CONTRACTIONARY" and macro and macro.retail_sentiment == "FEARFUL":
                action = "CONTRARIAN ENTRY"
                logic = "Retail fear detected alongside contraction. Your aggressive profile permits accumulating discounted assets."
            else:
                action = "MAINTAIN EXPOSURE"
                logic = "Signals are mixed. Awaiting stronger volatility squeeze before deploying additional capital."
        else:
            action = "NEUTRAL WEIGHT"
            logic = "Market dynamics do not breach thresholds for portfolio reallocation."

        return {
            "Verdict": action,
            "Personalized_Rationale": logic,
            "Evidence_Flow": f"{flow.raw_output} (Confidence: {flow.strength})",
            "Evidence_RAG": rag.extracted_insight,
            "Citation": rag.document_citation,
            "Evidence_Macro": macro_state
        }

# ==========================================
# 4. ORCHESTRATION 
# ==========================================
async def run_intel_pipeline(asset: str, user: RetailUser, fail_rag: bool, fail_macro: bool) -> Tuple:
    t0 = time.time()
    
    # Parallel dispatch[cite: 1]
    res = await asyncio.gather(
        OrderFlowAgent().process(asset),
        GovernanceRAGAgent().process(asset, fail_rag),
        BehavioralAgent().process(asset, fail_macro),
        return_exceptions=True # Graceful handling[cite: 1]
    )
    
    flow, rag, macro = res
    if isinstance(rag, Exception):
        rag = RegulatoryRAG("SEBI Filings Unavailable. Operating purely on quantitative order flow.", "System Bypass Protocol")
    if isinstance(macro, Exception):
        macro = None

    synthesis = DecisionSynthesizer().evaluate(flow, rag, macro, user)
    
    # 3 Measurable Metrics[cite: 1]
    latency = (time.time() - t0) * 1000
    metrics = {
        "Engine_Ping": f"{latency:.0f}ms",
        "Synthesis_Confidence": f"{flow.strength * 100:.1f}%",
        "Portfolio_Vol_Beta": "1.45 (High)" if user.strategy == "Alpha Seeker" else "0.82 (Low)"
    }
    
    return flow, synthesis, metrics

# ==========================================
# 5. STREAMLIT INTERFACE
# ==========================================
st.markdown("<h1 style='font-family: \"IBM Plex Mono\"; font-weight: 900; font-size: 36px; border-bottom: 4px solid #111; padding-bottom: 10px; margin-bottom: 30px;'>PROJECT NEXUS // INTELLIGENCE LAYER</h1>", unsafe_allow_html=True)

# Top Bar Configuration
c1, c2, c3 = st.columns([1.5, 1.5, 2])
with c1:
    target_asset = st.selectbox("TARGET EQUITY", ["TATAMOTORS", "ITC", "INFY"])
with c2:
    user_strategy = st.selectbox("USER STRATEGY PROFILE", ["Capital Shield", "Balanced", "Alpha Seeker"], index=2)
with c3:
    st.markdown("<div style='padding-top: 30px;'>", unsafe_allow_html=True)
    trigger = st.button("EXECUTE NEURAL PIPELINE", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with st.expander("DEGRADATION TESTING (GRACEFUL FAILURE)"):
    col_a, col_b = st.columns(2)
    with col_a: fail_rag = st.checkbox("Simulate SEBI DB Timeout")
    with col_b: fail_macro = st.checkbox("Simulate Alt-Data Webhook Crash")

# Portfolio Display (Unique Weights)
st.markdown("<p style='font-family: \"IBM Plex Mono\"; font-size: 12px; font-weight: bold; margin-top: 20px;'>CURRENT LEDGER WEIGHTS:</p>", unsafe_allow_html=True)
st.markdown("`TATAMOTORS: 42.5%` | `ITC: 27.0%` | `INFY: 15.5%` | `LIQUID_BEES (CASH): 15.0%`")

if trigger:
    user = RetailUser("USR_992", user_strategy, {})
    
    with st.spinner("Compiling multi-agent consensus..."):
        flow_data, output, stats = asyncio.run(run_intel_pipeline(target_asset, user, fail_rag, fail_macro))
    
    # Custom Metric Row[cite: 1]
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card"><div class="metric-lbl">Processing Latency</div><div class="metric-val">{stats['Engine_Ping']}</div></div>
        <div class="metric-card"><div class="metric-lbl">Synthesis Confidence</div><div class="metric-val">{stats['Synthesis_Confidence']}</div></div>
        <div class="metric-card"><div class="metric-lbl">Portfolio Vol Beta</div><div class="metric-val">{stats['Portfolio_Vol_Beta']}</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Verdict Box
    st.markdown(f"""
    <div class="verdict-box">
        <div class="verdict-title">System Verdict for {target_asset}</div>
        <div class="verdict-action" style="color: {'#111'};">{output['Verdict']}</div>
        <div style="font-size: 16px; line-height: 1.6; font-weight: 500;">{output['Personalized_Rationale']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stacked Raw Agent Traces (Terminal Style)
    st.markdown("### RAW AGENT TELEMETRY")
    
    st.markdown(f"<div class='agent-trace'>[QUANT_AGENT]: {output['Evidence_Flow']}</div>", unsafe_allow_html=True)
    with st.expander("View Quant Dimensions"): st.json(flow_data.metrics)
    
    rag_class = "error" if fail_rag else "rag"
    st.markdown(f"<div class='agent-trace {rag_class}'>[RAG_GOVERNANCE]: {output['Evidence_RAG']}<br><br><span style='font-size: 11px;'>SOURCE CITE: {output['Citation']}</span></div>", unsafe_allow_html=True)
    
    macro_class = "error" if fail_macro else "macro"
    st.markdown(f"<div class='agent-trace {macro_class}'>[MACRO_BEHAVIORAL]: {output['Evidence_Macro']}</div>", unsafe_allow_html=True)
