# 🌐 13-Chain Unified Ledger & Regulatory Intelligence Agent

An autonomous multi-chain monitoring and intelligence agent built on the Fetch.ai (uAgents) framework.  
It provides real-time layer-1/layer-2 infrastructure status alongside macro-financial/regulatory news, market momentum, and tokenized commodity reasoning.

---

## 🚀 Features

* **Multi-Chain Real-Time Monitoring:**  
  Tracks 13+ blockchain networks including Bitcoin, Ethereum (Sepolia), Solana, Linea, Base, XRPL, Stellar, Hedera, Algorand, TRON, Canton, XDC, and Quant.
* **Macro & Regulatory Intelligence:**  
  Automated RSS ingestion tracking key policy makers and macro entities:
  - **Legislative & Regulatory:** US House Financial Services Committee, SEC Press Releases
  - **Global Financial Institutions:** BIS (Bank for International Settlements)
  - **Ecosystem & RWA Leaders:** Chainlink (CCIP), Ripple, Hedera, Stellar
* **CoinGecko Market & Commodity Reasoning (New):**  
  Integrates multi-dimensional market reasoning into signals to validate conviction levels:
  1. **Sector Trends:** RWA (Real-World Assets) sector market cap & volume dynamics
  2. **Trending Topics:** Real-time trending coin searches
  3. **Macro Context:** BTC Dominance & market-wide sentiment
  4. **Commodity Momentum:** Tokenized Gold (PAXG/XAUT) & Silver token market activity
* **Autonomous Dynamic Pricing & Data Delivery:**  
  Supports the Fetch.ai Payment Protocol (`RequestPayment` / `CommitPayment`) for instant, agent-to-agent automated data transactions using FET.

---

## 💰 Data Packages & Pricing (FET)

| Package Name | Price | Description |
| :--- | :--- | :--- |
| `single_chain` | **0.1 FET** | Real-time status for a specified single blockchain network. |
| `summary` / `all` | **0.5 FET** | Complete 13-chain status summary. |
| `news` / `regulatory` | **1.0 FET** | Latest macro financial news, SEC updates, and legislative releases. |
| `full_intelligence` | **3.0 FET** | **Institutional Grade:** On-Chain + Regulatory News + CoinGecko & Gold/Silver Market Reasoning. |

---

## 🧠 Example Signal Output (`full_intelligence`)

```json
{
  "chain": "SEPOLIA",
  "confidence": "HIGH",
  "score": 0.95,
  "summary": "On-chain activity for SEPOLIA correlates with news/regulatory updates (chainlink, rwa).",
  "coingecko_reasoning": {
    "rwa_sector_trend": "+4.2% (24h)",
    "gold_market_momentum": "Gold Tokens 24h Change: +1.8%",
    "silver_market_momentum": "Silver Tokens 24h Change: +3.5%",
    "trending_coins_search": ["LINK", "PAXG", "XRP", "HBAR"],
    "macro_context": "BTC Dominance at 53.4%",
    "conviction_logic": "High institutional interest: On-chain RWA movement aligns with Macro Gold/Silver trends and trending market topics."
  }
```  <-- ここに ``` を追加！

---

### 📄 正しいマークダウンの書き方（例）

```markdown
## 🧠 Example Signal Output (`full_intelligence`)

```json
{
  "chain": "SEPOLIA",
  "confidence": "HIGH",
  "score": 0.95,
  "summary": "On-chain activity for SEPOLIA correlates with news/regulatory updates (chainlink, rwa).",
  "coingecko_reasoning": {
    "rwa_sector_trend": "+4.2% (24h)",
    "gold_market_momentum": "Gold Tokens 24h Change: +1.8%",
    "silver_market_momentum": "Silver Tokens 24h Change: +3.5%",
    "trending_coins_search": ["LINK", "PAXG", "XRP", "HBAR"],
    "macro_context": "BTC Dominance at 53.4%",
    "conviction_logic": "High institutional interest: On-chain RWA movement aligns with Macro Gold/Silver trends and trending market topics."
  }
}
