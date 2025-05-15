import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Load bot token
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
print("Loaded token:", BOT_TOKEN)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Click Me!", callback_data="clicked_button")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! 👋 Click the button below:",
        reply_markup=reply_markup
    )

# Button handler
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    print(">>> Button clicked:", query.data)

    if query.data == "clicked_button":
        await query.edit_message_text("You clicked the button! 🎉")
    else:
        await query.edit_message_text(f"Unknown button: {query.data}")

# Run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_button_click))  # <-- crucial line!
print("✅ Bot is running...")
app.run_polling()
