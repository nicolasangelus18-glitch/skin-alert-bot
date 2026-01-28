import requests
import os
from dotenv import load_dotenv

load_dotenv('config.env')

def buscar_dashskins():
    url = "https://api.dashskins.com.br/v1/market/items"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("❌ Erro ao acessar DashSkins:", e)
        return []  # NÃO quebra o bot

    skins = []

    for item in data.get("items", []):
        try:
            skins.append({
                "nome": item["market_hash_name"],
                "dash_brl": float(item["price"]),
                "liquidez": int(item.get("liquidity", 0)),
                "link": f"https://dashskins.com.br/item/{item['slug']}"
            })
        except:
            continue  # ignora item quebrado

    return skins


TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
DESCONTO = float(os.getenv('DESCONTO_MINIMO'))
LIQ_MIN = int(os.getenv('LIQUIDEZ_MINIMA'))

USD_BRL = 5.0  # depois automatizamos

print("DEBUG CONFIG:")
print("DESCONTO_MINIMO =", DESCONTO)
print("LIQUIDEZ_MINIMA =", LIQ_MIN)
print("TOKEN OK =", bool(TOKEN))
print("CHAT_ID OK =", bool(CHAT_ID))

# 🔹 FUNÇÃO DA MENSAGEM (sempre no topo)
def montar_mensagem(skin, buff_brl, desconto_percentual):
    if desconto_percentual >= 30:
        emoji = "🔥"
    elif desconto_percentual >= 25:
        emoji = "🟠"
    else:
        emoji = "🟡"

    margem = buff_brl - skin["dash_brl"]

    return f"""
🚨 *OPORTUNIDADE DE ARBITRAGEM* {emoji}

🎮 *Skin:* {skin['nome']}
📊 *Liquidez:* {skin['liquidez']}

💰 *Buff163:* R$ {buff_brl:.2f}
🏷️ *DashSkins:* R$ {skin['dash_brl']:.2f}
📉 *Desconto:* {desconto_percentual:.1f}%
💵 *Margem:* R$ {margem:.2f}

📦 *Marketplace:* DashSkins

⏰ Atualizado agora
"""


# 🔹 SKINS DE TESTE
skins = buscar_dashskins()

if not skins:
    print("⚠️ Nenhuma skin retornada da DashSkins")

# 🔹 LOOP PRINCIPAL
for skin in skins:
    buff_brl = skin["dash_brl"] * 1.30  # simula Buff 30% mais caro
    desconto_percentual = ((buff_brl - skin["dash_brl"]) / buff_brl) * 100

    if desconto_percentual >= DESCONTO and skin["liquidez"] >= LIQ_MIN:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": montar_mensagem(skin, buff_brl, desconto_percentual),
                "parse_mode": "Markdown"
            }
        )
