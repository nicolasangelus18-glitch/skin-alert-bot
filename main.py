import requests
import os
from dotenv import load_dotenv

load_dotenv('config.env')

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
DESCONTO = float(os.getenv('DESCONTO_MINIMO'))
LIQ_MIN = int(os.getenv('LIQUIDEZ_MINIMA'))

USD_BRL = 5.0  # depois vamos automatizar

skins = [
    {
        "nome": "AK-47 | Redline (FT)",
        "buff_usd": 100,
        "liquidez": 80,
        "dash_brl": 380
    }
]

for skin in skins:
    buff_brl = skin["buff_usd"] * USD_BRL
    desconto_percentual = ((buff_brl - skin["dash_brl"]) / buff_brl) * 100

    if desconto_percentual >= DESCONTO and skin["liquidez"] >= LIQ_MIN:
        msg = (
            f"🚨 ARBITRAGEM DETECTADA\n\n"
            f"Skin: {skin['nome']}\n"
            f"Buff: R$ {buff_brl:.2f}\n"
            f"Dash: R$ {skin['dash_brl']:.2f}\n"
            f"Desconto: {desconto_percentual:.1f}%\n"
            f"Liquidez: {skin['liquidez']}"
        )

        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": msg}
        )
