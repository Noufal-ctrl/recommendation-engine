import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer('all-MiniLM-L6-v2')

products = [
    {"id": 0, "name": "Pro Hiking Boots", "category": "Footwear", "desc": "Waterproof, rugged grip", "price": 4999, "tag": "Premium"},
    {"id": 1, "name": "Ultra-light Tent", "category": "Camping", "desc": "2-person, wind resistant", "price": 7499, "tag": "Trending"},
    {"id": 2, "name": "Thermal Base Layer", "category": "Apparel", "desc": "Moisture-wicking, cold weather", "price": 1499, "tag": "Winter pick"},
    {"id": 3, "name": "Portable Stove", "category": "Camping", "desc": "Compact, fast boiling", "price": 2299, "tag": "Budget pick"},
    {"id": 4, "name": "Energy Gel Pack", "category": "Nutrition", "desc": "Quick carb boost for runners", "price": 299, "tag": "Budget pick"},
    {"id": 5, "name": "Trail Running Shoes", "category": "Footwear", "desc": "Lightweight, breathable, strong grip", "price": 3499, "tag": "Trending"},
    {"id": 6, "name": "Camping Backpack", "category": "Camping", "desc": "50L capacity, ergonomic support", "price": 3899, "tag": "Bestseller"},
    {"id": 7, "name": "Insulated Water Bottle", "category": "Accessories", "desc": "Keeps drinks hot or cold for hours", "price": 899, "tag": "Budget pick"},
    {"id": 8, "name": "Rain Jacket", "category": "Apparel", "desc": "Waterproof, windproof, lightweight", "price": 2599, "tag": "Monsoon pick"},
    {"id": 9, "name": "Sleeping Bag", "category": "Camping", "desc": "Suitable for extreme cold conditions", "price": 3299, "tag": "Winter pick"},
    {"id": 10, "name": "Fitness Tracker Watch", "category": "Electronics", "desc": "Tracks heart rate and steps", "price": 4499, "tag": "Trending"},
    {"id": 11, "name": "Protein Bar Pack", "category": "Nutrition", "desc": "High protein snack for energy", "price": 599, "tag": "Budget pick"},
    {"id": 12, "name": "Headlamp Torch", "category": "Accessories", "desc": "Hands-free lighting for night trekking", "price": 799, "tag": "Budget pick"},
    {"id": 13, "name": "Hiking Socks", "category": "Apparel", "desc": "Comfortable, sweat-absorbing", "price": 349, "tag": "Budget pick"},
    {"id": 14, "name": "Portable Power Bank", "category": "Electronics", "desc": "Fast charging, high capacity", "price": 1599, "tag": "Bestseller"},
    {"id": 15, "name": "Camping Chair", "category": "Camping", "desc": "Foldable, lightweight, durable", "price": 1299, "tag": "Budget pick"},
    {"id": 16, "name": "Cycling Helmet", "category": "Accessories", "desc": "Safety certified, lightweight", "price": 1899, "tag": "Safety"},
    {"id": 17, "name": "Smart Water Bottle", "category": "Accessories", "desc": "Tracks hydration levels", "price": 1799, "tag": "Premium"},
    {"id": 18, "name": "Yoga Mat", "category": "Fitness", "desc": "Non-slip, comfortable cushioning", "price": 999, "tag": "Trending"},
    {"id": 19, "name": "Resistance Bands", "category": "Fitness", "desc": "Full body workout tool", "price": 699, "tag": "Budget pick"},
]

product_texts = [f"{p['name']} {p['category']} {p['desc']}" for p in products]
embeddings = encoder.encode(product_texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))


def search_by_text(query: str, k: int = 6):
    """Free-text search using embeddings (used by the search bar)."""
    q_vec = encoder.encode([query]).astype('float32')
    distances, indices = index.search(q_vec, k=k)
    return [products[i] for i in indices[0]]