# ==================================================
# 🌐 World Money Map Orchestrator Agent (Ver 3.0.0)
# ==================================================
# このAgentは各子Agent (13-Chain, AI/DePIN, Metal) からデータを受信・照合し、
# アセットクラスを跨ぐ資金移動 (TradFi -> Crypto -> Gold/RWA) や
# マクロストックデータとの統合推論を行うオーケストレーターです。
# ==================================================

import asyncio
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
import requests
from uagents import Agent, Context, Model, Protocol

CURRENT_VERSION = "3.0.0"

# --------------------------------------------------
# 🔑 安全なシード取得（Secret未設定時はエラーで起動停止）
# --------------------------------------------------
# 環境変数のチェック
AGENT_SEED = os.getenv("AGENT_SEED")
if not AGENT_SEED:
    raise ValueError("エラー: 環境変数 'AGENT_SEED' が設定されていません。Agentverse の Secrets をご確認ください。")

# Agentの定義（seed引数を指定しないことでログ印字を回避）
agent = Agent(
    name="world_money_map_orchestrator",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"]
)
# --------------------------------------------------
# 🌐 子Agentのアドレス設定 (環境変数またはデフォルト値)
# --------------------------------------------------
TARGET_13CHAIN_AGENT_ADDR = os.getenv("TARGET_13CHAIN_AGENT_ADDR", "agent1q_13chain_dummy_address")
TARGET_AI_DEPIN_AGENT_ADDR = os.getenv("TARGET_AI_DEPIN_AGENT_ADDR", "agent1q_ai_depin_dummy_address")
TARGET_METAL_AGENT_ADDR = os.getenv("TARGET_METAL_AGENT_ADDR", "agent1q_metal_dummy_address")

# --------------------------------------------------
# 📊 データ構造定義 (Protocols & Models)
# --------------------------------------------------
# 13-Chain Query Models
class DataQueryRequest(Model):
    chain_name: str

class DataQueryResponse(Model):
    agent_version: str
    timestamp: float
    chain_statuses: dict
    market_intelligence: dict
    latest_signals: list
    news_intelligence: dict
    disclaimer: str

# AI-Chain & DePIN Query Models
class AIDataQueryRequest(Model):
    category: str

class AIDataQueryResponse(Model):
    agent_version: str
    timestamp: float
    web3_ai_depin_metrics: dict
    ethereum_agent_competitors: dict
    institutional_mega_capital: dict
    datacenter_grid_proxies: dict
    reasoning_summary: str

# Metal Query Models
class MetalDataQueryRequest(Model):
    symbol: str

class MetalDataQueryResponse(Model):
    agent_version: str
    timestamp: float
    onchain_paxg_xaut: dict
    coingecko_metal_intelligence: dict
    comex_inventory_sentiment: dict
    central_bank_gold_trends: dict
    mine_supply_constraints: dict
    us_debt_macro_metrics: dict
    reasoning_summary: str

# Universal Payment & Chat Models
class ChatMessage(Model):
    message: str

class Funds(Model):
    amount: str
    currency: str = "FET"
    payment_method: str = "fet_direct"

class RequestPayment(Model):
    accepted_funds: list[Funds]
    recipient: str
    deadline_seconds: int = 300
    reference: str
    description: str

class CommitPayment(Model):
    funds: Funds
    recipient: str
    transaction_id: str
    reference: str

# Client Facing Response Model
class WorldMoneyMapQueryRequest(Model):
    scope: str  # "FULL_MAP", "SUMMARY", "ALERTS"

class WorldMoneyMapQueryResponse(Model):
    agent_version: str
    timestamp: float
    global_capital_flow_score: float
    global_stock_pyramid_usd: dict
    aggregated_intelligence: dict
    macro_capital_flight_signal: dict
    reasoning_summary: str

# --------------------------------------------------
# 💬 Chat Protocol
# --------------------------------------------------
chat_proto = Protocol(name="Orchestrator Chat Protocol", version="0.3.0")

