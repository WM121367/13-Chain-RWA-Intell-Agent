# 🤖 13-Chain Unified Ledger RWA, Metal & Macro Intelligence Agent (v2.4.0)

> **A Multi-Chain On-Chain Surveillance, RWA/Metal Market Scanner & Global Macro Intelligence Engine powered by uAgents Protocol with X402 Payment Retry Support.**

`13-Chain Unified Ledger Spy Agent` is an autonomous AI agent that monitors smart contract events and liquidity movements in real time across 13 major blockchains (EVM, Non-EVM, and dedicated RWA chains). It integrates and analyzes real-time market data for RWAs and commodities (Gold/Metal) via the CoinGecko API alongside primary institutional intelligence (RSS/IR/X402 developments from supranational entities, governments, and major banks) to generate high-precision alpha signals.

---

## 🚀 Key Features

* **13-Chain Multi-Ledger Monitoring:**
  * Tracks block height, event logs, and contract updates across all **13 chains**: Sepolia (Ethereum), Bitcoin, XRPL, Linea, Base, Solana, Hedera, TRON, Canton, Stellar, Algorand, XDC, and Quant.
  * Real-time detection of `Transfer` events for specific RWA contracts such as LINK, CCIP Router, and Ondo Finance.
* **CoinGecko RWA & Metal Category Intelligence:**
  * Automatically scans market and price trends for `real-world-assets-rwa` (general RWA) and `gold-backed` / `commodity-backed` (metal and commodity tokens) via CoinGecko API following 13-Chain surveillance.
  * Instantly detects 24-hour price surges (+10% or more) and volume spikes, logging and alerting on-chain activity.
* **Global Macro, Institutional & X402 Intelligence Engine:**
  * Automatically monitors press releases from supranational agencies, public institutions, and mega-banks (BRICS Pay, WEF, US House Financial Services Committee, SEC, CFTC, US Treasury, Federal Reserve, ECB, BIS, SSA).
  * Detects developments in the **X402 Protocol** (agent-to-agent payment standard) and agentic payments using correlation algorithms.
  * Executes automated correlation reasoning between macro news and on-chain activity via `KEYWORD_MAP` matching algorithms (calculating Confidence Scores).
* **X402 / uAgents Retry Payment Protocol (NEW):**
  * Executes up to 3 asynchronous retry verifications (at 3-second intervals) upon receiving payment notifications (`CommitPayment`) from client agents.
  * Implements robust error handling for unconfirmed or delayed payments (HTTP 402-style retry request notifications) to enhance the reliability of agent-to-agent commerce.
* **uAgents Protocol Integration & Dynamic Quoting:**
  * Fully compliant with the uAgents standard. Delivers dynamic quotes (payable in FET) based on the requested query scope (`full_intelligence`, `market`, `macro`, `summary`, `single_chain`) and executes automated data delivery upon payment verification.
* **Embedded Legal & Security Guardrails:**
  * Automatically embeds a `NOT FINANCIAL ADVICE` disclaimer into response outputs to mitigate unregistered investment advice risks.

---

## 🏗️ Architecture Overview

```text
┌─────────────────────────────────────────────────────────────┐
│    Global Macro & Regulatory RSS Collector (BRICS/WEF/Fed)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ News Text & Topic Extraction
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                13-Chain Intelligence Core Engine            │
└──────┬───────────────────────┬───────────────────────┬──────┘
       │                       │                       │
       ▼                       ▼                       ▼
【13-Chain Watcher】     【Correlated Processing】  【CoinGecko Category Scanner】
・Alchemy / Node        ・Confidence Score      ・RWA & Metal Market Data
・BUIDL / RLUSD         ・X402 Retry Logic      ・Volume Spike / 24h Trend
```
🛠️ Usage & Protocols
Message Models
DataQueryRequest: Submit a query specifying chain_name (e.g., "full", "market", "macro", "all", "sepolia").

RequestPayment / CommitPayment: Returns data delivery JSON instantly after payment processing (0.1 ~ 3.0 FET) and retry verification.

⚠️ Disclaimer
This agent is developed for informational and analytical purposes only. NOT FINANCIAL ADVICE. All analytical signals produced by this 13-Chain agent should be used purely for research and tool-level insights.
```
