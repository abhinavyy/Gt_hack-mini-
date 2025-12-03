# 🍟 McDonald's Hyper-Personalized Customer Support Chatbot

### RAG + Groq Llama 3.3 + Location Awareness + User Memory

This project is a hyper-personalized AI assistant designed for McDonald's customers.
It provides real-time, context-aware, and location-based responses using Retrieval-Augmented Generation (RAG), FAISS vector search, Groq Llama 3.3, and persistent user memory.

The chatbot understands where the user is, retrieves nearby McDonald's store information, and generates personalized responses through a Streamlit-based dashboard interface.

---

## 🌟 Features

### Location Awareness

The chatbot accepts user latitude and longitude, automatically finds the nearest McDonald's store, and responds with distance, store type, features, and context.

### RAG-Powered Knowledge Retrieval

All store information is stored in a structured JSON file.
A SentenceTransformer model converts store entries into embeddings, and FAISS provides instant similarity search for relevant store information.

### Groq Llama 3.3 Integration

Uses Groq’s ultra-fast inference API with the Llama-3.3-70B Versatile model to generate human-like responses based on retrieved context.

### User Memory

The chatbot stores user history, recent interactions, and preferences to provide more human-like and personalized answers.

### Streamlit-Based Interface

A clean, modern dashboard built in Streamlit allows users to interact with the chatbot in real time.
Useful for demonstrations and project evaluation.

---

## 📁 Project Structure

* A Streamlit UI for interacting with the chatbot
* A RAG pipeline handling embeddings, FAISS indexing, and Groq API calls
* A user memory system storing past interactions
* Utility modules for geolocation and prompt creation
* A JSON stores database with 100+ McDonald’s locations across India
* Environment configuration via `.env`

---

## 🛠️ Setup Instructions

1. Create a Python virtual environment
2. Install required libraries using the project's `requirements.txt`
3. Add a `.env` file containing your Groq API key
4. Run the Streamlit application
5. Enter a message and your location to start chatting

---

## ▶️ How to Run

Launch the Streamlit application using:

`streamlit run app.py`

This opens a real-time UI where users can chat with the personalized McDonald's AI assistant.

---

## 💡 How It Works (Architecture)

### RAG Engine

Each McDonald's store entry from the JSON file is converted into a descriptive text block.
These blocks are embedded using a SentenceTransformer model and indexed using FAISS.
Based on a user's query, relevant store information is retrieved and added to the prompt.

### Location Engine

The chatbot calculates the distance between the user's coordinates and all stores.
The closest store and its details are selected for personalization.

### User Memory

Stores past queries, preferences, and last visited store.
This allows responses to feel tailored and human.

### Prompt Builder

Combines four sources into a single optimized prompt:

* User query
* Nearest store information
* Retrieved RAG context
* User history

### Groq LLM

The optimized prompt is sent to Groq's Llama-3.3-70B model, producing fast and highly contextual responses.

Demonstrates personalization + location awareness + store context.
<img width="2112" height="1370" alt="Screenshot 2025-12-03 120007" src="https://github.com/user-attachments/assets/f7576dc7-0898-4efb-a079-0c4f99a5938b" />

---

## 🔮 Future Enhancements

* Add menu-level RAG entries
* Implement user authentication
* Add recommendatins based on user taste profiles

---