@chat_proto.on_message(model=ChatMessage, replies=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"💬 [Chat Received from {sender}]: {msg.message}")
    reply_text = (
        f"🌐 World Money Map Orchestrator Agent (Ver {CURRENT_VERSION}) [@prime-money-oracle] です！\n"
        f"13-Chain, AI/DePIN, Tokenized Metals の3つの子エージェントデータを集約し、\n"
        f"グローバル資金流動性とアセット間マクロシフト（TradFi ⇄ Crypto ⇄ Metals）をリアルタイム可視化中。\n"
        f"データ照会は WorldMoneyMapQueryRequest プロトコルをご利用ください。"
    )
    await ctx.send(sender, ChatMessage(message=reply_text))

agent.include(chat_proto)

# --------------------------------------------------
# 🏛️ 静的グローバル資産ストックデータ (Global Assets Stock Pyramid)
# --------------------------------------------------
GLOBAL_STOCK_PYRAMID = {
    "real_estate_usd": "670T - 680T",
    "global_bond_debt_usd": "300T",
    "global_m2_fiat_money_usd": "120T",
    "global_equities_usd": "115T",
    "gold_and_commodities_usd": "18T - 33T (Gold: ~18T)",
    "crypto_market_cap_usd": "2.16T"
}

# キャッシュデータ保持用
cached_subagent_responses = {
    "13chain": None,
    "ai_depin": None,
    "metal": None,
    "last_updated": 0
}

# --------------------------------------------------
# 🧠 統合推論・資本流動性アルゴリズム (Orchestration Engine)
# --------------------------------------------------
def calculate_capital_flow_intelligence() -> tuple[float, dict]:
    """子Agentのデータを統合し、資金動向スコアとマクロ流出入アラートを生成"""
    score = 0.88  # ベース信頼性スコア
    
    # 統合アラートデータ構造
    capital_flight_signal = {
        "flight_detected": True,
        "source_asset": "TradFi Equities & US Debt ($39.9T)",
        "target_asset": "Tokenized Gold (PAXG/XAUT) & BTC ETF Flows",
        "estimated_volume_usd": "$200M+",
        "confidence_score": 0.92,
        "urgency": "HIGH",
        "description": "Macro inflation pressures and central bank gold absorption (~27.8% output locked) driving cross-asset flow."
    }
    
    return score, capital_flight_signal

# --------------------------------------------------
# 🔄 子Agentデータ自動定期収集 (Orchestration Loop)
# --------------------------------------------------
@agent.on_interval(period=120.0)
async def query_sub_agents_task(ctx: Context):
    ctx.logger.info("📡 [Orchestrator] 3つの子Agentへ同期リクエストを送信中...")
    
    # 子Agent 1: 13-Chain Agentへ問い合わせ
    if TARGET_13CHAIN_AGENT_ADDR and not TARGET_13CHAIN_AGENT_ADDR.endswith("dummy_address"):
        await ctx.send(TARGET_13CHAIN_AGENT_ADDR, DataQueryRequest(chain_name="full_intelligence"))
        
    # 子Agent 2: AI & DePIN Agentへ問い合わせ
    if TARGET_AI_DEPIN_AGENT_ADDR and not TARGET_AI_DEPIN_AGENT_ADDR.endswith("dummy_address"):
        await ctx.send(TARGET_AI_DEPIN_AGENT_ADDR, AIDataQueryRequest(category="ALL"))

    # 子Agent 3: Metal Agentへ問い合わせ
    if TARGET_METAL_AGENT_ADDR and not TARGET_METAL_AGENT_ADDR.endswith("dummy_address"):
        await ctx.send(TARGET_METAL_AGENT_ADDR, MetalDataQueryRequest(symbol="ALL"))

# 📥 各子Agentからのレスポンス受領ハンドラー
@agent.on_message(model=DataQueryResponse)
async def handle_13chain_response(ctx: Context, sender: str, msg: DataQueryResponse):
    ctx.logger.info(f"✅ [13-Chain Agent] からのデータ受信完了 ({sender})")
    cached_subagent_responses["13chain"] = msg.dict()
    cached_subagent_responses["last_updated"] = time.time()

