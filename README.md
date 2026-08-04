# 🤖 13-Chain Unified Ledger RWA, Metal & Macro Intelligence Agent (v2.4.0)

> **A Multi-Chain On-Chain Surveillance, RWA/Metal Market Scanner & Global Macro Intelligence Engine powered by uAgents Protocol with X402 Payment Retry Support.**

`13-Chain Unified Ledger Spy Agent` は、13の主要ブロックチェーン（EVM, Non-EVM, RWA専用チェーン）上のスマートコントラクトイベントや流動性移動をリアルタイム監視し、CoinGecko API 経由の RWA / コモディティ（Gold / Metal）市場データ、および超国家機関・政府・主要メガバンクの一次情報（RSS / IR / X402動向）と統合解析して高精度なアルファシグナルを生成する自律型AI Agentです。

---

## 🚀 Key Features

* **13-Chain Multi-Ledger Monitoring:**
  * Sepolia (Ethereum), Bitcoin, XRPL, Linea, Base, Solana, Hedera, TRON, Canton, Stellar, Algorand, XDC, Quant の全 **13-Chain** のブロックハイト、イベントログ、コントラクト更新を監視。
  * LINK, CCIP Router, Ondo Finance などの特定RWAコントラクトの `Transfer` イベントをリアルタイム検知。
* **CoinGecko RWA & Metal Category Intelligence:**
  * 13-Chain 監視の実行後、CoinGecko API から `real-world-assets-rwa`（RWA全般）、`gold-backed` / `commodity-backed`（メタル・コモディティ系トークン）の市場・価格動向を自動スキャン。
  * 24時間の価格急増（+10%以上）やボリュームスパイクを即時に検知してログ・アラート化[cite: 7, 8]。
* **Global Macro, Institutional & X402 Intelligence Engine:**
  * 超国家機関・公的機関・メガバンク（BRICS Pay, WEF, US House Financial Services Committee, SEC, CFTC, US Treasury, Federal Reserve, ECB, BIS, SSA）のプレスリリースを自動巡回[cite: 7, 8]。
  * **X402 Protocol**（エージェント間決済規格）および Agentic Payments に関する動向を相関アルゴリズムで検知[cite: 7, 8]。
  * `KEYWORD_MAP` 照合アルゴリズムによるニュースとオンチェーンアクティビティの自動相関推論（Confidence Score 算出）[cite: 7, 8]。
* **X402 / uAgents Retry Payment Protocol (NEW):**
  * クライアントエージェントからの着金通知（`CommitPayment`）に対し、最大3回（3秒間隔）の非同期リトライ検証を実施[cite: 7]。
  * 決済未確定や遅延時のエラーハンドリング（HTTP 402 風の再試行要求通知）を実装し、エージェント間売買の信頼性を向上[cite: 7]。
* **uAgents Protocol Integration & Dynamic Quoting:**
  * uAgents 規格に準拠。クエリ範囲（`full_intelligence`, `market`, `macro`, `summary`, `single_chain`）に応じた動的な見積もり（FET決済）と着金確認後の自動データ納品処理[cite: 7, 8]。
* **Embedded Legal & Security Guardrails:**
  * 無登録投資助言リスクを回避する `NOT FINANCIAL ADVICE` 免責事項（Disclaimer）の出力レスポンス自動挿入[cite: 7, 8]。

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
DataQueryRequest: chain_name ("full", "market", "macro", "all", "sepolia" など) を指定して照会[cite: 7, 8]。

RequestPayment / CommitPayment: 規定料金（0.1 ~ 3.0 FET）の支払い後、リトライ検証を経て即時にデータ納品 JSON を返却[cite: 7, 8]。

⚠️ Disclaimer
This agent is developed for informational and analytical purposes only. NOT FINANCIAL ADVICE. All analytical signals produced by this 13-Chain agent should be used purely for research and tool-level insights[cite: 7, 8].
```
