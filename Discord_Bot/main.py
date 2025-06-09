import discord
import asyncio
import scrape
import re
import time

# Custom imports
from login_and_save import login_and_save_session
from bot_class import send_messages_to_discord
from chat_history import read_history, extract_status_id
from variables import TOKEN, CHANNEL_ID, TWITTER_USERNAMES, RUN_INTERVAL_SECONDS, TWEETS_PER_USER


def main(num_tweets):
    from pathlib import Path

    if not Path("chrome_profile").exists():
        print("🔑 No session found. Logging in...")
        login_and_save_session()
    else:
        print("✅ Existing session found.")


    history_ids = read_history(TOKEN, CHANNEL_ID)

    newTweets = []
    for username in TWITTER_USERNAMES:
            
        recentTweets = scrape.recent_urls(username, num_tweets)

        for url in recentTweets:
            url_id = extract_status_id(url)
            if url_id not in history_ids:
                newTweets.append(url)

    if newTweets:
        send_messages_to_discord(newTweets)
    else:
        print("No new tweets at this time")
        


if __name__ == "__main__":
    # Running first iteration with high number of tweets to account for backlog
    main(5)

    while True:
        print("\n🔁 Running tweet scrape + Discord update cycle...")
        try:
            main(TWEETS_PER_USER)
        except Exception as e:
            print(f"❌ Error during main execution: {e}")
        print(f"⏳ Waiting {RUN_INTERVAL_SECONDS} seconds...\n")
        time.sleep(RUN_INTERVAL_SECONDS)


