# 🌐 13-Chain Unified Ledger, Macro Treasury & Regulatory Intelligence Agent

An institutional-grade autonomous multi-chain monitoring and intelligence agent built on the Fetch.ai (uAgents) framework.  
It provides real-time layer-1/layer-2 infrastructure status alongside US Debt Clock macro indicators, regulatory news, and commodity reasoning.

---

## 🚀 Features

* **Multi-Chain Real-Time Monitoring:**  
  Tracks 13+ blockchain networks including Bitcoin, Ethereum (Sepolia), Solana, Linea, Base, XRPL, Stellar, Hedera, Algorand, TRON, Canton, XDC, and Quant.
* **Macro Treasury & US Debt Clock Metrics (New):**  
  Integrates national debt, interest payment momentum, and paper-to-physical leverage ratios to evaluate fiat devaluation pressures and institutional hedging sentiment:
  - **US National Debt Tracking:** Real-time updates on national debt accumulation ($39.9T+)
  - **Daily Interest Load:** Tracking interest burden on treasury reserves ($3.5B+/day)
  - **Macro Valuation Bias:** Evaluates hard asset (Gold/Silver/RWA) rotation demand vs. fiat inflation
* **Legislative & Regulatory Intelligence:**  
  Automated RSS ingestion tracking key policy makers and macro entities:
  - **Legislative & Regulatory:** US House Financial Services Committee, SEC Press Releases
  - **Global Financial Institutions:** BIS (Bank for International Settlements)
  - **Ecosystem & RWA Leaders:** Chainlink (CCIP), Ripple, Hedera, Stellar
* **Autonomous Dynamic Pricing & Data Delivery:**  
  Supports the Fetch.ai Payment Protocol (`RequestPayment` / `CommitPayment`) for instant, agent-to-agent automated data transactions using FET.

---

## 💰 Data Packages & Pricing (FET)

| Package Name | Price | Description |
| :--- | :--- | :--- |
| `single_chain` | **0.1 FET** | Real-time block height and signals for a specified single blockchain network. |
| `summary` / `all` | **0.5 FET** | Complete 13-chain status summary. |
| `news` / `regulatory` | **1.0 FET** | Latest macro financial news, SEC updates, and legislative releases. |
| `full_intelligence` | **3.0 FET** | **Institutional Grade:** On-Chain + Regulatory News + **US Debt Clock & Treasury Macro Metrics**. |

---

## 🧠 Example Signal Output (`full_intelligence`)

```json
{
  "agent_version": "2.1.1",
  "timestamp": 1785704100.0,
  "chain_statuses": {
    "sepolia": 11407863,
    "bitcoin": 882104,
    "xrp": 91048201
  },
  "latest_signals": [
    {
      "chain": "SEPOLIA",
      "confidence": "HIGH",
      "score": 0.92,
      "matched_topics": ["chainlink", "rwa"],
      "summary": "On-chain activity for SEPOLIA correlates with news/regulatory updates (chainlink, rwa)."
    }
  ],
  "macro_treasury_metrics": {
    "total_debt": "$39.9T+",
    "daily_interest": "$3.5B",
    "paper_to_silver_ratio": "CRITICAL_HIGH",
    "fiat_devaluation_signal": "HIGH_INFLATION_PRESSURE",
    "macro_bias": "BULLISH_HARD_ASSETS"
  }
}
```
🔌 Protocols Supported
DataQueryRequest / DataQueryResponse

Agent Payment Protocol (FET Direct Payment via RequestPayment / CommitPayment)

chat_proto (Text Query & Interactive Agent Support)

⚠️ Disclaimer
Not Financial Advice (NFA) / Do Your Own Research (DYOR):

This agent is an automated data processing node designed solely for informational, research, and monitoring purposes. The intelligence provided (including on-chain activity, US debt metrics, news correlation, and market sentiment reasoning) does not constitute investment, financial, or trading advice. Users and autonomous buyer agents should conduct independent research (DYOR) before making any financial decisions.
```
