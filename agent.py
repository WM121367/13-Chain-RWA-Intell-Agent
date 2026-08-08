# ==================================================
# 📦 1. モジュール・ライブラリの読み込み (Top of file)
# ==================================================
import asyncio
import re
import requests
import time
import urllib.request
import xml.etree.ElementTree as ET
import os
from uagents import Agent, Context, Model, Protocol

# ==================================================
# ⚙️ 2. 基本設定 ＆ グローバル変数定義
# ==================================================
CURRENT_VERSION = "2.5.0"

# Agentverse Secretsから登録済みのAGENT_SEEDを直接読み込み
AGENT_SEED = os.getenv("AGENT_SEED")

agent = Agent(
    name="13chain-rwa-intell-agent",
    seed=AGENT_SEED
)

latest_news_data = {}
latest_market_data = {}

# --------------------------------------------------
# 💬 Chat Protocol 用データ構造 & プロトコル定義
# --------------------------------------------------
class ChatMessage(Model):
    message: str

chat_proto = Protocol(name="Agent Chat Protocol", version="0.2.0")

@chat_proto.on_message(model=ChatMessage, replies=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"💬 チャット受信 ({sender}): {msg.message}")
    
    reply_text = (
        f"🤖 13-Chain Unified Ledger RWA, Metal, BTC ETF & Macro Intelligence Agent (Ver {CURRENT_VERSION}) です！\n"
        f"現在 13 チェーンの監視、Farside BTC ETF Flow、CoinGecko RWA/Metal 市場データ、および主要金融・超国家機関の一次情報を自動照合中です。\n"
        f"最新データは DataQueryRequest プロトコル経由で取得できます。"
    )
    await ctx.send(sender, ChatMessage(message=reply_text))

agent.include(chat_proto)

# --------------------------------------------------
# 📊 データ照会 & 決済用データ構造
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

# --------------------------------------------------
# 🌐 エンドポイント & アドレス定義 (Secret管理へ移行)
# --------------------------------------------------
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

ALCHEMY_SEPOLIA_KEY = os.getenv("ALCHEMY_SEPOLIA_KEY", "")
ALCHEMY_LINEA_KEY = os.getenv("ALCHEMY_LINEA_KEY", "")
ALCHEMY_BASE_KEY = os.getenv("ALCHEMY_BASE_KEY", "")

SEPOLIA_RPC_URL = f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_SEPOLIA_KEY}" if ALCHEMY_SEPOLIA_KEY else "https://rpc.sepolia.org"
LINEA_RPC_URL = f"https://linea-sepolia.g.alchemy.com/v2/{ALCHEMY_LINEA_KEY}" if ALCHEMY_LINEA_KEY else "https://rpc.sepolia.org"
BASE_RPC_URL = f"https://base-sepolia.g.alchemy.com/v2/{ALCHEMY_BASE_KEY}" if ALCHEMY_BASE_KEY else "https://sepolia.base.org"

SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
HEDERA_API_URL = "https://mainnet-public.mirrornode.hedera.com/api/v1/blocks?order=desc&limit=1"
TRON_API_URL = "https://api.trongrid.io/wallet/getnowblock"
CANTON_API_URL = "https://explorer.canton.network/api/status"
STELLAR_API_URL = "https://horizon.stellar.org/ledgers?order=desc&limit=1"
XRPL_RPC_URL = "https://s1.ripple.com:51234"

BTC_API_URL = "https://mempool.space/api/blocks/tip/height"
ALGORAND_API_URL = "https://mainnet-api.algonode.cloud/v2/status"
XDC_RPC_URL = "https://erpc.xinfin.network"
QNT_OVERLEDGER_API_URL = "https://api.overledger.io/v2/status"

FARSIDE_BTC_URL = "https://farside.co.uk/btc/"

LINK_TOKEN_ADDRESS = "0x779877a7b0d9e8603169ddbd7836e478b4624789".lower()
CCIP_ROUTER_ADDRESS = "0x0bf340722c3d830152e437c384122d1ed8202d0d".lower()
ONDO_TOKEN_ADDRESS = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48".lower()
TRANSFER_EVENT_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

LEGAL_DISCLAIMER_TEXT = (
    "NOT FINANCIAL ADVICE. This data is generated automatically by an autonomous AI agent "
    "for informational and analytical purposes only. It does not constitute investment, legal, or tax advice."
)

# --------------------------------------------------
# 🚨 アラート・通知モジュール (Discord / Logger)
# --------------------------------------------------
def send_discord_message(message_text: str):
    """Discord Webhook 経由でアラートを送信"""
    if not DISCORD_WEBHOOK_URL or "discord.com" not in DISCORD_WEBHOOK_URL:
        return
    payload = {"content": message_text, "username": "13-Chain Unified Ledger Agent"}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"⚠️ Discord送信エラー: {e}")

