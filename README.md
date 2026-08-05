# 🤖 13-Chain Unified Ledger & RWA / BTC ETF / Macro Intelligence Agent (Ver 2.5.0)

## 🌟 Overview
This autonomous Agent operates as an institutional-grade intelligence oracle within the Fetch.ai / Agentverse ecosystem. It tracks real-time data across **13 distinct blockchain networks**, monitors **US Spot Bitcoin ETF flows (Farside Investors RAW data)**, analyzes **RWA & Precious Metal markets (CoinGecko)**, and cross-references macro updates from major financial bodies (SEC, BIS, US Treasury, FED, ECB) using a keyword matching engine.

Data access is monetized via the **uAgents / X402 Payment Verification & Retry Protocol** with dynamic quote generation and automated delivery.

---

## 🚀 Key Features (v2.5.0 Update)
- **13-Chain On-Chain Tracking:** Sepolia, Bitcoin, XRPL, Linea, Base, Solana, Hedera, TRON, Canton, Stellar, Algorand, XDC, and Quant Overledger.
- **BTC ETF Flow Integration (NEW):** Real-time daily net inflow/outflow tracking for US Spot Bitcoin ETFs (IBIT, FBTC, BITB, ARKB, GBTC, etc.).
- **RWA & Metal Market Scanning:** Automated monitoring of tokenized treasury, gold-backed tokens, and commodity categories.
- **Macro & Regulatory Correlation Engine:** Automated RSS ingestion from SEC, FED, ECB, BIS, and House Financial Services with confidence scoring.
- **Security Hardened Architecture:** API key encapsulation via environment variables (`Secrets`) and masked log printing for production safety.

---

## 🛠️ Environment Variables (Agentverse Secrets Setup)
To run this agent securely without exposing credentials, configure the following secrets in your environment:

| Key | Description |
|---|---|
| `AGENT_SEED` | Seed phrase for persistent agent address generation |
| `ALCHEMY_SEPOLIA_KEY` | Alchemy API key for Sepolia RPC & log monitoring |
| `ALCHEMY_LINEA_KEY` | Alchemy API key for Linea RPC |
| `ALCHEMY_BASE_KEY` | Alchemy API key for Base RPC |
| `DISCORD_WEBHOOK_URL` | (Optional) Discord Webhook for execution & signal alerts |

---

## 📊 Data Query Protocol (`DataQueryRequest`)
Query targets supported:
- `full` / `intelligence`: Complete package (13-Chain + BTC ETF + RWA/Metal + Macro) — **3.0 FET**
- `market` / `rwa` / `etf`: RWA, Metal & BTC ETF Flow Market Data — **1.5 FET**
- `news` / `macro`: Regulatory & Global Financial News Signals — **1.0 FET**
- `summary`: High-level status across all 13 chains — **0.5 FET**

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
