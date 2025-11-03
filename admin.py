import json

USER_FILE = "user.json"

def load_data():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def grant_coins(username, amount, ADMIN_ID, caller_id):
    data = load_data()
    if caller_id != ADMIN_ID:
        return False, "❌ Not authorized."
    
    if username not in data:
        data[username] = {"coins": 0, "gems": 0}
    
    data[username]["coins"] += amount
    save_data(data)
    return True, f"✅ {amount} coins added to {username}. Total: {data[username]['coins']}"
