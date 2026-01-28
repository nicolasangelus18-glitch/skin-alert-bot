from playwright.sync_api import sync_playwright
import time

print("🚀 Iniciando bot DashSkins (modo teste de scraping)...")

URL = "https://dashskins.com.br"

def buscar_dashskins():
    skins = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = browser.new_page()

        print("🌐 Abrindo DashSkins...")
        page.goto(URL, timeout=60000)

        # Cloudflare costuma mostrar "Just a moment..."
        print("⏳ Aguardando Cloudflare...")
        time.sleep(8)

        print("🔍 Aguardando cards de skins aparecerem...")
        page.wait_for_selector("div[class*=item]", timeout=60000)

        cards = page.query_selector_all("div[class*=item]")

        print(f"📦 {len(cards)} cards encontrados")

        for card in cards[:20]:
            try:
                texto = card.inner_text()

                linhas = texto.split("\n")

                nome = linhas[0]

                preco_linha = next(l for l in linhas if "R$" in l)
                preco = float(
                    preco_linha
                    .replace("R$", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )

                skins.append({
                    "nome": nome,
                    "preco": preco
                })

                print(f"✅ {nome} — R$ {preco:.2f}")

            except Exception as e:
                print("⚠️ Erro ao ler card:", e)
                continue

        browser.close()

    return skins


skins = buscar_dashskins()

print(f"\n🏁 Fim do teste. Total de skins capturadas: {len(skins)}")
