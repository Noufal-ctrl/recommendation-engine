import sqlite3
import os
from datetime import datetime
from collections import Counter

DB_PATH = os.path.join("data", "recommender.db")
os.makedirs("data", exist_ok=True)


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Run once at startup to create tables."""
    with _connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS user_events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     TEXT NOT NULL,
            product_id  INTEGER NOT NULL,
            action      TEXT NOT NULL,           -- view | add_to_cart | search | purchase
            query       TEXT,                    -- search keyword if action=search
            timestamp   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_cart (
            user_id     TEXT NOT NULL,
            product_id  INTEGER NOT NULL,
            added_at    TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_user_events_user ON user_events(user_id);
        CREATE INDEX IF NOT EXISTS idx_user_cart_user   ON user_cart(user_id);
        """)


# ---------- Event recording ----------
def record_event(user_id: str, product_id: int, action: str = "view", query: str = None):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO user_events (user_id, product_id, action, query, timestamp) VALUES (?, ?, ?, ?, ?)",
            (user_id, product_id, action, query, datetime.utcnow().isoformat()),
        )


# ---------- History reads ----------
def get_user_history(user_id: str, limit: int = 100):
    """Returns list of product_ids the user has interacted with (newest last)."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT product_id FROM user_events WHERE user_id = ? ORDER BY timestamp ASC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return [r["product_id"] for r in rows]


def get_user_history_detailed(user_id: str, limit: int = 50):
    """Full event log with timestamps — useful for the UI."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT product_id, action, query, timestamp FROM user_events "
            "WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def get_all_users_history():
    """For collaborative filtering: {user_id: [product_ids,...]}"""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT user_id, product_id FROM user_events ORDER BY timestamp ASC"
        ).fetchall()
    out = {}
    for r in rows:
        out.setdefault(r["user_id"], []).append(r["product_id"])
    return out


# ---------- Cart ----------
def add_to_cart(user_id: str, product_id: int):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO user_cart (user_id, product_id, added_at) VALUES (?, ?, ?)",
            (user_id, product_id, datetime.utcnow().isoformat()),
        )


def get_cart(user_id: str):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT product_id FROM user_cart WHERE user_id = ?",
            (user_id,),
        ).fetchall()
    return [r["product_id"] for r in rows]


# ---------- Preferences (computed from history) ----------
def compute_user_preferences(user_id: str, products: list):
    history = get_user_history(user_id)
    if not history:
        return {}
    viewed = [products[pid] for pid in history]
    cat_counts = Counter(p["category"] for p in viewed)
    prices = [p["price"] for p in viewed]
    avg_price = sum(prices) / len(prices)
    price_band = "budget" if avg_price < 1000 else "mid" if avg_price < 3000 else "premium"

    return {
        "top_categories": [c for c, _ in cat_counts.most_common(3)],
        "avg_price": round(avg_price, 2),
        "price_band": price_band,
        "total_interactions": len(history),
    }