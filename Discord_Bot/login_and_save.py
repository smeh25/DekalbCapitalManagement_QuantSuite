from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_DIR = Path("chrome_profile")

def login_and_save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False
        )
        page = browser.new_page()
        page.goto("https://x.com/login")

        print("🔐 Please log in to Twitter/X in the opened browser...")
        input("👉 Press Enter when you're done logging in...")

        print("✅ Login complete and session saved.")
        browser.close()
