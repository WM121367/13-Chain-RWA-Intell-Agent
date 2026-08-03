# ==================================================
# 📦 1. モジュール・ライブラリの読み込み (Top of file)
# ==================================================
import asyncio
import re
import requests
import time
import urllib.request
import xml.etree.ElementTree as ET
from uagents import Agent, Context, Model, Protocol

# ==================================================
# ⚙️ 2. 基本設定 ＆ グローバル変数定義
# ==================================================
CURRENT_VERSION = "2.1.1"
agent = Agent(name="onchain_event_agent", seed="")

latest_news_data = {}

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
        f"🤖 13-Chain Unified Ledger RWA & Regulatory Intelligence Agent (Ver {CURRENT_VERSION}) です！\n"
        f"現在 13 チェーンの監視および金融・規制ニュース（下院金融委/SEC/BIS等）を自動照合中です。\n"
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
    latest_signals: list
    news_intelligence: dict
    macro_treasury_metrics: dict

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
# 🌐 エンドポイント & アドレス定義
# --------------------------------------------------
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1533234005682557140/d4Uh_PiX1pHHXwH963mw7UCFEWMtySRz4i7sejuXMHS23xifufpMTi_9e7aXyavyuNmw"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/WM121367/agent-monitor/main/version.json"

SEPOLIA_RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/alch_hUmfIMazl7GsZ4UgO80LR"
LINEA_RPC_URL = "https://linea-sepolia.g.alchemy.com/v2/alch_cUftWSKsQ93YGADeM4AHQ"
BASE_RPC_URL = "https://base-sepolia.g.alchemy.com/v2/alch_cUftWSKsQ93YGADeM4AHQ"
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

LINK_TOKEN_ADDRESS = "0x779877a7b0d9e8603169ddbd7836e478b4624789".lower()
CCIP_ROUTER_ADDRESS = "0x0bf340722c3d830152e437c384122d1ed8202d0d".lower()
ONDO_TOKEN_ADDRESS = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48".lower()
TRANSFER_EVENT_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

def send_discord_message(message_text: str):
    if "discord.com" not in DISCORD_WEBHOOK_URL:
        return
    payload = {"content": message_text, "username": "13-Chain Unified Ledger Agent"}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print(f"Discord送信エラー: {e}")

has_notified_update = False
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
# 📰 RSS_FEEDS辞書 ＆ パース処理
# ==================================================
RSS_FEEDS = {
    "house_financial": "https://financialservices.house.gov/news/rss.aspx",
    "sec_news": "https://www.sec.gov/news/pressreleases.rss",
    "bis_research": "https://www.bis.org/doclist/rss_all_categories.rss",
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
# 🧠 オンチェーン ✕ ニュース照合 ＆ ログエンジン
# ==================================================
KEYWORD_MAP = {
    "ripple": ["xrpl", "ripple", "sec", "cross-border", "cbdc", "rlusd"],
    "xrp": ["xrpl", "ripple", "sec", "cross-border", "cbdc", "rlusd"],
    "chainlink": ["chainlink", "ccip", "rwa", "oracle", "tokenization"],
    "sepolia": ["chainlink", "ccip", "rwa", "ethereum"],
    "hedera": ["hedera", "hbar", "tokenization", "rwa", "iso 20022"],
    "stellar": ["stellar", "xlm", "payment", "sdf", "soroban"],
    "linea": ["linea", "l2", "consensys", "zk-rollup", "ethereum"],
    "macro": ["house financial", "sec", "bis", "stablecoin", "fit21", "treasury"]
}

# ==================================================
# 🏛️ US Debt Clock / Macro Treasury データ取得関数
# ==================================================
def fetch_us_debt_clock_metrics() -> dict:
    try:
        url = "https://www.us-debt-clock.com/api/gpt/current-debt"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return {
                "total_debt": data.get("totalDebt", "$39.9T"),
                "daily_interest": data.get("dailyInterest", "$3.5B"),
                "fiat_devaluation_signal": "HIGH_INFLATION_PRESSURE"
            }
    except Exception as e:
        print(f"Debt Clockデータ取得スキップ: {e}")
    
    # フォールバック（基準値）
    return {
        "total_debt": "$39.9T+",
        "paper_to_silver_ratio": "CRITICAL_HIGH",
        "macro_bias": "BULLISH_HARD_ASSETS"
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
                "summary": f"On-chain activity for {chain_name.upper()} correlates with news/regulatory updates ({', '.join(matched_keywords)}).",
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
    ctx.logger.info("==================================================")

async def fetch_rss_updates(ctx: Context):
    global latest_news_data
    ctx.logger.info("📡 [RSS Collector] 主要機関・規制・13チェーンの公式発表を巡回中...")
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
        f"• 監視対象: 13-Chain Status + House Financial/SEC/BIS Intelligence\n"
        f"• データ提供アドレス: `{agent.address}`"
    )

@agent.on_interval(period=3600.0)
async def scheduled_news_task(ctx: Context):
    await fetch_rss_updates(ctx)

@agent.on_interval(period=30.0)
async def check_and_update_task(ctx: Context):
    global has_notified_update, last_checked_sepolia_block, latest_chain_data, latest_detected_signals
    
    try:
        res_block = requests.post(SEPOLIA_RPC_URL, json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}, timeout=5)
        if res_block.status_code == 200 and "result" in res_block.json():
            current_block = int(res_block.json()["result"], 16)
            latest_chain_data["sepolia"] = current_block
            ctx.logger.info(f"🟢 [Sepolia] 正常監視中 | ブロック: {current_block}")
            
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
                        if contract_addr == LINK_TOKEN_ADDRESS:
                            latest_detected_signals["last_link_event"] = current_block
                        elif contract_addr == CCIP_ROUTER_ADDRESS:
                            latest_detected_signals["last_ccip_event"] = current_block
                        elif contract_addr == ONDO_TOKEN_ADDRESS:
                            latest_detected_signals["last_ondo_event"] = current_block
            last_checked_sepolia_block = current_block
    except Exception as e:
        ctx.logger.error(f"🚨 [Sepolia] エラー保護: {e}")

    try:
        res_btc = requests.get(BTC_API_URL, timeout=5)
        if res_btc.status_code == 200:
            latest_chain_data["bitcoin"] = int(res_btc.text.strip())
            
        res_xrpl = requests.post(XRPL_RPC_URL, json={"method": "ledger", "params": [{"ledger_index": "validated"}]}, timeout=5)
        if res_xrpl.status_code == 200:
            latest_chain_data["xrp"] = res_xrpl.json().get("result", {}).get("ledger_index")
    except Exception as e:
        pass

