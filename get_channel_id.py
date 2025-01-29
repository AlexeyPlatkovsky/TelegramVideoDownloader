from telethon import TelegramClient
from configparser import ConfigParser

# Read configuration from `config.ini`
config = ConfigParser()
config.read("config.ini")

# Credentials
api_id = int(config["telegram"]["api_id"])
api_hash = config["telegram"]["api_hash"]

# Initialize the Telegram client (as a user, not a bot)
client = TelegramClient("user_session", api_id, api_hash)

async def main():
    # Start the client (you will be prompted for authentication)
    await client.start()

    # List dialogs to find the channel
    async for dialog in client.iter_dialogs():
        print(f"Name: {dialog.name}, ID: {dialog.id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
