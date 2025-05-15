import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

print(f"Bot token: {BOT_TOKEN}")

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "<b>Welcome to Jumpy_Bot 🕷️📊</b>\n\n"
        "You’re currently on the <b>Basic</b> tier.\n"
        "Want deeper insights with real-time sentiment analytics?\n"
        "✨ Upgrade to <b>Premium</b> for full access.\n\n"
        "🚀 Auto-trading with Jupiter & Solflare coming soon to Premium users."
    )


    keyboard = [
        [InlineKeyboardButton("📡 Get Signals", callback_data="get_signals"),
         InlineKeyboardButton("🕵️ Track Token", callback_data="track_token")],
        [InlineKeyboardButton("🙋 Help", callback_data="help"),
         InlineKeyboardButton("🧪 Feedback", callback_data="feedback"),
         InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode="HTML")

# Button callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    print("Button clicked:", query.data)  # Debug output
    await query.answer()

    if query.data == "help":
        await query.edit_message_text(
            text=(
                "🙋 <b>Jumpy_Bot Help</b>\n\n"
                "📡 <b>Get Signals</b> – Subscribe to trading signals based on real-time sentiment from curated crypto accounts on X (Twitter).\n\n"
                "🕵️ <b>Track Token</b> – Monitor a single token for sentiment spikes and key mentions.\n\n"
                "🧪 <b>Feedback</b> – Found a bug? Got a request? Drop it in.\n\n"
                "💸 <b>Is this free?</b> – During beta, yes. After that, Basic = $5/month. Premium = $15/month.\n\n"
                "🤖 <b>Where do signals come from?</b> – We monitor influencer chatter, meme waves, and market-moving tweets.\n\n"
                "📬 Questions? Email us at support@jumpingspyder.com"
            ),
            parse_mode="HTML"
        )

    elif query.data == "feedback":
        await query.edit_message_text(
            text=(
                "🧪 <b>Feedback</b>\n\n"
                "We’re building fast — and your input makes it better.\n\n"
                "Tell us what’s broken, what’s confusing, or what would make Jumpy_Bot better.\n\n"
                "Email: support@jumpingspyder.com"
            ),
            parse_mode="HTML"
        )

    elif query.data == "settings":
        await query.edit_message_text(
            text=(
                "⚙️ <b>Settings</b>\n\n"
                "Coming soon: customize alerts, manage watchlists, and control trading behavior.\n\n"
                "Until then, let us know what you'd love to see under Feedback."
            ),
            parse_mode="HTML"
        )

    else:
        await query.edit_message_text(
            text=f"🚧 Feature coming soon! ({query.data})",
            parse_mode="HTML"
        )

# Entry point
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
