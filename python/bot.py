import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from solders.pubkey import Pubkey
from solana.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from signal_dispatcher import handle_signal

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PRIVATE_KEY = json.loads(os.getenv("PRIVATE_KEY"))  # List of ints
BACKEND_KEYPAIR = Keypair.from_secret_key(bytes(PRIVATE_KEY))
SOLANA_ENDPOINT = "https://api.devnet.solana.com"

wallet_map = {}  # Use a dict for wallet bindings
paid_users = set()  # Track who deposited

async def linkwallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /linkwallet <wallet_address>")
        return
    try:
        pubkey = Pubkey.from_string(context.args[0])
        wallet_map[update.effective_user.id] = pubkey
        await update.message.reply_text(f"✅ Wallet linked: {pubkey}")
    except Exception:
        await update.message.reply_text("❌ Invalid wallet address.")

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deposit_address = BACKEND_KEYPAIR.public_key
    paid_users.add(update.effective_user.id)
    await update.message.reply_text(f"To deposit SOL, send to: {deposit_address}\nOnce we confirm it, you'll receive trading signals.")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in wallet_map:
        await update.message.reply_text("❌ Please link your wallet first using /linkwallet <address>")
        return
    async with AsyncClient(SOLANA_ENDPOINT) as client:
        balance = await client.get_balance(wallet_map[user_id])
        sol = balance['result']['value'] / 1_000_000_000
        await update.message.reply_text(f"💰 Balance: {sol:.4f} SOL")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in wallet_map:
        await update.message.reply_text("❌ Please link your wallet first.")
        return
    if len(context.args) != 1 or not context.args[0].replace('.', '', 1).isdigit():
        await update.message.reply_text("Usage: /withdraw <amount>")
        return
    amount_sol = float(context.args[0])
    lamports = int(amount_sol * 1_000_000_000)
    txn = Transaction().add(
        transfer(
            TransferParams(
                from_pubkey=BACKEND_KEYPAIR.public_key,
                to_pubkey=wallet_map[user_id],
                lamports=lamports
            )
        )
    )
    async with AsyncClient(SOLANA_ENDPOINT) as client:
        try:
            res = await client.send_transaction(txn, BACKEND_KEYPAIR)
            sig = res['result']
            await update.message.reply_text(f"✅ Sent {amount_sol} SOL\nExplorer: https://explorer.solana.com/tx/{sig}?cluster=devnet")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to JumpingSpyder! Use /linkwallet <wallet> and /deposit to start.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("linkwallet", linkwallet))
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("signal", handle_signal, block=False))
    print("🤖 Bot is running...")
    app.run_polling()