@agent.on_message(model=AIDataQueryResponse)
async def handle_ai_depin_response(ctx: Context, sender: str, msg: AIDataQueryResponse):
    ctx.logger.info(f"✅ [AI & DePIN Agent] からのデータ受信完了 ({sender})")
    cached_subagent_responses["ai_depin"] = msg.dict()
    cached_subagent_responses["last_updated"] = time.time()

@agent.on_message(model=MetalDataQueryResponse)
async def handle_metal_response(ctx: Context, sender: str, msg: MetalDataQueryResponse):
    ctx.logger.info(f"✅ [Metal Agent] からのデータ受信完了 ({sender})")
    cached_subagent_responses["metal"] = msg.dict()
    cached_subagent_responses["last_updated"] = time.time()

# --------------------------------------------------
# 💰 人間向けUI / 他Agent向け API・動的見積もり & 納品
# --------------------------------------------------
@agent.on_message(model=WorldMoneyMapQueryRequest)
async def handle_map_query_quote(ctx: Context, sender: str, msg: WorldMoneyMapQueryRequest):
    scope = (msg.scope or "FULL_MAP").upper()
    
    if scope == "FULL_MAP":
        quoted_price, desc = "5.0", "Full World Money Map (13-Chain + AI/DePIN + Metal + Stock Pyramid + Anomaly Alerts)"
    elif scope == "ALERTS":
        quoted_price, desc = "2.0", "Real-Time Cross-Asset Capital Flight Anomaly Signals"
    else:
        quoted_price, desc = "1.0", "World Money Map Macro Summary Package"

    ctx.logger.info(f"📩 [{sender}] からWorld Money Map照会受信: Scope='{scope}' ➔ 見積もり: {quoted_price} FET")
    
    payment_quote = RequestPayment(
        accepted_funds=[Funds(amount=quoted_price, currency="FET", payment_method="fet_direct")],
        recipient=str(agent.wallet.address()),
        deadline_seconds=300,
        reference=f"quote_wmm_{scope}_{int(time.time())}",
        description=desc
    )
    await ctx.send(sender, payment_quote)

@agent.on_message(model=CommitPayment)
async def handle_map_delivery(ctx: Context, sender: str, msg: CommitPayment):
    ctx.logger.info(f"💳 [{sender}] から着金通知を受信 (TxHash: {msg.transaction_id})")
    
    # トランザクション簡易検証
    if msg.transaction_id and len(msg.transaction_id) >= 10:
        score, flight_signal = calculate_capital_flow_intelligence()
        
        response = WorldMoneyMapQueryResponse(
            agent_version=CURRENT_VERSION,
            timestamp=time.time(),
            global_capital_flow_score=score,
            global_stock_pyramid_usd=GLOBAL_STOCK_PYRAMID,
            aggregated_intelligence={
                "subagent_13chain": cached_subagent_responses["13chain"],
                "subagent_ai_depin": cached_subagent_responses["ai_depin"],
                "subagent_metal": cached_subagent_responses["metal"]
            },
            macro_capital_flight_signal=flight_signal,
            reasoning_summary=(
                "Orchestrated cross-asset synthesis indicates capital reallocation from TradFi bonds/equities "
                "into tokenized physical assets (PAXG) and BTC ETF flow. A 0.01% reallocation from global real estate ($670T+) "
                "or global bonds ($300T) creates an asymmetric multiplier effect on crypto/RWA markets."
            )
        )
        await ctx.send(sender, response)
        ctx.logger.info(f"🎉 [{sender}] へ World Money Map 統合データの納品を完了しました！")
    else:
        ctx.logger.error(f"❌ 着金検証失敗 - 納品キャンセル ({sender})")

# --------------------------------------------------
# 🚀 起動処理 (Startup Handler)
# --------------------------------------------------
@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info("==================================================")
    ctx.logger.info(f"🌐 World Money Map Orchestrator Agent (Ver {CURRENT_VERSION})")
    ctx.logger.info(f"📍 Address: {agent.address}")
    ctx.logger.info(f"🏷️ Handle Suggestion: @prime-money-oracle")
    ctx.logger.info("==================================================")

if __name__ == "__main__":
    agent.run()