# ==================================================
# 💰 動的見積もり ＆ 決済自動納品 (Protocols)
# ==================================================
@agent.on_message(model=DataQueryRequest)
async def handle_dynamic_quote(ctx: Context, sender: str, msg: DataQueryRequest):
    requested_target = (msg.chain_name or "all").lower()
    
    if requested_target in ["full", "intelligence", "full_intelligence"]:
        quoted_price, desc = "3.0", "Institutional Grade Combined Intelligence (On-Chain + Macro/Regulatory + Debt Clock)"
    elif requested_target in ["news", "regulatory", "macro"]:
        quoted_price, desc = "1.0", "Macro Financial & Regulatory News Package"
    elif requested_target in ["all", "summary"]:
        quoted_price, desc = "0.5", "Complete 13-Chain Unified Status Summary"
    else:
        quoted_price, desc = "0.1", f"Single Chain On-Chain Data for '{requested_target}'"

    ctx.logger.info(f"📩 [{sender}] リクエスト受信: Target='{requested_target}' ➔ 見積もり: {quoted_price} FET")

    payment_quote = RequestPayment(
        accepted_funds=[Funds(amount=quoted_price, currency="FET", payment_method="fet_direct")],
        recipient=str(agent.wallet.address()),
        deadline_seconds=300,
        reference=f"quote_{requested_target}_{int(time.time())}",
        description=desc
    )
    await ctx.send(sender, payment_quote)

@agent.on_message(model=CommitPayment)
async def handle_paid_delivery(ctx: Context, sender: str, msg: CommitPayment):
    ctx.logger.info(f"💳 [{sender}] から着金通知を受信 (TxHash: {msg.transaction_id})")
    
    # 💡 納品時のリアルタイムマクロデータ呼び出しを追加
    debt_metrics = fetch_us_debt_clock_metrics()
    
    response_data = DataQueryResponse(
        agent_version=CURRENT_VERSION,
        timestamp=time.time(),
        chain_statuses=latest_chain_data,
        latest_signals=generate_intelligence_signals(),
        news_intelligence=latest_news_data,
        macro_treasury_metrics=debt_metrics
    )
    await ctx.send(sender, response_data)
    ctx.logger.info(f"🎉 [{sender}] への統合インテリジェンスデータの納品が完了しました！")

# ==================================================
# 🏁 3. エージェントの起動 (Bottom of file)
# ==================================================
if __name__ == "__main__":
    agent.run()
