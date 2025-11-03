import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from fun import casino
from admin import grant_coins

# Config
TOKEN = os.getenv("ZYRO_TOKEN") or "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 8256350355  # admin id with unlimited coins/gems

# Load/save helpers
def load_data():
    if not os.path.exists("user.json"):
        with open("user.json", "w") as f:
            json.dump({}, f)
    with open("user.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("user.json", "w") as f:
        json.dump(data, f, indent=4)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or str(update.effective_user.id)
    data = load_data()
    if username not in data:
        data[username] = {"coins": 100, "gems": 0}
        save_data(data)

    keyboard = [
        [InlineKeyboardButton("🎰 Casino", callback_data="casino")],
        [InlineKeyboardButton("🎮 Games Menu", callback_data="menu")]
    ]
    await update.message.reply_text("Welcome to ZYRO BOT — pick a game:", reply_markup=InlineKeyboardMarkup(keyboard))

# Button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "casino":
        await casino(query, context, ADMIN_ID)
    elif query.data == "menu":
        await query.message.reply_text("🎮 Menu:\n🎰 Casino", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🎰 Casino", callback_data="casino")]]
        ))

# Admin command: /gcoin <username> <amount>
async def gcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caller_id = update.effective_user.id
    if caller_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /gcoin <username> <amount>")
        return

    username, amount_str = context.args
    try:
        amount = int(amount_str)
    except ValueError:
        await update.message.reply_text("❌ Amount must be a number.")
        return

    success, message = grant_coins(username, amount, ADMIN_ID, caller_id)
    await update.message.reply_text(message)

# Run app
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("gcoin", gcoin))  # admin command
    print("🤖 ZYRO BOT is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
