from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schema import ActivityRequest, SearchRequest
from app.model import products, search_by_text
from app.recommender import get_recommendations
from app.llm import get_gemini_explanation
from app.context import get_context
from app import storage

app = FastAPI(title="Real-Time GenAI Recommender")


@app.on_event("startup")
def startup():
    storage.init_db()


def _build_recs_payload(user_id: str, product_id: int, tone: str):
    current = products[product_id]
    recs, ctx = get_recommendations(
        product_id,
        storage.get_user_history(user_id),
        storage.get_all_users_history(),
    )
    prefs = storage.compute_user_preferences(user_id, products)

    output = []
    for rec in recs:
        output.append({
            "id": rec["id"],
            "name": rec["name"],
            "category": rec["category"],
            "price": rec["price"],
            "tag": rec["tag"],
            "explanation": get_gemini_explanation(current["name"], rec["name"], tone, ctx),
        })
    return {
        "user_context": f"Viewing {current['name']} • {ctx['time_of_day']} / {ctx['season']}",
        "preferences": prefs,
        "recommendations": output,
    }


@app.get("/products")
async def list_products():
    return {"products": products}


@app.post("/track")
async def track_and_recommend(data: ActivityRequest):
    storage.record_event(data.user_id, data.product_id, data.action)
    if data.action == "add_to_cart":
        storage.add_to_cart(data.user_id, data.product_id)
    return _build_recs_payload(data.user_id, data.product_id, data.tone or "casual")


@app.post("/search")
async def search(data: SearchRequest):
    matched = search_by_text(data.query, k=6)
    if not matched:
        return {"results": [], "recommendations": []}
    seed = matched[0]
    storage.record_event(data.user_id, seed["id"], action="search", query=data.query)
    payload = _build_recs_payload(data.user_id, seed["id"], data.tone or "casual")
    payload["results"] = matched
    payload["search_query"] = data.query
    return payload


@app.get("/cart/{user_id}")
async def get_cart(user_id: str):
    ids = storage.get_cart(user_id)
    return {"cart": [products[i] for i in ids]}


@app.get("/history/{user_id}")
async def history(user_id: str):
    """Full multi-day activity log."""
    events = storage.get_user_history_detailed(user_id)
    enriched = [
        {**e, "product_name": products[e["product_id"]]["name"]}
        for e in events
    ]
    return {"user_id": user_id, "events": enriched}


@app.get("/preferences/{user_id}")
async def preferences(user_id: str):
    return {
        "user_id": user_id,
        "preferences": storage.compute_user_preferences(user_id, products),
    }


# ---- Serve frontend ----
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")