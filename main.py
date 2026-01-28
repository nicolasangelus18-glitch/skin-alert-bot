from playwright.sync_api import sync_playwright
import time

URL = "https://dashskins.com.br"

print("🚀 Teste Cloudflare + DashSkins (Railway)")

def run_once():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
            ],
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="pt-BR",
            timezone_id="America/Sao_Paulo",
            viewport={"width": 1366, "height": 768},
        )

        page = context.new_page()

        # Remove webdriver flag (ajuda em alguns sites)
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)

        print("🌐 Abrindo site...")
        page.goto(URL, timeout=60000, wait_until="domcontentloaded")

        # Espera Cloudflare “soltar” (até 90s)
        print("⏳ Esperando challenge do Cloudflare (até 90s)...")
        t0 = time.time()
        while time.time() - t0 < 90:
            title = page.title()
            if "Just a moment" not in title and "Attention Required" not in title:
                break
            time.sleep(2)

        title = page.title()
        print("📄 Título agora:", title)
        print("🔗 URL agora:", page.url)

        # Tenta achar cards (pode variar)
        selectors = [
            "div[class*=item]",
            "[class*=item]",
            "[data-testid*=item]",
            "a[href*='item']",
        ]

        found = False
        for sel in selectors:
            try:
                page.wait_for_selector(sel, timeout=15000)
                elements = page.query_selector_all(sel)
                print(f"✅ Seletor OK: {sel} | elementos: {len(elements)}")
                found = True
                break
            except:
                print(f"⚠️ Não achei: {sel}")

        if not found:
            # Debug: mostra um pedaço do HTML pra confirmar que ficou no challenge
            html = page.content()
            print("🧾 HTML (primeiros 800 chars):")
            print(html[:800])

        browser.close()

# Roda 2 tentativas
for i in range(2):
    print(f"\n===== TENTATIVA {i+1}/2 =====")
    run_once()