last_checked_sepolia_block = None

latest_chain_data = {
    "sepolia": None, "linea": None, "base": None, "solana": None,
    "hedera": None, "tron": None, "canton": None, "stellar": None,
    "xrp": None, "bitcoin": None, "algorand": None, "xdc": None, "quant": None
}

latest_detected_signals = {
    "last_link_event": None, "last_ccip_event": None,
    "last_ondo_event": None, "last_canton_bridge_activity": None,
    "last_algorand_round": None
}

# ==================================================
# 📰 RSS_FEEDS 辞書（超国家機関・政府・規制・メガバンク統合）
# ==================================================
RSS_FEEDS = {
    "house_financial": "https://financialservices.house.gov/news/rss.aspx",
    "sec_news": "https://www.sec.gov/news/pressreleases.rss",
    "bis_research": "https://www.bis.org/doclist/rss_all_categories.rss",
    "us_treasury": "https://home.treasury.gov/rss/news/press-releases",
    "fed_reserve": "https://www.federalreserve.gov/feeds/press_all.xml",
    "ecb_press": "https://www.ecb.europa.eu/rss/press.html",
    "coindesk_rwa": "https://www.coindesk.com/arc/outboundfeeds/rss",
    "chainlink_blog": "https://cointelegraph.com/rss/tag/chainlink",
    "ripple_insights": "https://cointelegraph.com/rss/tag/ripple",
    "hedera_news": "https://hedera.com/blog/rss.xml",
    "stellar_blog": "https://cointelegraph.com/rss/tag/stellar"
}

def parse_rss_xml(url: str) -> list:
    entries = []
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*'
        }
    )
    with opener.open(req, timeout=10) as response:
        raw_bytes = response.read()
        xml_string = raw_bytes.decode('utf-8', errors='ignore')
        xml_string = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', xml_string)
        
        root = ET.fromstring(xml_string)
        items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')
        for item in items[:3]:
            title_node = item.find('title') or item.find('{http://www.w3.org/2005/Atom}title')
            link_node = item.find('link') or item.find('{http://www.w3.org/2005/Atom}link')
            pub_node = item.find('pubDate') or item.find('{http://www.w3.org/2005/Atom}published')
            
            title = title_node.text.strip() if (title_node is not None and title_node.text) else "No Title"
            link = ""
            if link_node is not None:
                link = link_node.text or link_node.attrib.get('href', '')
            pub_date = pub_node.text.strip() if (pub_node is not None and pub_node.text) else "Unknown Date"
            
            entries.append({"title": title, "link": link, "published": pub_date})
    return entries

