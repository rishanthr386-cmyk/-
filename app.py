import asyncio
import time
import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import streamlit as st

# ==========================================
# 0. UI & CSS CONFIGURATION
# ==========================================
st.set_page_config(page_title="NeuraFi Terminal | HackVerse 2026", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS for the "Bloomberg Terminal meets Cyberpunk" vibe
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@300;500;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glowing Title */
    .terminal-title {
        font-family: 'Fira Code', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Decision Banner Cards */
    .decision-banner {
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    .buy-banner { background: linear-gradient(135deg, rgba(16,185,129,0.2) 0%, rgba(6,78,59,0.4) 100%); border-left: 5px solid #10b981; }
    .sell-banner { background: linear-gradient(135deg, rgba(239,68,68,0.2) 0%, rgba(127,29,29,0.4) 100%); border-left: 5px solid #ef4444; }
    .hold-banner { background: linear-gradient(135deg, rgba(245,158,11,0.2) 0%, rgba(120,53,15,0.4) 100%); border-left: 5px solid #f59e0b; }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #1a1c23;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2e323d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Monospace Text for Data */
    .mono { font-family: 'Fira Code', monospace; font-size: 0.9em; color: #a0aec0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. STRUCTURED DATA CONTRACTS
# ==========================================
@dataclass
class MarketSignal:
    classification: str
    confidence: float
    dimensions_evaluated: Dict[str, float]
    reasoning: str

@dataclass
class RAGOutput:
    insight: str
    source_attribution: List[str]

@dataclass
class SentimentSignal:
    classification: str
    confidence: float
    reasoning: str

@dataclass
class UserProfile:
    user_id: str
    risk_tolerance: str
    portfolio: Dict[str, float]

# ==========================================
# 2. PARALLEL AGENTS
# ==========================================
class SignalClassificationAgent:
    async def analyze(self, ticker: str) -> MarketSignal:
        await asyncio.sleep(0.3) # Added slight delay for realistic loading effect
        momentum = random.uniform(-1, 1)
        vol_anomaly = random.uniform(0.5, 3.0)
        volatility = random.uniform(10, 50)
        
        is_bullish = momentum > 0.1 and vol_anomaly > 1.2
        classification = "Bullish" if is_bullish else "Bearish" if momentum < -0.1 else "Neutral"
        confidence = round(min(0.98, abs(momentum) + (vol_anomaly * 0.1)), 2)
        
        return MarketSignal(
            classification=classification,
            confidence=confidence,
            dimensions_evaluated={"Momentum_Osc": round(momentum, 2), "Vol_Spike_X": round(vol_anomaly, 2), "VIX_Proxy": round(volatility, 2)},
            reasoning=f"{classification} momentum detected ({momentum:.2f}) validated by {vol_anomaly:.2f}x average volume."
        )

class FundamentalRAGAgent:
    def __init__(self):
        self.vector_db = {
            "RELIANCE": {"chunk": "EBITDA margin expansion of 14% driven by JIO subscriber growth and retail footprint.", "doc": "SEBI Q3 Filing, Pg 14"},
            "HDFCBANK": {"chunk": "NIM contraction stabilized; deposit mobilization targeted aggressively for H2.", "doc": "Q2 Earnings Transcript, 18:30"},
            "TCS": {"chunk": "Operating margins contracted 40bps. Client deferrals in US financial sector noted.", "doc": "SEBI Q3 Disclosure - Sec 2"},
            "ZOMATO": {"chunk": "Blinkit GOV grew 112% YoY, achieving operating profitability across 70% of dark stores.", "doc": "Corporate Disclosure - April 2024"}
        }

    async def analyze(self, ticker: str, degrade: bool = False) -> RAGOutput:
        await asyncio.sleep(0.4)
        if degrade:
            raise FileNotFoundError(f"Vector Index Missing for {ticker}.")
        data = self.vector_db.get(ticker, {"chunk": "No structural anomalies in SEC/SEBI filings.", "doc": "Sys Database"})
        return RAGOutput(insight=data["chunk"], source_attribution=[data["doc"]])

class AlternativeDataAgent:
    async def analyze(self, ticker: str, degrade: bool = False) -> SentimentSignal:
        await asyncio.sleep(0.2)
        if degrade:
            raise ConnectionError("Live Stream API offline.")
        sentiment = random.uniform(-1, 1)
        return SentimentSignal(
            classification="Positive" if sentiment > 0 else "Negative",
            confidence=0.82,
            reasoning=f"Social graph sentiment score: {sentiment:.2f} (Weighted against historical baseline)."
        )

# ==========================================
# 3. SYNTHESIS ENGINE
# ==========================================
class SynthesisEngine:
    def synthesize(self, quant: MarketSignal, rag: RAGOutput, alt: Optional[SentimentSignal], user: UserProfile) -> Dict[str, Any]:
        alt_status = alt.reasoning if alt else "⚠️ SYSTEM DEGRADED: Alternative feed offline."
        
        if user.risk_tolerance == "Low":
            if quant.classification == "Bearish":
                action, just = "SELL / REDUCE EXPOSURE", "Capital preservation prioritized for low-risk profile given downward momentum."
            else:
                action, just = "HOLD / ACCUMULATE", "Positive signals offset by conservative parameters. Awaiting fundamental confirmation."
        elif user.risk_tolerance == "High":
            if quant.classification == "Bullish":
                action, just = "AGGRESSIVE BUY", "Strong quantitative momentum aligns perfectly with your high-risk appetite."
            else:
                action, just = "SCALE IN / WATCH", "Technicals are soft, but high-risk capacity permits selective long entries."
        else:
            action, just = "MAINTAIN CURRENT WEIGHT", "Balanced risk parameters suggest no immediate portfolio restructuring."

        return {
            "Recommendation": action,
            "Justification": just,
            "Tech_Base": f"{quant.reasoning} (Conf: {quant.confidence * 100:.0f}%)",
            "Fund_Base": rag.insight,
            "Source": rag.source_attribution[0],
            "Alt_Base": alt_status
        }

# ==========================================
# 4. PIPELINE EXECUTION
# ==========================================
async def run_pipeline(ticker: str, user: UserProfile, degrade_rag: bool, degrade_alt: bool):
    start = time.time()
    results = await asyncio.gather(
        SignalClassificationAgent().analyze(ticker),
        FundamentalRAGAgent().analyze(ticker, degrade_rag),
        AlternativeDataAgent().analyze(ticker, degrade_alt),
        return_exceptions=True
    )
    
    quant, rag, alt = results
    if isinstance(rag, Exception): rag = RAGOutput("Filings unavailable. Fallback to technicals.", ["Sys Fallback"])
    if isinstance(alt, Exception): alt = None

    final = SynthesisEngine().synthesize(quant, rag, alt, user)
    latency = (time.time() - start) * 1000

    metrics = {
        "Latency": f"{latency:.0f}ms",
        "Accuracy": f"{random.uniform(70, 95):.1f}%",
        "Risk": "8.5/10" if user.risk_tolerance == "High" else "3.2/10"
    }
    return quant, final, metrics

# ==========================================
# 5. STREAMLIT FRONTEND
# ==========================================
st.markdown('<p class="terminal-title">⌘ NEURA-FI ORCHESTRATOR</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0aec0; margin-bottom: 30px;'>Autonomous Multi-Agent Intelligence Layer</p>", unsafe_allow_html=True)

# Main Controls Layout
col_asset, col_risk, col_btn = st.columns([2, 2, 1.5])
with col_asset:
    selected_ticker = st.selectbox("TARGET ASSET", ["RELIANCE", "HDFCBANK", "TCS", "ZOMATO"], label_visibility="collapsed")
with col_risk:
    risk_profile = st.selectbox("USER RISK TOLERANCE", ["Low", "Medium", "High"], index=2, label_visibility="collapsed")
with col_btn:
    execute = st.button("⚡ INITIATE PIPELINE", use_container_width=True, type="primary")

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=60)
    st.markdown("### SYSTEM CONTROLS")
    st.markdown("---")
    
    with st.expander("🛠️ Chaos Engineering (Degradation)", expanded=True):
        degrade_rag = st.checkbox("Kill Vector DB (RAG Fail)", value=False)
        degrade_alt = st.checkbox("Kill Sentiment API", value=False)
    
    st.markdown("---")
    st.markdown("### LIVE PORTFOLIO")
    portfolio = {"RELIANCE": "35%", "HDFCBANK": "25%", "ZOMATO": "20%", "CASH": "20%"}
    for asset, weight in portfolio.items():
        st.markdown(f"<p class='mono'>▸ {asset}: {weight}</p>", unsafe_allow_html=True)
    st.caption("User ID: SYS_RET_1099")

# Execution & Results
if execute:
    user = UserProfile("SYS_RET_1099", risk_profile, portfolio)
    
    with st.spinner("Dispatching specialized agents to cluster..."):
        quant_sig, synth_out, metrics = asyncio.run(run_pipeline(selected_ticker, user, degrade_rag, degrade_alt))
        st.toast('Analysis complete. Rendering insights...', icon='✅')

    # Metric Row
    m1, m2, m3 = st.columns(3)
    m1.metric("⏱️ Engine Latency", metrics["Latency"], "-24ms vs avg")
    m2.metric("🎯 30D Forward Acc (Mock)", metrics["Accuracy"], "+1.2% model drift")
    m3.metric("⚠️ Portfolio Risk Score", metrics["Risk"])

    # Decision Banner
    action = synth_out['Recommendation']
    banner_class = "buy-banner" if "BUY" in action else "sell-banner" if "SELL" in action else "hold-banner"
    
    st.markdown(f"""
    <div class="decision-banner {banner_class}">
        <h2 style="margin: 0; font-weight: 800; letter-spacing: 2px;">{action}</h2>
        <p style="margin-top: 10px; font-size: 1.1em; opacity: 0.9;">{synth_out['Justification']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧠 AGENT REASONING TRACE")
    
    # Custom Agent Output Boxes instead of Tabs
    a1, a2, a3 = st.columns(3)
    
    with a1:
        st.markdown("#### 📊 Quant Agent")
        st.info(f"**Signal:** {quant_sig.classification}")
        st.progress(quant_sig.confidence, text=f"Confidence: {quant_sig.confidence * 100:.0f}%")
        st.markdown(f"<p class='mono'>{synth_out['Tech_Base']}</p>", unsafe_allow_html=True)
        with st.expander("Raw Dimensions"):
            st.json(quant_sig.dimensions_evaluated)

    with a2:
        st.markdown("#### 📑 RAG Agent")
        if degrade_rag:
            st.error("Vector DB Connection Lost")
        else:
            st.success("Filings Retrieved")
        st.markdown(f"<p class='mono'>{synth_out['Fund_Base']}</p>", unsafe_allow_html=True)
        st.caption(f"Source: `{synth_out['Source']}`")

    with a3:
        st.markdown("#### 🌐 Alternative Agent")
        if degrade_alt:
            st.warning("Sentiment Feed Dropped")
        else:
            st.success("Feeds Synced")
        st.markdown(f"<p class='mono'>{synth_out['Alt_Base']}</p>", unsafe_allow_html=True)
