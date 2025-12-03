# rag_pipeline.py
import json
import os
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize clients
client = Groq(api_key=GROQ_API_KEY)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load store data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_PATH = os.path.join(BASE_DIR, "data", "stores.json")

with open(STORE_PATH, "r") as f:
    all_data = json.load(f)
    store_data = all_data["stores"]

# Build corpus for RAG
corpus = []
for store in store_data:
    text = f"""
    McDonald's {store['store_id']} in {store['city']}.
    Address: {store['address']}
    Type: {store['type']}
    Features: {', '.join(store['features'])}
    """
    corpus.append(text)

# Create FAISS index if we have data
if corpus:
    embeddings = embedder.encode(corpus)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
else:
    index = None

def retrieve_context(query, top_k=2):
    """Retrieve relevant store information"""
    if index is None or len(corpus) == 0:
        return ["McDonald's stores offer burgers, fries, drinks, and breakfast items."]
    
    query_vec = embedder.encode([query])
    distances, indices = index.search(query_vec, top_k)
    
    results = []
    for i in indices[0]:
        if i < len(corpus):
            results.append(corpus[i])
    
    return results if results else ["McDonald's restaurant information available."]

def ask_groq(prompt):
    """Get response from Groq LLM"""
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200
    )
    return completion.choices[0].message.content