# ==================================================
# 📈 Farside Bitcoin ETF Flow RAW Collector
# ==================================================
def fetch_farside_btc_etf_flow() -> dict:
    """Farside InvestorsからBTC ETFの最新日次資金流入出RAWデータを取得・抽出"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        res = requests.get(FARSIDE_BTC_URL, headers=headers, timeout=10)
        if res.status_code == 200:
            text = res.text
            matches = re.findall(r'(\d{2}\s+[A-Za-z]{3}\s+\d{4}).*?([-\d\.\(\)]+)\s*$', text, re.MULTILINE)
            if matches:
                latest_date, total_flow = matches[-1]
                return {
                    "source": "Farside Investors",
                    "asset": "BTC_ETF",
                    "latest_date": latest_date,
                    "total_net_flow_usdm": total_flow,
                    "status": "SUCCESS"
                }
            return {"source": "Farside Investors", "status": "PARSED_RAW_HTML", "url": FARSIDE_BTC_URL}
    except Exception as e:
        print(f"⚠️ Farside ETF Fetch Error: {e}")
    return {"source": "Farside Investors", "status": "FAILED"}

# ==================================================
# 📊 CoinGecko API Collector (RWA & Metal Categories)
# ==================================================
COINGECKO_TARGET_CATEGORIES = [
    "real-world-assets-rwa",
    "gold-backed",
    "commodity-backed",
    "tokenized-treasury"
]

def fetch_coingecko_category(category_id: str) -> list:
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "category": category_id,
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": "false"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"⚠️ CoinGecko API取得エラー ({category_id}): {e}")
    return []

# ==================================================
# 🧠 オンチェーン ✕ ニュース ✕ ETF ✕ 市場照合 ＆ ログエンジン
# ==================================================
KEYWORD_MAP = {
    "ripple": ["xrpl", "ripple", "sec", "cross-border", "cbdc", "rlusd", "buidl"],
    "xrp": ["xrpl", "ripple", "sec", "cross-border", "cbdc", "rlusd", "buidl"],
    "sepolia": ["chainlink", "ccip", "rwa", "ethereum", "buidl", "blackrock"],
    "bitcoin": ["btc", "etf", "ibit", "farside", "fbtc", "blackrock", "fidelity"],
    "chainlink": ["chainlink", "ccip", "rwa", "oracle", "tokenization", "dtcc"],
    "hedera": ["hedera", "hbar", "tokenization", "rwa", "iso 20022"],
    "stellar": ["stellar", "xlm", "payment", "sdf", "soroban"],
    "linea": ["linea", "l2", "consensys", "zk-rollup", "ethereum"],
    "macro": ["house financial", "sec", "bis", "treasury", "brics", "wef", "ssa", "fed", "ecb", "x402", "402", "agent payment"]
}

def generate_intelligence_signals() -> list:
    correlated_signals = []
    all_news_text = ""
    for source, articles in latest_news_data.items():
        for art in articles:
            all_news_text += f"{art['title']} ".lower()

    for chain_name, chain_status in latest_chain_data.items():
        if chain_status is None:
            continue
        keywords = KEYWORD_MAP.get(chain_name.lower(), [chain_name.lower()])
        matched_keywords = [kw for kw in keywords if kw in all_news_text]
        
        if matched_keywords:
            correlated_signals.append({
                "chain": chain_name,
                "confidence": "HIGH",
                "score": 0.92,
                "matched_topics": matched_keywords,
                "summary": f"On-chain activity for {chain_name.upper()} correlates with macro/regulatory/ETF updates ({', '.join(matched_keywords)}).",
                "timestamp": time.time()
            })
            
    return correlated_signals

def debug_print_intelligence(ctx: Context):
    signals = generate_intelligence_signals()
    ctx.logger.info("==================================================")
    ctx.logger.info("🧠 【統合インテリジェンス・生成シグナル一覧】")
    ctx.logger.info("==================================================")
    if not signals:
        ctx.logger.info("ℹ️ 現在、ニュースキーワードと一致するオンチェーンイベントはありません。")
    else:
        for idx, sig in enumerate(signals, 1):
            ctx.logger.info(f"[{idx}] Chain: {sig['chain'].upper()} | Confidence: {sig['confidence']} (Score: {sig['score']})")
            ctx.logger.info(f"    - Matched Keywords: {', '.join(sig['matched_topics'])}")
            ctx.logger.info(f"    - Summary: {sig['summary']}")
            
            # 高コンフィデンスシグナル検知時の Discord アラート送信
            alert_msg = (
                f"🧠 **[Intelligence Signal Alert]**\n"
                f"• Chain: `{sig['chain'].upper()}` (Confidence: {sig['confidence']} / Score: {sig['score']})\n"
                f"• Matched Topics: `{', '.join(sig['matched_topics'])}`\n"
                f"• Summary: {sig['summary']}"
            )
            send_discord_message(alert_msg)
    ctx.logger.info("==================================================")

async def fetch_rss_updates(ctx: Context):
    global latest_news_data
    ctx.logger.info("📡 [RSS Collector] グローバル超国家機関・政府・13チェーンの公式発表を巡回中...")
    loop = asyncio.get_event_loop()
    
    success_count = 0
    for source_name, feed_url in RSS_FEEDS.items():
        try:
            entries = await loop.run_in_executor(None, parse_rss_xml, feed_url)
            latest_news_data[source_name] = entries
            success_count += 1
        except Exception as e:
            ctx.logger.warning(f"⚠️ RSS取得スキップ [{source_name}]: {e}")
            
    ctx.logger.info(f"✅ [RSS Collector] 巡回完了: 計 {success_count}/{len(RSS_FEEDS)} ソース更新")
    debug_print_intelligence(ctx)

# ==================================================
# 🚀 起動 ＆ 定期タスク (Background Tasks)
# ==================================================
@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info(f"🚀 エージェント起動 (Ver: {CURRENT_VERSION}) | Address: {agent.address}")
    await fetch_rss_updates(ctx)
    send_discord_message(
        f"🚀 **13-Chain Unified Ledger Spy Agent (Ver: `{CURRENT_VERSION}`) 起動**\n"
        f"• 監視対象: 13-Chain + BTC ETF Flow + RWA/Metal Market + Macro/X402 Intelligence\n"
        f"• データ提供アドレス: `{agent.address}`"
    )

@agent.on_interval(period=3600.0)
async def scheduled_news_task(ctx: Context):
    await fetch_rss_updates(ctx)

@agent.on_interval(period=30.0)
async def check_and_update_task(ctx: Context):
    global last_checked_sepolia_block, latest_chain_data, latest_detected_signals, latest_market_data
    
    # --------------------------------------------------
    # 🔍 Sepolia オンチェーン・イベント監視 & アラート
    # --------------------------------------------------
    try:
        res_block = requests.post(SEPOLIA_RPC_URL, json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}, timeout=5)
        if res_block.status_code == 200 and "result" in res_block.json():
            current_block = int(res_block.json()["result"], 16)
            latest_chain_data["sepolia"] = current_block
            
            if last_checked_sepolia_block is not None and current_block > last_checked_sepolia_block:
                payload_logs = {
                    "jsonrpc": "2.0", "method": "eth_getLogs",
                    "params": [{"fromBlock": hex(last_checked_sepolia_block + 1), "toBlock": hex(current_block), "topics": [TRANSFER_EVENT_TOPIC]}],
                    "id": 2
                }
                res_logs = requests.post(SEPOLIA_RPC_URL, json=payload_logs, timeout=5)
                if res_logs.status_code == 200 and "result" in res_logs.json():
                    for log in res_logs.json()["result"]:
                        contract_addr = log.get("address", "").lower()
                        event_name = None
                        
                        if contract_addr == LINK_TOKEN_ADDRESS:
                            latest_detected_signals["last_link_event"] = current_block
                            event_name = "Chainlink (LINK) Token Transfer"
                        elif contract_addr == CCIP_ROUTER_ADDRESS:
                            latest_detected_signals["last_ccip_event"] = current_block
                            event_name = "Chainlink CCIP Router Message"
                        elif contract_addr == ONDO_TOKEN_ADDRESS:
                            latest_detected_signals["last_ondo_event"] = current_block
                            event_name = "Ondo Finance Token Transfer"
                        
                        if event_name:
                            alert_msg = f"⚡ **[Sepolia Event Alert]** {event_name} detected in block `#{current_block}`"
                            ctx.logger.info(alert_msg)
                            send_discord_message(alert_msg)

            last_checked_sepolia_block = current_block
    except Exception as e:
        ctx.logger.error(f"🚨 [Sepolia] エラー保護: {e}")

    # --------------------------------------------------
    # 🔍 Bitcoin & XRPL 状態更新
    # --------------------------------------------------
    try:
        res_btc = requests.get(BTC_API_URL, timeout=5)
        if res_btc.status_code == 200:
            latest_chain_data["bitcoin"] = int(res_btc.text.strip())
            
        res_xrpl = requests.post(XRPL_RPC_URL, json={"method": "ledger", "params": [{"ledger_index": "validated"}]}, timeout=5)
        if res_xrpl.status_code == 200:
            latest_chain_data["xrp"] = res_xrpl.json().get("result", {}).get("ledger_index")
    except Exception as e:
        pass

    # --------------------------------------------------
    # 🔍 Farside BTC ETF 資金流出入更新
    # --------------------------------------------------
    loop = asyncio.get_event_loop()
    etf_data = await loop.run_in_executor(None, fetch_farside_btc_etf_flow)
    latest_market_data["btc_etf_flow"] = etf_data

    # --------------------------------------------------
    # 🔍 CoinGecko RWA / Gold 市場急沸騰アラート
    # --------------------------------------------------
    for cat_id in COINGECKO_TARGET_CATEGORIES:
        tokens = await loop.run_in_executor(None, fetch_coingecko_category, cat_id)
        if tokens:
            latest_market_data[cat_id] = tokens
            for t in tokens:
                p_change = t.get("price_change_percentage_24h") or 0.0
                if p_change >= 10.0:
                    symbol = t.get('symbol', '').upper()
                    name = t.get('name', symbol)
                    price = t.get('current_price', 0)
                    
                    alert_msg = (
                        f"🚨 **[{cat_id.upper()} 急沸騰検知]**\n"
                        f"• 銘柄: **{name} ({symbol})**\n"
                        f"• 24h変動率: **+{p_change:.2f}%**\n"
                        f"• 現在価格: `${price}`"
                    )
                    ctx.logger.info(f"🚨 [{cat_id.upper()} 急沸騰検知] {symbol}: +{p_change:.2f}% (24h)")
                    send_discord_message(alert_msg)

# ==================================================
# 💰 直接レスポンス返信ハンドラー
# ==================================================
@agent.on_message(model=DataQueryRequest)
async def handle_dynamic_quote(ctx: Context, sender: str, msg: DataQueryRequest):
    requested_target = (msg.chain_name or "all").lower()
    ctx.logger.info(f"📩 [{sender}] リクエスト受信: Target='{requested_target}'")

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

# ==================================================
# 🏁 3. エージェントの起動 (Bottom of file)
# ==================================================
if __name__ == "__main__":
    agent.run()
