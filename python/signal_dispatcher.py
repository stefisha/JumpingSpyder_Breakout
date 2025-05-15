from telegram import Update
from telegram.ext import ContextTypes
import json

# Fake GPT result for demo
GPT_FAKE_RESULT = {
    "tweet": "Dogecoin is going to the moon!",
    "scam": False,
    "signal": "BUY",
    "reason": "Strong positive sentiment and bullish language."
}

paid_users = set()  # should be shared via storage in real use

async def handle_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in paid_users:
        await update.message.reply_text("🔒 Access denied. Use /deposit to unlock signals.")
        return

    signal_data = GPT_FAKE_RESULT  # simulate GPT output
    msg = f"""📈 New Trading Signal Detected 📈

From: @someaccount
Signal: {'🟢 BUY' if signal_data['signal'] == 'BUY' else '🔴 SELL'}
Tweet: "{signal_data['tweet']}"
Reason: {signal_data['reason']}
"""
    await update.message.reply_text(msg)
