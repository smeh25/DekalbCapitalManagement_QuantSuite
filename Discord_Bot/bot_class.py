import discord

from variables import TOKEN, CHANNEL_ID


class TweetBot(discord.Client):
    def __init__(self, messages, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = messages

    async def on_ready(self):
        print(f"🤖 Logged in as {self.user}")
        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print("❌ Channel not found.")
            await self.close()
            return

        for msg in self.messages:
            await channel.send(msg)
            print(f"✅ Sent: {msg[:50]}{'...' if len(msg) > 50 else ''}")

        await self.close()

def send_messages_to_discord(messages):
    intents = discord.Intents.default()
    intents.message_content = True
    client = TweetBot(messages, intents=intents)
    client.run(TOKEN)