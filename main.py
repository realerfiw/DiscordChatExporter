import discord
import csv
import requests
import os
from keepalive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ADMIN_ID = <YOUR_ADMIN_ID> # Replace <YOUR_ADMIN_ID> with your ID
NOTIFY_CHANNEL_ID = <YOUR_NOTIFY_CHANNEL_ID> # Replace <YOUR_NOTIFY_CHANNEL_ID> with your channel ID


@client.event
async def on_ready():
  print('Bot is ready')


@client.event
async def on_message(message):
  if message.content == '!export' and message.author.id == ADMIN_ID:
    await message.channel.send(
        "Which channel do you want to export? Please provide the channel ID.")

    def check(m):
      return m.author == message.author and m.channel == message.channel

    channel_id = await client.wait_for('message', check=check)
    channel = client.get_channel(int(channel_id.content))

    messages = []
    async for message in channel.history(limit=None):
      avatar_url = str(
          message.author.avatar.url) if message.author.avatar else ""
      messages.append([message.author.name, avatar_url, message.content])

    # Export messages to HTML file
    html_content = "<html>\n<head>\n<style>\n.message-box {\n  display: flex;\n  align-items: center;\n  margin-bottom: 10px;\n  border-bottom: 1px solid lightgray;\n}\n\n.message-avatar {\n  width: 64px;\n  height: 64px;\n}\n\n.message-body {\n  margin-left: 10px;\n}\n\n.message-meta {\n  display: flex;\n  align-items: center;\n}\n\n.message-author {\n  font-weight: bold;\n}\n\n.message-content {\n  margin-top: 5px;\n}</style>\n</head>\n<body>\n"

    for msg in reversed(messages):
      user = msg[0]
      avatar_url = msg[1]
      content = msg[2]

      html_content += f"<div class='message-box'>\n<img class='message-avatar' width='64' height='64' src='{avatar_url}'>\n<div class='message-body'>\n<div class='message-meta'>\n<span class='message-author'>{user}</span>\n</div>\n<div class='message-content'>\n<span>{content}</span>\n</div>\n</div>\n</div>\n"

    html_content += "</body>\n</html>"

    with open('chat_history.html', 'w', encoding='utf-8') as file:
      file.write(html_content)

    # Send HTML file to Telegram
    url = "https://api.telegram.org/<TELEGRAM_BOT_TOKEN>/sendDocument"  # Replace <TELEGRAM_BOT_TOKEN> with your actual token
    params = {
        'chat_id':
        <TELEGRAM_CHAT_ID>,  # Replace <TELEGRAM_CHAT_ID> with the destination chat ID
        'caption': f'Exported Discord Chat History from #{channel_id.content}',
    }
    files = {'document': open('chat_history.html', 'rb')}
    try:
      requests.post(url, params=params, files=files)
      # Notify user that export was successful
      notify_channel = client.get_channel(NOTIFY_CHANNEL_ID)
      await notify_channel.send(
          f"Messages exported from #{channel_id.content} and sent to Telegram")
    except Exception as e:
      print(e)


my_secret = 'YOUR_DISCORD_BOT_TOKEN'
keep_alive()
client.run(my_secret)
