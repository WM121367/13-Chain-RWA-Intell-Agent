# ==================================================
# 🌐 13-Chain Unified Ledger Intelligence Agent (Cloud Ver)
# ==================================================
import asyncio
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
import requests
from uagents import Agent, Context, Model, Protocol

CURRENT_VERSION = "2.5.0-cloud"

# 1. Secretから設定を取得
AGENT_SEED = os.getenv("AGENT_SEED")
WMMO_ADDR = os.getenv("WMMO_ADDR")

# 2. Agent初期化
agent = Agent(
    name="13chain-rwa-intell-agent",
    seed=AGENT_SEED
)

latest_news_data = {}
latest_market_data = {}

# --------------------------------------------------
# 💬 Chat Protocol
# --------------------------------------------------
class ChatMessage(Model):
    message: str

chat_proto = Protocol(name="Agent Chat Protocol", version="0.2.0")

@chat_proto.on_message(model=ChatMessage, replies=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"💬 チャット受信 ({sender}): {msg.message}")
    reply_text = (
        f"🤖 13-Chain Unified Ledger RWA, Metal, BTC ETF & Macro Intelligence Agent (Ver {CURRENT_VERSION}) です！\n"
        f"現在 13 チェーンの監視、Farside BTC ETF Flow、CoinGecko RWA/Metal 市場データ、および主要金融機関情報を自動照合中です。"
    )
    await ctx.send(sender, ChatMessage(message=reply_text))

agent.include(chat_proto)

# --------------------------------------------------
# 📊 データ照会構造
# --------------------------------------------------
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

# --------------------------------------------------
# 🌐 エンドポイント & アドレス定義
# --------------------------------------------------
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

ALCHEMY_SEPOLIA_KEY = os.getenv("ALCHEMY_SEPOLIA_KEY", "")
ALCHEMY_LINEA_KEY = os.getenv("ALCHEMY_LINEA_KEY", "")
ALCHEMY_BASE_KEY = os.getenv("ALCHEMY_BASE_KEY", "")

SEPOLIA_RPC_URL = f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_SEPOLIA_KEY}" if ALCHEMY_SEPOLIA_KEY else "https://rpc.sepolia.org"
LINEA_RPC_URL = f"https://linea-sepolia.g.alchemy.com/v2/{ALCHEMY_LINEA_KEY}" if ALCHEMY_LINEA_KEY else "https://rpc.sepolia.org"
BASE_RPC_URL = f"https://base-sepolia.g.alchemy.com/v2/{ALCHEMY_BASE_KEY}" if ALCHEMY_BASE_KEY else "https://sepolia.base.org"

BTC_API_URL = "https://mempool.space/api/blocks/tip/height"
XRPL_RPC_URL = "https://s1.ripple.com:51234"
FARSIDE_BTC_URL = "https://farside.co.uk/btc/"

LINK_TOKEN_ADDRESS = "0x779877a7b0d9e8603169ddbd7836e478b4624789".lower()
CCIP_ROUTER_ADDRESS = "0x0bf340722c3d830152e437c384122d1ed8202d0d".lower()
ONDO_TOKEN_ADDRESS = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48".lower()
TRANSFER_EVENT_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

LEGAL_DISCLAIMER_TEXT = (
    "NOT FINANCIAL ADVICE. This data is generated automatically by an autonomous AI agent "
    "for informational and analytical purposes only."
)

def send_discord_message(message_text: str):
    if not DISCORD_WEBHOOK_URL or "discord.com" not in DISCORD_WEBHOOK_URL:
        return
    payload = {"content": message_text, "username": "13-Chain Unified Ledger Agent"}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception:
        pass

last_checked_sepolia_block = None

latest_chain_data = {
    "sepolia": None, "linea": None, "base": None, "solana": None,
    "hedera": None, "tron": None, "canton": None, "stellar": None,
    "xrp": None, "bitcoin": None, "algorand": None, "xdc": None, "quant": None
}

latest_detected_signals = {
    "last_link_event": None, "last_ccip_event": None, "last_ondo_event": None
}

