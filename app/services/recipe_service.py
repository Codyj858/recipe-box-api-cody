import sqlite3
from app.db import get_db
from app.helpers import recipe_to_dict
from app.data.auth_data import count_recipes

def create_recipe_for_user(user_id, data):
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO recipes (title, ingredients, instructions, is_public, owner_id)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                data["title"],
                data["ingredients"],
                data.get("instructions", ""),
                1 if data.get("is_public", True) else 0,
                user_id,
            ),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise
    row = db.execute(
        "SELECT * FROM recipes WHERE id = ?", (cur.lastrowid,)
    ).fetchone()
    return recipe_to_dict(row)

def list_recipes():
    db = get_db()
    rows = db.execute("SELECT * FROM recipes ORDER BY id").fetchall()
    return [recipe_to_dict(r) for r in rows]

def get_recipe_by_id(recipe_id):
    db = get_db()
    row = db.execute(
        "SELECT * FROM recipes WHERE id = ?", (recipe_id,)
    ).fetchone()
    return recipe_to_dict(row) if row is not None else None

def get_recipe_count():
    db = get_db()
    count = count_recipes(db)
    return {"count": count}, 200