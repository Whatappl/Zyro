import json
import random
from telegram import Update
from telegram.ext import ContextTypes

USER_FILE = "user.json"

def load_data():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def casino(query, context: ContextTypes.DEFAULT_TYPE, ADMIN_ID):
    username = query.from_user.username or str(query.from_user.id)
    data = load_data()
    if username not in data:
        data[username] = {"coins": 100, "gems": 0}
    
    # Admin has unlimited coins
    if query.from_user.id == ADMIN_ID:
        data[username]["coins"] = float('inf')
    
    bet = 10
    result = random.choice(["win", "lose"])
    if result == "win":
        data[username]["coins"] += bet
        await query.edit_message_text(f"🎉 You won {bet} coins! Total: {data[username]['coins']}")
    else:
        data[username]["coins"] -= bet
        await query.edit_message_text(f"😢 You lost {bet} coins! Total: {data[username]['coins']}")
    
    save_data(data)
