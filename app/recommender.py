import numpy as np
from collections import Counter
from app.model import encoder, index, product_texts, products
from app.context import get_context, SEASON_BOOST


def content_based(product_id: int, k: int = 5):
    query_vector = encoder.encode([product_texts[product_id]]).astype('float32')
    _, indices = index.search(query_vector, k=k)
    return [products[i] for i in indices[0] if i != product_id]


def collaborative(user_history: list, all_users_history: dict, k: int = 3):
    """Lightweight 'users-like-you' recommender based on overlap of viewed products."""
    if not user_history:
        return []
    my_set = set(user_history)
    candidate_counter = Counter()
    for uid, hist in all_users_history.items():
        if not set(hist) & my_set:
            continue
        for pid in hist:
            if pid not in my_set:
                candidate_counter[pid] += 1
    top = [pid for pid, _ in candidate_counter.most_common(k)]
    return [products[pid] for pid in top]


def apply_context_boost(recs: list):
    ctx = get_context()
    boost_names = set(SEASON_BOOST.get(ctx["season"], []))
    recs.sort(key=lambda p: 0 if p["name"] in boost_names else 1)
    return recs, ctx


def get_recommendations(product_id: int, user_history: list, all_users_history: dict):
    cb = content_based(product_id, k=5)
    cf = collaborative(user_history, all_users_history, k=3)

    # Merge & dedupe (content first, collaborative fills the gaps)
    seen, hybrid = set(), []
    for p in cb + cf:
        if p["id"] != product_id and p["id"] not in seen:
            hybrid.append(p)
            seen.add(p["id"])

    hybrid, ctx = apply_context_boost(hybrid)
    return hybrid[:4], ctx