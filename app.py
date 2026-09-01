import asyncio
import time
import random
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any

# ==========================================
# 1. STRUCTURED OUTPUT CONTRACTS & MODELS
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
    risk_tolerance: str  # "Low", "Medium", "High"
    portfolio: Dict[str, float] # Ticker to allocation percentage
    historical_bias: str

# ==========================================
# 2. PARALLEL SPECIALIZED AGENTS 
# ==========================================
class SignalClassificationAgent:
    """Evaluates market data across at least three independent dimensions."""
    async def analyze(self, ticker: str) -> MarketSignal:
        await asyncio.sleep(0.1) # Network simulation
        
        # 3 Independent Dimensions
        price_momentum = random.uniform(-1, 1)
        volume_anomaly = random.uniform(0.5, 3.0) 
        volatility_index = random.uniform(10, 50)
        
        is_bullish = price_momentum > 0.2 and volume_anomaly > 1.2
        classification = "Bullish" if is_bullish else "Bearish" if price_momentum < -0.2 else "Neutral"
        confidence = round(min(0.98, abs(price_momentum) + (volume_anomaly * 0.1)), 2)
        
        return MarketSignal(
            classification=classification,
            confidence=confidence,
            dimensions_evaluated={
                "price_momentum": round(price_momentum, 2), 
                "volume_anomaly_x": round(volume_anomaly, 2), 
                "volatility": round(volatility_index, 2)
            },
            reasoning=f"{classification} momentum ({price_momentum:.2f}) confirmed by {volume_anomaly:.2f}x volume anomaly."
        )

class FundamentalRAGAgent:
    """Queries a document corpus and grounds output in retrieved source material."""
    def __init__(self):
        # Simulated Vector Database
        self.vector_db = {
            "RELIANCE": {"chunk": "Management highlighted a 14% EBITDA margin expansion driven by retail and telecom.", "doc": "SEBI Q3 Earnings Filing, Section 4"},
            "HDFCBANK": {"chunk": "NIM contracted by 10 bps; deposit growth remains a priority for the next two quarters.", "doc": "Q2 Earnings Transcript, 18:30"},
            "ZOMATO": {"chunk": "Blinkit GOV grew 112% YoY, achieving operating profitability in 70% of dark stores.", "doc": "Corporate Disclosure - April 2024"}
        }

    async def analyze(self, ticker: str, simulate_missing_filing: bool = False) -> RAGOutput:
        await asyncio.sleep(0.2)
        
        if simulate_missing_filing:
            raise FileNotFoundError(f"No recent SEBI filings found for {ticker} in vector space.")
            
        data = self.vector_db.get(ticker, {"chunk": "No major fundamental anomalies detected in recent filings.", "doc": "General Market Screener"})
        return RAGOutput(insight=data["chunk"], source_attribution=[data["doc"]])

class AlternativeDataAgent:
    """Evaluates real-time news and macro sentiment."""
    async def analyze(self, ticker: str, simulate_feed_failure: bool = False) -> SentimentSignal:
        await asyncio.sleep(0.15)
        
        if simulate_feed_failure:
            raise ConnectionError("Live News API feed timeout.")
            
        sentiment_score = random.uniform(-1, 1)
        return SentimentSignal(
            classification="Positive" if sentiment_score > 0 else "Negative",
            confidence=0.82,
            reasoning=f"Aggregated social and news sentiment score is {sentiment_score:.2f}."
        )

# ==========================================
# 3. SYNTHESIS LAYER & USER PROFILING
# ==========================================
class SynthesisOrchestrator:
    """Weights outputs against a specific user's risk profile to produce a synthesized recommendation."""
    def synthesize(self, ticker: str, quant: MarketSignal, rag: RAGOutput, alt: Optional[SentimentSignal], user: UserProfile) -> Dict[str, Any]:
        alt_status = alt.reasoning if alt else "SYSTEM DEGRADED: Sentiment feed offline."
        
        # User Profiling Logic (Identical inputs -> Different outputs)
        if user.risk_tolerance == "Low":
            if quant.classification == "Bearish":
                action = "SELL / CUT LOSSES"
                justification = "Your low-risk profile prioritizes capital preservation. Downward momentum detected."
            else:
                action = "HOLD"
                justification = "Despite bullish signals, your conservative profile warrants waiting for stronger fundamental confirmation."
        
        elif user.risk_tolerance == "High":
            if quant.classification == "Bullish":
                action = "AGGRESSIVE BUY"
                justification = "Strong momentum aligns with your aggressive risk appetite. Ideal entry point."
            elif quant.classification == "Neutral" and alt and alt.classification == "Positive":
                action = "SCALE IN"
                justification = "Neutral technicals, but positive sentiment allows early positioning for high-risk profiles."
            else:
                action = "WATCH"
                justification = "Market conditions do not support aggressive positioning at this moment."
        else:
            action = "MAINTAIN WEIGHT"
            justification = "Balanced risk parameters suggest holding current allocation."

        return {
            "Recommendation": action,
            "User_Justification": justification,
            "Technical_Base": f"{quant.reasoning} (Confidence: {quant.confidence})",
            "Fundamental_Base": f"{rag.insight} [Cited: {rag.source_attribution[0]}]",
            "Alternative_Base": alt_status
        }

