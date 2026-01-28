from playwright.sync_api import sync_playwright

print("🚀 Iniciando teste do Playwright...")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🌐 Abrindo DashSkins...")
        page.goto("https://dashskins.com.br", timeout=60000)

        title = page.title()
        print("✅ Site carregou com sucesso!")
        print("📄 Título da página:", title)

        browser.close()

except Exception as e:
    print("❌ Erro ao testar Playwright:")
    print(e)

print("🏁 Fim do teste")
