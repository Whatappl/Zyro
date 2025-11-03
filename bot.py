from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN, ADMIN_ID
import random
import json
import os

# File to store user coins
COINS_FILE = "coins.json"

# Load coins from file
if os.path.exists(COINS_FILE):
    with open(COINS_FILE, "r") as f:
        coins = json.load(f)
else:
    coins = {}

def save_coins():
    with open(COINS_FILE, "w") as f:
        json.dump(coins, f)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    if user_id not in coins:
        coins[user_id] = 0
        save_coins()
    await update.message.reply_text(f"Hello {user.first_name}! Welcome to the bot. You have {coins[user_id]} coins.")

# Admin-only command
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("You are the admin! Unlimited coins activated.")
    else:
        await update.message.reply_text("You are not the admin!")

# Coin flip game
async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    result = random.choice(["Heads", "Tails"])
    # Winner earns 10 coins
    coins[user_id] = coins.get(user_id, 0) + 10
    save_coins()
    await update.message.reply_text(f"🪙 You flipped: {result}\nYou earned 10 coins! Total coins: {coins[user_id]}")

# Roll number game
async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    number = random.randint(1, 100)
    coins[user_id] = coins.get(user_id, 0) + number
    save_coins()
    await update.message.reply_text(f"🎲 You rolled: {number}\nYou earned {number} coins! Total coins: {coins[user_id]}")

# Check balance
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    total = coins.get(user_id, 0)
    await update.message.reply_text(f"💰 You have {total} coins.")

# Shop command
async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    shop_items = {
        "Sword": 100,
        "Shield": 80,
        "Potion": 50
    }
    msg = "🏪 Shop Items:\n"
    for item, price in shop_items.items():
        msg += f"{item}: {price} coins\n"
    msg += "Buy an item with /buy <item_name>"
    await update.message.reply_text(msg)

# Buy command
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("Specify an item to buy. Example: /buy Sword")
        return
    item = context.args[0].capitalize()
    shop_items = {
        "Sword": 100,
        "Shield": 80,
        "Potion": 50
    }
    if item not in shop_items:
        await update.message.reply_text("Item not found in shop!")
        return
    if coins.get(user_id, 0) >= shop_items[item]:
        coins[user_id] -= shop_items[item]
        save_coins()
        await update.message.reply_text(f"You bought {item}! Remaining coins: {coins[user_id]}")
    else:
        await update.message.reply_text("You don't have enough coins!")

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start the bot\n"
        "/admin - Admin command\n"
        "/coin - Flip a coin and earn coins\n"
        "/roll - Roll a number and earn coins\n"
        "/balance - Check your coins\n"
        "/shop - View shop items\n"
        "/buy <item> - Buy an item from shop\n"
        "/help - Show this message"
    )

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("coin", coin))
    app.add_handler(CommandHandler("roll", roll))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()
