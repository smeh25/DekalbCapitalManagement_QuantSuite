import discord
import asyncio
from login_and_save import login_and_save_session
import scrape
import re

def extract_status_id(url):
    match = re.search(r"/status/(\d+)", url)
    return match.group(1) if match else None

def read_history(token, channel_id):
    class HistoryBot(discord.Client):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.status_ids = []

        async def on_ready(self):
            channel = self.get_channel(channel_id)
            if not channel:
                print("Channel not found.")
                await self.close()
                return

            async for message in channel.history(limit=50):
                status_id = extract_status_id(message.content.strip())
                if status_id:
                    self.status_ids.append(status_id)
                if len(self.status_ids) >= 10:
                    break

            await self.close()

    intents = discord.Intents.default()
    intents.message_content = True
    client = HistoryBot(intents=intents)
    asyncio.run(client.start(token))
    return client.status_ids
