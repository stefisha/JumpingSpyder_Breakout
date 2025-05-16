# Jumpy_Bot Documentation

## Overview

**Jumpy_Bot** is a Node.js Telegram bot for crypto traders, focused on Solana. It provides real-time sentiment signals, lets users track tokens, and manages premium access using Solana wallet balances. The bot is built with [Telegraf](https://telegraf.js.org/) and integrates with Solana via deterministic wallet generation.

---

## Features

- **Start & Onboarding:**  
  `/start` welcomes users and presents main actions via inline buttons.

- **Get Signals:**  
  `/getsignals` or the "Get Signals" button subscribes users to live trading signals from curated sources.

- **Track Token:**  
  `/track_token` or the "Track Token" button lets users specify a token (e.g., `/track SOL`) to receive focused sentiment alerts.

- **Help & Feedback:**  
  `/help` and `/feedback` provide detailed instructions and a way to send suggestions or bug reports.

- **Settings:**  
  `/settings` (and button) previews upcoming customization features.

- **Solana Wallet Integration:**  
  `/subscribe` generates a unique Solana public key for each user (based on their Telegram user ID) and checks their SOL balance. Users must deposit SOL to unlock premium features.

---

## Key Files

- [`bot/bot.js`](jumping_spyder/bot/bot.js):  
  Main Telegram bot logic, commands, and responses.

- [`solana/paymentGate.js`](jumping_spyder/solana/paymentGate.js):  
  Handles deterministic Solana wallet generation and balance checks.

---

## Usage

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   - Copy `.env.example` to `.env` and fill in your secrets (Telegram bot token, Solana mnemonic, etc.).

3. **Run the bot:**
   ```bash
   node jumping_spyder/bot/bot.js
   ```

---

## Example: Solana Wallet Subscription

When a user sends `/subscribe`, the bot:
1. Derives a unique Solana public key from their Telegram user ID.
2. Checks the SOL balance for that key.
3. Replies with the public key and subscription status (based on balance).

---

## Extending

- Add new commands by extending the `responses` object and registering new `bot.command` or `bot.action` handlers in [`bot.js`](jumping_spyder/bot/bot.js).
- Wallet logic can be extended in [`paymentGate.js`](jumping_spyder/solana/paymentGate.js) for more advanced payment or on-chain features.

---

## Environment Variables

See `.env` for required configuration:
- `BOT_TOKEN` — Telegram bot token
- `MNEMONIC` — Solana wallet mnemonic
- `TELEGRAM_CHANNEL_ID` — Channel/user for alerts
- (and others for Twitter/OpenAI integration)

---

## License

MIT License © 2025 Stefan Veličković

---