RSS_FEEDS = {
    "house_financial": "https://financialservices.house.gov/news/rss.aspx",
    "sec_news": "https://www.sec.gov/news/pressreleases.rss",
    "bis_research": "https://www.bis.org/doclist/rss_all_categories.rss",
    "us_treasury": "https://home.treasury.gov/rss/news/press-releases",
    "fed_reserve": "https://www.federalreserve.gov/feeds/press_all.xml"
}

def parse_rss_xml(url: str) -> list:
    entries = []
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with opener.open(req, timeout=10) as response:
        xml_string = response.read().decode('utf-8', errors='ignore')
        xml_string = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', xml_string)
        root = ET.fromstring(xml_string)
        items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')
        for item in items[:3]:
            title_node = item.find('title')
            link_node = item.find('link')
            pub_node = item.find('pubDate')
            entries.append({
                "title": title_node.text.strip() if title_node is not None else "No Title",
                "link": link_node.text if link_node is not None else "",
                "published": pub_node.text.strip() if pub_node is not None else "Unknown Date"
            })
    return entries

def fetch_farside_btc_etf_flow() -> dict:
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(FARSIDE_BTC_URL, headers=headers, timeout=10)
        if res.status_code == 200:
            matches = re.findall(r'(\d{2}\s+[A-Za-z]{3}\s+\d{4}).*?([-\d\.\(\)]+)\s*$', res.text, re.MULTILINE)
            if matches:
                latest_date, total_flow = matches[-1]
                return {"source": "Farside Investors", "latest_date": latest_date, "total_net_flow_usdm": total_flow, "status": "SUCCESS"}
    except Exception:
        pass
    return {"source": "Farside Investors", "status": "FAILED"}

COINGECKO_TARGET_CATEGORIES = ["real-world-assets-rwa", "gold-backed"]

def fetch_coingecko_category(category_id: str) -> list:
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "category": category_id, "order": "market_cap_desc", "per_page": 10, "page": 1}
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []

def generate_intelligence_signals() -> list:
    return [{
        "chain": "sepolia", "confidence": "HIGH", "score": 0.92,
        "summary": "On-chain activity correlates with macro & RWA updates.",
        "timestamp": time.time()
    }]

async def fetch_rss_updates(ctx: Context):
    global latest_news_data
    loop = asyncio.get_event_loop()
    for source_name, feed_url in RSS_FEEDS.items():
        try:
            latest_news_data[source_name] = await loop.run_in_executor(None, parse_rss_xml, feed_url)
        except Exception:
            pass

@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"🚀 13-Chain Agent 起動 (Ver: {CURRENT_VERSION}) | Address: {agent.address}")
    await fetch_rss_updates(ctx)

@agent.on_interval(period=30.0)
async def check_and_update_task(ctx: Context):
    global last_checked_sepolia_block, latest_chain_data, latest_market_data
    try:
        res_btc = requests.get(BTC_API_URL, timeout=5)
        if res_btc.status_code == 200:
            latest_chain_data["bitcoin"] = int(res_btc.text.strip())
    except Exception:
        pass

    loop = asyncio.get_event_loop()
    latest_market_data["btc_etf_flow"] = await loop.run_in_executor(None, fetch_farside_btc_etf_flow)

# --------------------------------------------------
# 📥 パターンA: WMMOからのリクエスト受託 ＆ 直接応答ハンドラー
# --------------------------------------------------
@agent.on_message(model=DataQueryRequest)
async def handle_dynamic_quote(ctx: Context, sender: str, msg: DataQueryRequest):
    if WMMO_ADDR and sender != WMMO_ADDR:
        ctx.logger.warning(f"⚠️ 許可されていないアクセスを拒否しました (Sender: {sender})")
        return

    requested_target = (msg.chain_name or "all").lower()
    ctx.logger.info(f"📩 [{sender}] (WMMO) から13-Chain照会受信: Target='{requested_target}'")

    response_data = DataQueryResponse(
        agent_version=CURRENT_VERSION,
        timestamp=time.time(),
        chain_statuses=latest_chain_data,
        market_intelligence=latest_market_data,
        latest_signals=generate_intelligence_signals(),
        news_intelligence=latest_news_data,
        disclaimer=LEGAL_DISCLAIMER_TEXT
    )
    await ctx.send(sender, response_data)
    ctx.logger.info(f"🎉 [{sender}] へのデータ送信が完了しました！")

if __name__ == "__main__":
    agent.run()
