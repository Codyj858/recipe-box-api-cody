from flask import Blueprint, jsonify, request
import sqlite3
from app.services.recipe_service import (create_recipe_for_user, list_recipes as list_recipes_service, get_recipe_by_id, get_recipe_count )
from app.helpers import require_auth, recipe_to_dict


recipes_bp = Blueprint("recipes", __name__)

@recipes_bp.get("")
def list_recipes():
        rows = list_recipes_service()
        return jsonify(rows)

@recipes_bp.get("/recipes/<int:recipe_id>")
def get_recipe(recipe_id):
        recipe = get_recipe_by_id(recipe_id)
        if recipe is None:
             return jsonify({"error": "recipe not found"}), 404
        return jsonify(recipe), 200


@recipes_bp.post("")
def create_recipe():
        from app.db import get_db
        auth_result = require_auth()
        if isinstance(auth_result, tuple):
            user_id, username, role = auth_result
        else:
            return auth_result
        
        data = request.get_json(silent=True)
        if not data or not data.get("title") or not data.get("ingredients"):
            return jsonify({"error": "title and ingredients are required"}), 400

        try:
            recipe_dict = create_recipe_for_user(user_id, data)
        except sqlite3.IntegrityError:
            return jsonify({"error": "a recipe with that title already exists"}), 409

        return jsonify(recipe_dict), 201


@recipes_bp.patch("/recipes/<int:recipe_id>")
def update_recipe(recipe_id):
        from app.db import get_db
        auth_result = require_auth()
        if isinstance(auth_result, tuple):
            user_id, username, role = auth_result
        else:
            return auth_result

        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "a JSON body is required"}), 400
        fields, values = [], []
        for column in ("title", "ingredients", "instructions"):
            if column in data:
                fields.append(f"{column} = ?")
                values.append(data[column])
        if "is_public" in data:
            fields.append("is_public = ?")
            values.append(1 if data["is_public"] else 0)
        if not fields:
            return jsonify({"error": "nothing to update"}), 400

        db = get_db()

        # 1) load existing recipe
        existing = db.execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,),
        ).fetchone()
        if existing is None:
            return jsonify({"error": "recipe not found"}), 404

        # 2) ownership check
        if str(existing["owner_id"]) != str(user_id) and role != "admin":
            return jsonify({"error": "forbidden: not the owner"}), 403

        # 3) proceed with update
        values.append(recipe_id)
        try:
            cur = db.execute(
                f"UPDATE recipes SET {', '.join(fields)} WHERE id = ?",
                values,
            )
            db.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "a recipe with that title already exists"}), 409
        if cur.rowcount == 0:
            return jsonify({"error": "recipe not found"}), 404
        row = db.execute(
            "SELECT * FROM recipes WHERE id = ?", (recipe_id,)
        ).fetchone()
        return jsonify(recipe_to_dict(row))

@recipes_bp.delete("/recipes/<int:recipe_id>")
def delete_recipe(recipe_id):
        from app.db import get_db
        auth_result = require_auth()
        if isinstance(auth_result, tuple):
            user_id, username, role = auth_result
        else:
            return auth_result

        db = get_db()

        # load existing recipe
        existing = db.execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,),
        ).fetchone()
        if existing is None:
            return jsonify({"error": "recipe not found"}), 404

        # ownership check
        if str(existing["owner_id"]) != str(user_id) and role != "admin":
            return jsonify({"error": "forbidden: not the owner"}), 403

        # perform delete
        cur = db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        db.commit()
        return "", 204

@recipes_bp.get("/count")
def recipe_count():
     body, status = get_recipe_count()
     return jsonify(body), status