from app import app, get_db

with app.app_context():
    db = get_db()
    db.execute("ALTER TABLE recipes ADD COLUMN owner_id INTEGER NOT NULL DEFAULT 0;")
    db.commit()
    print("Done")