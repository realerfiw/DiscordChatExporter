# Project Overview

This project is a Discord Bot designed to export the message history of a Discord channel into an HTML file and send it to a Telegram chat. It is particularly useful for Discord server administrators who want to back up or share the message history of specific channels.

# Prerequisites

1. Python 3.8 or higher installed on your system.

2. Required Python packages:<br/>
• discord.py<br/>
• requests

3. Access to:<br/>
   • A Discord Bot Token.<br/>
   • A Telegram Bot Token.<br/>
   • The Telegram Chat ID where the exported file will be sent.

# Installation and Setup

1. Clone the Project


   ```bash
   git clone https://github.com/realerfiw/DiscordChatExporter.git
   cd DiscordChatExporter
   ```
3. Install Dependencies

   ```bash
   pip install -r requirements.txt
   ```
4. Configure Environment Variables<br/>
Update the following variables in the code with your details:<br/>
  • `DISCORD_BOT_TOKEN`: The token for your Discord bot.<br/>
  • `DISCORD_ADMIN_ID`: Your Discord user ID (to restrict the bot's admin commands).<br/>
  • `DISCORD_NOTIFY_CHANNEL_ID`: The ID of the Discord channel where notifications will be sent.<br/>
  • `TELEGRAM_BOT_TOKEN`: The token for your Telegram bot.<br/>
  • `TELEGRAM_CHAT_ID`: The Telegram chat ID where the exported file will be uploaded.<br/>

  # How to run

  1. Start the bot by running:
     ```bash
     python main.py
     ```
  
