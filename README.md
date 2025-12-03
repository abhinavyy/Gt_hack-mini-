# 🍟 McDonald's Hyper-Personalized Customer Support Chatbot

### **RAG + Groq Llama 3.3 + Location-Awareness + User Memory**

This project is a **hyper-personalized AI assistant** built for McDonald's store support.
It provides **real-time, personalized, location-based answers** using a combination of:

* **RAG (Retrieval-Augmented Generation)**
* **FAISS Vector Search**
* **SentenceTransformer Embeddings**
* **Groq Llama 3.3 (70B Versatile)**
* **User History & Preferences**
* **Geolocation Intelligence**

The chatbot understands the user’s location, finds the **nearest McDonald’s store**, retrieves store-specific details from a RAG pipeline, and personalizes responses based on previous interactions.

---

## 🚀 Features

### ⭐ **1. Location Awareness**

* Accepts user latitude & longitude
* Finds the **nearest McDonald's store** using geodesic distance
* Returns distance and store details

### ⭐ **2. RAG-Powered Store Lookup**

* Store database stored in `stores.json`
* Makes embeddings with SentenceTransformers
* Uses FAISS to retrieve the **most relevant stores or info**

### ⭐ **3. Groq Llama-3.3 Integration**

* Uses Groq API (extremely fast inference)
* Model used: **llama-3.3-70b-versatile**

### ⭐ **4. User Memory**

* Stores:

  * last queries
  * last visited store
  * preferences (e.g., hot food, late-night dining)
* Makes responses feel human & personalized

### ⭐ **5. Clean Architecture**

* Modular components
* Easy to modify, extend, and debug

---

