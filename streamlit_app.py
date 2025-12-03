# streamlit_app.py
import streamlit as st
import json
import os
import sys
import random

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
try:
    from rag_pipeline import retrieve_context, ask_groq
    from user_history import get_user_history, update_user_history
    from utils.geo import find_nearest_store, geocode_location
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STORE_PATH = os.path.join(BASE_DIR, "data", "stores.json")
    
    with open(STORE_PATH, "r") as f:
        store_data = json.load(f)["stores"]
    
    MODULES_LOADED = True
except Exception as e:
    st.error(f"Error loading modules: {e}")
    MODULES_LOADED = False

# Page Configuration
st.set_page_config(
    page_title="McDonald's Assistant",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fixed CSS with proper contrast
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Sidebar styling - DARK TEXT */
    .sidebar .sidebar-content {
        background-color: white;
        color: #333333 !important;
    }
    
    /* All text in sidebar should be dark */
    .sidebar .sidebar-content * {
        color: #333333 !important;
    }
    
    /* Sidebar headers */
    .sidebar .sidebar-content h1,
    .sidebar .sidebar-content h2,
    .sidebar .sidebar-content h3,
    .sidebar .sidebar-content h4,
    .sidebar .sidebar-content h5,
    .sidebar .sidebar-content h6 {
        color: #333333 !important;
    }
    
    /* Sidebar paragraphs and text */
    .sidebar .sidebar-content p,
    .sidebar .sidebar-content div,
    .sidebar .sidebar-content span {
        color: #333333 !important;
    }
    
    /* Chat messages */
    .user-message {
        background: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 80%;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        color: #333333 !important;
    }
    
    .assistant-message {
        background: white;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 8px 0;
        max-width: 80%;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border-left: 4px solid #DA291C;
        color: #333333 !important;
    }
    
    /* Message headers - DARK TEXT */
    .message-header {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        font-weight: 600;
        color: #333333 !important;
    }
    
    .user-header {
        color: #0066cc !important;
    }
    
    .assistant-header {
        color: #DA291C !important;
    }
    
    /* Message content - DARK TEXT */
    .user-message div,
    .assistant-message div {
        color: #333333 !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 12px 20px;
        border: 2px solid #e0e0e0;
        background: white;
        color: #333333 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999999 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #DA291C;
        box-shadow: 0 0 0 2px rgba(218, 41, 28, 0.1);
        color: #333333 !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background: white;
        color: #333333 !important;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        border-color: #DA291C;
        background: #fff5f5;
        color: #333333 !important;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color: #333333 !important;
    }
    
    /* Info card text */
    .info-card strong,
    .info-card small,
    .info-card div {
        color: #333333 !important;
    }
    
    /* Radio buttons text */
    .stRadio > label {
        color: #333333 !important;
    }
    
    /* All labels and text */
    label, p, div, span {
        color: #333333 !important;
    }
    
    /* Chat input placeholder */
    .stChatInput > div > div > input::placeholder {
        color: #666666 !important;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        font-size: 0.75rem;
        font-weight: 500;
        border-radius: 12px;
        margin: 2px;
        background: #f0f0f0;
        color: #333333 !important;
    }
    
    /* Typing indicator */
    .typing {
        display: flex;
        align-items: center;
        padding: 10px 15px;
        color: #666666 !important;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        margin: 0 3px;
        background: #999999;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-5px); }
    }
    
    /* Force all text to be dark */
    * {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{random.randint(1000, 9999)}"

if 'user_location' not in st.session_state:
    st.session_state.user_location = {"lat": 28.6139, "lon": 77.2090, "address": "New Delhi"}

if 'nearest_store' not in st.session_state:
    st.session_state.nearest_store = None

# ==================== SIDEBAR ====================
with st.sidebar:
    # Title with explicit color
    st.markdown('<h3 style="color: #333333 !important;">🍟 McDonald\'s Assistant</h3>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Location Settings
    st.markdown('<h4 style="color: #333333 !important;">📍 Your Location</h4>', unsafe_allow_html=True)
    
    # Method selection
    method = st.radio("Select method:", ["Auto", "Manual", "Address"], horizontal=True, label_visibility="collapsed")
    
    if method == "Auto":
        if st.button("📍 Detect My Location", use_container_width=True):
            # Simulate location detection
            demo_locations = [
                {"lat": 28.6139, "lon": 77.2090, "address": "New Delhi"},
                {"lat": 19.0760, "lon": 72.8777, "address": "Mumbai"},
                {"lat": 12.9716, "lon": 77.5946, "address": "Bangalore"},
                {"lat": 28.5355, "lon": 77.3910, "address": "Noida"}
            ]
            location = random.choice(demo_locations)
            st.session_state.user_location = location
            st.success(f"Location set to {location['address']}")
            st.rerun()
    
    elif method == "Manual":
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitude", value=28.6139, format="%.6f")
        with col2:
            lon = st.number_input("Longitude", value=77.2090, format="%.6f")
        
        if st.button("📍 Set Coordinates", use_container_width=True):
            st.session_state.user_location = {"lat": lat, "lon": lon, "address": f"Lat: {lat:.4f}, Lon: {lon:.4f}"}
            st.success("Location set!")
            st.rerun()
    
    else:  # Address
        address = st.text_input("Enter address:", placeholder="e.g., Connaught Place, Delhi")
        if address and st.button("📍 Find Location", use_container_width=True):
            with st.spinner("Finding location..."):
                try:
                    lat, lon = geocode_location(address)
                    st.session_state.user_location = {"lat": lat, "lon": lon, "address": address}
                    st.success("Location found!")
                    st.rerun()
                except:
                    st.error("Could not find location")
    
    # Display current location
    if st.session_state.user_location["lat"]:
        st.markdown(f"""
        <div class="info-card">
            <strong style="color: #333333 !important;">📍 Current Location</strong><br>
            <span style="color: #333333 !important;">{st.session_state.user_location['address']}</span><br>
            <small style="color: #666666 !important;">Lat: {st.session_state.user_location['lat']:.4f}, Lon: {st.session_state.user_location['lon']:.4f}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Find and display nearest store
    if MODULES_LOADED and st.session_state.user_location["lat"]:
        nearest, distance = find_nearest_store(
            st.session_state.user_location["lat"],
            st.session_state.user_location["lon"],
            store_data
        )
        
        if nearest:
            nearest["distance"] = distance
            st.session_state.nearest_store = nearest
            
            # Convert distance to readable format
            if distance < 1000:
                distance_text = f"{distance}m"
            else:
                distance_text = f"{distance/1000:.1f}km"
            
            st.markdown(f"""
            <div class="info-card">
                <strong style="color: #333333 !important;">🏪 Nearest Store</strong><br>
                <span style="color: #333333 !important;">{nearest.get('store_id', 'McDonald\'s')}</span><br>
                <small style="color: #666666 !important;">📏 {distance_text} away</small><br>
                <small style="color: #666666 !important;">📍 {nearest.get('city', '')}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Questions
    st.markdown('<h4 style="color: #333333 !important;">💡 Quick Questions</h4>', unsafe_allow_html=True)
    
    questions = [
        "Where's the nearest store?",
        "I'm hungry",
        "Need coffee",
        "Opening hours?",
        "Any deals?",
        "Drive-thru available?",
        "Family friendly?"
    ]
    
    for q in questions:
        if st.button(q, key=f"q_{q}", use_container_width=True):
            st.session_state.quick_question = q
            st.rerun()
    
    st.markdown("---")
    
    # Chat Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔄 New User", use_container_width=True):
            st.session_state.messages = []
            st.session_state.user_id = f"user_{random.randint(1000, 9999)}"
            st.rerun()

# ==================== MAIN CHAT AREA ====================
# Header
st.markdown('<h1 style="color: #333333 !important;">McDonald\'s Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #666666 !important;">Ask me anything about McDonald\'s near you</p>', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <div class="message-header user-header">👤 You</div>
            <div style="color: #333333 !important;">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <div class="message-header assistant-header">🍟 McDonald\'s Assistant</div>
            <div style="color: #333333 !important;">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Handle quick questions from sidebar
if 'quick_question' in st.session_state:
    prompt = st.session_state.quick_question
    del st.session_state.quick_question
    
    # Add to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Chat input
if MODULES_LOADED:
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Create typing indicator
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
            <div class="typing">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            """, unsafe_allow_html=True)
        
        try:
            # Get nearest store
            nearest, distance = find_nearest_store(
                st.session_state.user_location["lat"],
                st.session_state.user_location["lon"],
                store_data
            )
            
            if nearest:
                nearest["distance"] = distance
            
            # Get user history
            history = get_user_history(st.session_state.user_id)
            
            # Get context
            rag_context = retrieve_context(prompt)
            
            # Build prompt
            from utils.prompt_builder import build_prompt
            full_prompt = build_prompt(prompt, nearest, history, rag_context)
            
            # Get response
            reply = ask_groq(full_prompt)
            
            # Update history
            update_user_history(prompt, nearest, st.session_state.user_id)
            
            # Update typing indicator with actual response
            typing_placeholder.markdown(f"""
            <div class="assistant-message">
                <div class="message-header assistant-header">🍟 McDonald's Assistant</div>
                <div style="color: #333333 !important;">{reply}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add to messages
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
        except Exception as e:
            typing_placeholder.markdown(f"""
            <div class="assistant-message">
                <div class="message-header assistant-header">🍟 McDonald's Assistant</div>
                <div style="color: #333333 !important;">Sorry, I encountered an error. Please try again.</div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})
        
        st.rerun()

# Welcome message for empty chat
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 40px; color: #666666 !important;">
        <h3 style="color: #DA291C !important;">👋 Welcome to McDonald's Assistant!</h3>
        <p style="color: #666666 !important;">I'm here to help you find McDonald's locations and answer your questions.</p>
        <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 500px; border: 1px solid #e0e0e0;">
            <p style="color: #333333 !important;"><strong>📍 First, set your location in the sidebar</strong></p>
            <p style="font-size: 0.9rem; color: #666666 !important;">Then try asking:</p>
            <p style="font-size: 0.9rem; color: #666666 !important;">
                • "Where's the nearest McDonald's?"<br>
                • "I'm hungry, what do you recommend?"<br>
                • "Do you have McCafe coffee?"<br>
                • "What are your opening hours?"
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<p style="color: #666666 !important; font-size: 0.9rem;">🍟 McDonald\'s Assistant • Your location is used to provide personalized recommendations</p>', unsafe_allow_html=True)