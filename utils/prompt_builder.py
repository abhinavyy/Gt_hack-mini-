# utils/prompt_builder.py
from datetime import datetime

def build_prompt(user_message, nearest_store, user_history, rag_context):
    """Build a prompt for the LLM"""
    
    # Check if greeting
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    is_greeting = any(greet in user_message.lower() for greet in greetings)
    
    # Store info
    store_text = ""
    if nearest_store:
        distance = nearest_store.get("distance", 0)
        if distance < 1000:
            distance_str = f"{distance}m"
        else:
            distance_str = f"{distance/1000:.1f}km"
        
        store_text = f"""
        Nearest McDonald's Store:
        • Store: {nearest_store.get('store_id', 'McDonald\'s')}
        • Distance: {distance_str} away
        • Address: {nearest_store.get('address', '')}
        • Features: {', '.join(nearest_store.get('features', []))}
        """
    
    # User preferences
    preferences = user_history.get('preferences', [])
    
    # Time of day
    current_hour = datetime.now().hour
    if current_hour < 12:
        time_of_day = "morning"
    elif current_hour < 17:
        time_of_day = "afternoon"
    else:
        time_of_day = "evening"
    
    if is_greeting:
        prompt = f"""
        User: "{user_message}"
        
        This is a greeting. Respond warmly and briefly.
        If we know their location, mention the nearest store casually.
        
        {store_text}
        
        Respond naturally as a friendly McDonald's assistant.
        """
    else:
        prompt = f"""
        User asked: "{user_message}"
        
        Context:
        • Time: {time_of_day}
        • User preferences: {', '.join(preferences) if preferences else 'None yet'}
        
        {store_text}
        
        Additional store info: {rag_context[0] if rag_context else ''}
        
        Guidelines:
        1. Answer directly and helpfully
        2. Be concise (2-3 sentences usually)
        3. Mention distance if relevant
        4. Suggest specific items if asking about food/drink
        5. Sound natural and friendly
        
        Response:
        """
    
    return prompt