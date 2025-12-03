# user_history.py
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_PATH = os.path.join(BASE_DIR, "data", "user_history.json")

def load_history():
    """Load history from JSON file"""
    if not os.path.exists(HISTORY_PATH):
        os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
        return {"users": {}}
    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except:
        return {"users": {}}

def save_history(data):
    """Save history to JSON file"""
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def get_user_history(user_id="user_001"):
    """Get user's history"""
    data = load_history()
    return data["users"].get(user_id, {
        "preferences": [],
        "previous_queries": []
    })

def update_user_history(user_message, nearest_store, user_id="user_001"):
    """Update user history"""
    data = load_history()
    
    if user_id not in data["users"]:
        data["users"][user_id] = {
            "preferences": [],
            "previous_queries": []
        }
    
    user = data["users"][user_id]
    
    # Detect preferences
    msg_lower = user_message.lower()
    
    if "coffee" in msg_lower or "mccafe" in msg_lower:
        if "likes coffee" not in user["preferences"]:
            user["preferences"].append("likes coffee")
    
    if "burger" in msg_lower or "big mac" in msg_lower:
        if "likes burgers" not in user["preferences"]:
            user["preferences"].append("likes burgers")
    
    if "breakfast" in msg_lower or "egg" in msg_lower or "mcmuffin" in msg_lower:
        if "likes breakfast" not in user["preferences"]:
            user["preferences"].append("likes breakfast")
    
    # Remove duplicates
    user["preferences"] = list(set(user["preferences"]))
    
    # Save query (keep last 5)
    user["previous_queries"].append(user_message)
    user["previous_queries"] = user["previous_queries"][-5:]
    
    save_history(data)