🛍️ Real-Time GenAI Recommender

A **real-time, AI-powered recommendation system** that combines **hybrid recommendation techniques** with **GenAI explanations** to deliver personalized and explainable product suggestions.

---

# 🚀 Features

* ⚡ Real-time recommendations (no page reload)
* 🧠 Hybrid recommender:

  * Content-based (FAISS + embeddings)
  * Collaborative filtering
  * Context-aware ranking (time & season)
* 🤖 GenAI explanations using Gemini
* 👤 Multi-day user tracking (localStorage + SQLite)
* 🎨 Tone-based responses (casual, premium, budget)
* 🛒 Cart tracking & history analysis

---

# 🧱 Tech Stack

| Component     | Technology            | Purpose                      |
| ------------- | --------------------- | ---------------------------- |
| Backend       | FastAPI               | API handling & orchestration |
| Vector Search | FAISS                 | Similarity search            |
| Embeddings    | Sentence Transformers | Convert text → vectors       |
| LLM           | Gemini                | Generate explanations        |
| Database      | SQLite                | Store user events & cart     |
| Frontend      | HTML, CSS, JS         | UI & interaction             |

---

# 🧠 System Architecture

```text
Frontend (HTML/JS)
    ↓
FastAPI Backend
    ↓
Recommendation Engine
    ↓
FAISS + Embeddings
    ↓
Gemini (LLM)
    ↓
SQLite (Storage)
    ↓
Response → UI Update
```

---

# 🔄 Workflow

1. User opens the app → UI loads products
2. User interacts (view/search/cart)
3. Frontend sends API request (`/track` or `/search`)
4. Backend:

   * Stores user activity
   * Runs hybrid recommender
   * Applies context (time & season)
   * Generates explanation using Gemini
5. Response sent as JSON
6. UI updates instantly (no reload)

---

# 📁 Project Structure

```text
project/
│
├── app/
│   ├── model.py          # Embeddings + FAISS
│   ├── recommender.py   # Recommendation logic
│   ├── llm.py           # Gemini integration
│   ├── context.py       # Time & season logic
│   ├── storage.py       # SQLite operations
│   ├── schema.py        # Request validation
│   └── __init__.py
│
├── static/
│   └── index.html       # Frontend UI
│
├── main.py              # FastAPI app
└── requirements.txt
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the repo

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

## 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Add API Key

Create `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

## 5️⃣ Run the server

```bash
uvicorn main:app --reload
```

---

## 6️⃣ Open in browser

```text
http://localhost:8000
```

---

# 🔌 API Endpoints

| Method | Endpoint                 | Description                             |
| ------ | ------------------------ | --------------------------------------- |
| GET    | `/products`              | Get all products                        |
| POST   | `/track`                 | Track user action & get recommendations |
| POST   | `/search`                | Search + recommendations                |
| GET    | `/cart/{user_id}`        | Get cart items                          |
| GET    | `/history/{user_id}`     | User activity history                   |
| GET    | `/preferences/{user_id}` | User preferences                        |

---

# 🧠 Key Concepts

* **Embeddings**: Convert text → vectors for similarity
* **FAISS**: Fast nearest-neighbor search
* **Hybrid Recommender**: Combines multiple strategies
* **Context Awareness**: Time & season-based ranking
* **GenAI**: Explains recommendations in natural language

---

# 🎯 Example Output

```json
{
  "user_context": "Viewing Running Shoes • evening / monsoon",
  "recommendations": [
    {
      "name": "Rain Jacket",
      "explanation": "Perfect for rainy evening workouts."
    }
  ]
}
```

---

# 🔥 Highlights

* Real-time personalization
* Explainable AI (not black-box)
* Lightweight & scalable design
* Clean frontend-backend integration

---

# 🧑‍💻 Author

**Mohamed Noufal**
AI & Data Science Student

---

# 📌 Future Improvements

* Deploy on cloud (AWS / GCP)
* Replace SQLite with PostgreSQL
* Add authentication system
* Use streaming LLM responses
* Improve collaborative filtering with ML models

---

# ⭐ Conclusion

This project demonstrates how to build a **real-time, explainable, AI-powered recommendation system** by combining **machine learning, vector search, and generative AI**.

---

