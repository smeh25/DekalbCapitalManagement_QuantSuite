from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_DIR = Path("chrome_profile")

def scrape_latest_tweet(username):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True
        )
        page = browser.new_page()
        page.goto(f"https://x.com/{username}")
        page.wait_for_selector("article", timeout=15000)

        tweet = page.query_selector("article")
        if tweet:
            tweet_text = tweet.inner_text()
            browser.close()
            return f"🟢 Latest tweet from @{username}:\n\n{tweet_text.strip()}"
        else:
            browser.close()
            return f"⚠️ No tweet found for @{username}."

def scrape_latest_tweet_url(username):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True
        )
        page = browser.new_page()
        page.goto(f"https://x.com/{username}")
        page.wait_for_selector("article", timeout=15000)

        tweet = page.query_selector("article")
        if tweet:
            # Get the <a> tag that links to the tweet
            link = tweet.query_selector("a[href*='/status/']")
            if link:
                href = link.get_attribute("href")
                browser.close()
                return f"https://x.com{href}"
        
        browser.close()
        return None  # Nothing found
    
def recent_urls(username, n):
    if n > 10:
        raise ValueError("You can only request up to 10 tweets at a time.")
    
    tweet_urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=True
        )
        page = browser.new_page()
        page.goto(f"https://x.com/{username}")
        page.wait_for_selector("article", timeout=15000)

        articles = page.query_selector_all("article")

        for article in articles:
            if len(tweet_urls) >= n:
                break

            link = article.query_selector("a[href*='/status/']")
            if link:
                href = link.get_attribute("href")
                if href:
                    full_url = f"https://x.com{href}"
                    if full_url not in tweet_urls:
                        tweet_urls.append(full_url)

        browser.close()
    return tweet_urls
