from playwright.sync_api import sync_playwright
import os
import urllib.parse
import time
URL_endings = ["ALP","BTH","BOB","CCS","CUR","FSK","FRS","IHO","LUG","NCB","STK","SKN","SJP","SMT","SBD","SSK"]
URL = "https://www.olympics.com/en/milano-cortina-2026/results/general-reports?discipline={}"

def download_pdfs():
    os.makedirs("pdfs", exist_ok=True)

    with sync_playwright() as p:
        # 🔥 IMPORTANT: run NON-headless to avoid bot blocks
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
            ]
        )

        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        )

        page = context.new_page()

        for ending in URL_endings:
            url = URL.format(ending)
            print(f"\n==============================")
            print(f"Scraping discipline: {ending}")
            print(f"URL: {url}")

            # 🔁 Retry navigation (important for flaky HTTP/2 sites)
            for i in range(3):
                try:
                    page.goto(url, timeout=60000, wait_until="domcontentloaded")
                    break
                except Exception as e:
                    print(f"Navigation retry {i+1}/3 failed:", e)
                    time.sleep(2)
            else:
                print(f"❌ Failed to load {ending}, skipping...")
                continue

            # Wait a bit for JS content to populate
            page.wait_for_timeout(3000)

            # 🔍 Extract PDF links
            pdf_links = page.eval_on_selector_all(
                "a[href$='.pdf']",
                "els => els.map(e => e.href)"
            )

            print(f"Found {len(pdf_links)} PDFs")

            # 📥 Download each PDF safely
            for link in pdf_links:
                try:
                    filename = urllib.parse.urlparse(link).path.split("/")[-1]
                    print("Downloading:", filename)

                    response = context.request.get(link)

                    if response.ok:
                        with open(f"pdfs/{filename}", "wb") as f:
                            f.write(response.body())
                    else:
                        print(f"❌ Failed HTTP download: {link} ({response.status})")

                    time.sleep(1)  # small delay to reduce blocking

                except Exception as e:
                    print(f"❌ Failed to download {link}: {e}")

        browser.close()

if __name__ == "__main__":
    download_pdfs()