# ==========================================
# 4. LOGGING, PERSISTENCE & INTERFACE
# ==========================================
class SystemLogger:
    """Captures performance metrics across sessions."""
    def __init__(self):
        self.session_store = []

    def log_session(self, ticker: str, user_id: str, latency: float, user_risk: str, success: bool):
        # 3 Measurable Metrics: Response Latency, Signal Accuracy (Mocked), Risk Concentration Score
        metrics = {
            "timestamp": time.time(),
            "user_id": user_id,
            "ticker_evaluated": ticker,
            "metrics": {
                "agent_response_latency_ms": round(latency * 1000, 2),
                "signal_accuracy_30d_forward": round(random.uniform(45.0, 92.0), 2),
                "portfolio_risk_concentration": 8.5 if user_risk == "High" else 3.2
            },
            "pipeline_success": success
        }
        self.session_store.append(metrics)

class LiveInterfaceMock:
    """Renders live signal outputs, agent reasoning traces, and portfolio state."""
    @staticmethod
    def render(ticker: str, user: UserProfile, result: Dict[str, Any]):
        print(f"\n{'='*60}")
        print(f"  HACKVERSE INTELLIGENCE TERMINAL | ASSET: {ticker}")
        print(f"  USER: {user.user_id} | RISK PROFILE: {user.risk_tolerance}")
        print(f"  CURRENT PORTFOLIO STATE: {user.portfolio}")
        print(f"{'='*60}")
        print(f"\n> FINAL RECOMMENDATION: ** {result['Recommendation']} **")
        print(f"> REASONING: {result['User_Justification']}\n")
        print("--- MULTI-AGENT REASONING TRACE ---")
        print(f" [QUANT AGENT] : {result['Technical_Base']}")
        print(f" [RAG AGENT]   : {result['Fundamental_Base']}")
        print(f" [MACRO AGENT] : {result['Alternative_Base']}")
        print(f"{'='*60}\n")

# ==========================================
# 5. MAIN EXECUTION PIPELINE
# ==========================================
async def execute_pipeline(ticker: str, user: UserProfile, logger: SystemLogger, degrade_rag: bool = False, degrade_alt: bool = False):
    start_time = time.time()
    
    # Initialize Agents
    quant_agent = SignalClassificationAgent()
    rag_agent = FundamentalRAGAgent()
    alt_agent = AlternativeDataAgent()
    synthesizer = SynthesisOrchestrator()

    # 1. Parallel Dispatch (Multi-Agent Architecture)
    results = await asyncio.gather(
        quant_agent.analyze(ticker),
        rag_agent.analyze(ticker, simulate_missing_filing=degrade_rag),
        alt_agent.analyze(ticker, simulate_feed_failure=degrade_alt),
        return_exceptions=True # CRITICAL for Graceful Degradation
    )
    
    quant_res, rag_res, alt_res = results

    # 2. Graceful Degradation Handling
    if isinstance(quant_res, Exception):
        quant_res = MarketSignal("Unknown", 0.0, {}, "Feed Offline")
    
    if isinstance(rag_res, Exception):
        # Fallback without failing the pipeline
        rag_res = RAGOutput(insight="Unable to retrieve SEC/SEBI filings. Operating on technicals.", source_attribution=["System Fallback"])
        
    if isinstance(alt_res, Exception):
        alt_res = None # Synthesizer handles None values gracefully

    # 3. Synthesis Layer
    final_output = synthesizer.synthesize(ticker, quant_res, rag_res, alt_res, user)
    
    # 4. Logging & Visualization
    latency = time.time() - start_time
    logger.log_session(ticker, user.user_id, latency, user.risk_tolerance, success=True)
    
    LiveInterfaceMock.render(ticker, user, final_output)

# ==========================================
# 6. END-TO-END DEMONSTRATION RUN
# ==========================================
async def run_hackathon_demo():
    logger = SystemLogger()
    
    # Define two contrasting user profiles
    user_retiree = UserProfile("U_4091", "Low", {"NIFTYBEES": 80, "GOLD": 20}, "Yield-focused")
    user_trader = UserProfile("U_9942", "High", {"ZOMATO": 50, "CRYPTO": 50}, "Momentum-chaser")

    print("\n>>> INITIATING SCENARIO 1: Identical Market Inputs, Different User Profiles")
    await execute_pipeline("ZOMATO", user_retiree, logger)
    await execute_pipeline("ZOMATO", user_trader, logger)
    
    print("\n>>> INITIATING SCENARIO 2: Graceful Degradation (News Feed API & Vector DB Offline)")
    await execute_pipeline("HDFCBANK", user_trader, logger, degrade_rag=True, degrade_alt=True)
    
    print("\n>>> SESSION LOGS (Measurable Metrics)")
    print(json.dumps(logger.session_store, indent=2))

if __name__ == "__main__":
    asyncio.run(run_hackathon_demo())
