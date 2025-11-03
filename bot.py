from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN, ADMIN_ID

# Store user coins
user_coins = {}

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    if user_id not in user_coins:
        user_coins[user_id] = 0
    await update.message.reply_text(f"Hello @{user_name}! You have {user_coins[user_id]} coins.")

# Command: /coin
async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text("You have ∞ coins, Admin!")
    else:
        coins = user_coins.get(user_id, 0)
        await update.message.reply_text(f"You have {coins} coins.")

# Command: /addcoin (Admin only)
async def addcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("You are not allowed to use this command!")
        return

    try:
        target_user = int(context.args[0])
        amount = int(context.args[1])
        user_coins[target_user] = user_coins.get(target_user, 0) + amount
        await update.message.reply_text(f"Added {amount} coins to user {target_user}.")
    except:
        await update.message.reply_text("Usage: /addcoin <user_id> <amount>")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("coin", coin))
    app.add_handler(CommandHandler("addcoin", addcoin))

    print("ZYRO BOT is now running...")
    app.run_polling()

if __name__ == "__main__":
    main()
