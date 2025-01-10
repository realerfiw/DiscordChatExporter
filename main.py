import discord
import requests
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

DISCORD_BOT_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
DISCORD_ADMIN_ID = YOUR_DISCORD_ADMIN_ID
DISCORD_NOTIFY_CHANNEL_ID = YOUR_DISCORD_NOTIFY_CHANNEL_ID
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = YOUR_TELEGRAM_CHAT_ID

@client.event
async def on_ready():
    print(f'Bot is ready as {client.user}')

@client.event
async def on_message(message):
    if message.content == '!export' and message.author.id == DISCORD_ADMIN_ID:
        await message.channel.send(
            "Which channel do you want to export? Please provide the channel ID."
        )

        def check(m):
            return m.author == message.author and m.channel == message.channel

        channel_id_message = await client.wait_for('message', check=check)
        channel_id = int(channel_id_message.content)
        channel = client.get_channel(channel_id)

        if not channel:
            await message.channel.send("Invalid channel ID.")
            return

        messages = []
        async for msg in channel.history(limit=None):
            avatar_url = str(msg.author.avatar.url) if msg.author.avatar else ""
            messages.append([msg.author.name, avatar_url, msg.content])

        html_content = """<html>
<head>
<style>
.message-box { display: flex; align-items: center; margin-bottom: 10px; border-bottom: 1px solid lightgray; }
.message-avatar { width: 64px; height: 64px; }
.message-body { margin-left: 10px; }
.message-meta { display: flex; align-items: center; }
.message-author { font-weight: bold; }
.message-content { margin-top: 5px; }
</style>
</head>
<body>
"""

        for user, avatar_url, content in reversed(messages):
            html_content += f"""
<div class='message-box'>
    <img class='message-avatar' width='64' height='64' src='{avatar_url}'>
    <div class='message-body'>
        <div class='message-meta'>
            <span class='message-author'>{user}</span>
        </div>
        <div class='message-content'>
            <span>{content}</span>
        </div>
    </div>
</div>
"""

        html_content += "</body></html>"

        file_path = 'chat_history.html'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        files = {'document': open(file_path, 'rb')}
        params = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': f'Exported Discord Chat History from #{channel.name}',
        }
        try:
            response = requests.post(url, files=files, data=params)
            response.raise_for_status()

            notify_channel = client.get_channel(DISCORD_NOTIFY_CHANNEL_ID)
            await notify_channel.send(
                f"Messages exported from #{channel.name} and sent to Telegram."
            )
        except requests.exceptions.RequestException as e:
            await message.channel.send(f"Failed to send file to Telegram: {e}")
        finally:
            os.remove(file_path)

client.run(DISCORD_BOT_TOKEN)
