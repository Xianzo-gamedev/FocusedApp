import telegram
from config import TELEGRAM_API_KEY
import asyncio

class TelegramBot:
    def __init__(self):
        self.bot = None
        self.chat_id = None
        self.enabled = False
        
        # Only initialize if we have a valid API key
        if TELEGRAM_API_KEY and TELEGRAM_API_KEY != 'your-telegram-api-key':
            try:
                self.bot = telegram.Bot(token=TELEGRAM_API_KEY)
                self.enabled = True
            except Exception as e:
                print(f"Warning: Could not initialize Telegram bot: {e}")
                self.enabled = False
        else:
            print("Warning: Telegram API key not configured. Telegram notifications disabled.")

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    async def send_message(self, message):
        """Send a message via Telegram bot"""
        if not self.enabled or not self.bot or not self.chat_id:
            print(f"Telegram notification (disabled): {message}")
            return
            
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as e:
            print(f"Error sending message: {e}")

    async def send_focus_mode_started(self):
        """Send notification when focus mode starts"""
        message = "🔴 Distraction detected. Focus Mode started."
        await self.send_message(message)

    async def send_focus_mode_ended(self):
        """Send notification when focus mode ends"""
        message = "✅ Focus session completed. Meet you next time!"
        await self.send_message(message)

    async def send_manual_focus_started(self):
        """Send notification when manual focus mode starts"""
        message = "🎯 Manual Focus Mode started. Stay strong!"
        await self.send_message(message)

# Initialize bot instance
telegram_bot = TelegramBot()
