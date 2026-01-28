import os
import time
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DESCONTO_MIN = float(os.getenv("DESCONTO_MINIMO", 20))
LIQ_MIN = int(os.getenv("LIQUIDEZ_MINIMA", 60))

print("BOT INICIADO")

def enviar_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }
    )

def buscar_dashskins():
    skins = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://dashskins.com.br", timeout=60000)
        page.wait_for_timeout(8000)  # espera JS carregar

        cards = page.query_selector_all("div[class*=item]")

        for card in cards[:30]:
            try:
                nome = card.inner_text().split("\n")[0]
                preco = card.inner_text().split("R$")[1].split("\n")[0]
                preco = float(preco.replace(",", "."))
                liquidez = 80  # placeholder (ajustamos depois)

                skins.append({
                    "nome": nome,
                    "preco": preco,
                    "liquidez": liquidez
                })
            except:
                continue

        browser.close()

    return skins

while True:
    skins = buscar_dashskins()

    for skin in skins:
        buff_brl = skin["preco"] * 1.3
        desconto = ((buff_brl - skin["preco"]) / buff_brl) * 100

        if desconto >= DESCONTO_MIN and skin["liquidez"] >= LIQ_MIN:
            msg = f"""
🚨 *OPORTUNIDADE*

🎮 *Skin:* {skin['nome']}
💰 Dash: R$ {skin['preco']:.2f}
📉 Desconto: {desconto:.1f}%
"""
            enviar_telegram(msg)

    time.sleep(300)
