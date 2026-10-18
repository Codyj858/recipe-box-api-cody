def insert_user(db, username, email, password_hash):
    db.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash),
    )
    db.commit()

def get_user_by_username(db, username):
    return db.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,),
    ).fetchone()

def count_recipes(db):
    row = db.execute("SELECT COUNT(*) AS c FROM recipes").fetchone()
    return row["c"]
    