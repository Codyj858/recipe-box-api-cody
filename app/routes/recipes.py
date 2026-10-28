from flask import Blueprint, jsonify, request
from sqlite3 import IntegrityError
from app.services.recipe_service import (create_recipe_for_user, list_recipes as list_recipes_service, get_recipe_by_id, update_recipe_for_user, delete_recipe_for_user)
from app.services.rating_service import create_rating_for_recipe
from app.helpers import require_auth, recipe_to_dict
from app.extensions import cache


recipes_bp = Blueprint("recipes", __name__)

@recipes_bp.get("")
@cache.cached(timeout=30, key_prefix="recipes_list")
def list_recipes():
        rows = list_recipes_service()
        return jsonify(rows)

@recipes_bp.get("/<int:recipe_id>")
def get_recipe(recipe_id):
        recipe = get_recipe_by_id(recipe_id)
        if recipe is None:
             return jsonify({"error": "recipe not found"}), 404
        return jsonify(recipe), 200


@recipes_bp.post("")
def create_recipe():
    auth_result = require_auth()
    if not isinstance(auth_result, tuple):
        return auth_result
    if len(auth_result) == 2:
        return auth_result
    user_id, username, role = auth_result

    data = request.get_json(silent=True)
    if not data or not data.get("title") or not data.get("ingredients"):
        return jsonify({"error": "title and ingredients are required"}), 400

    try:
        recipe_dict = create_recipe_for_user(user_id, data)
    except IntegrityError:
        return jsonify({"error": "a recipe with that title already exists"}), 409

    return jsonify(recipe_dict), 201


@recipes_bp.patch("/<int:recipe_id>")
def update_recipe(recipe_id):
    print("DEBUG route reached, recipe_id:", recipe_id)
    auth_result = require_auth()
    if not isinstance(auth_result, tuple):
        return auth_result
    if len(auth_result) == 2:
        return auth_result
    user_id, username, role = auth_result

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "a JSON body is required"}), 400

    result = update_recipe_for_user(recipe_id, user_id, role, data)
    print("DEBUG result value and type:", result, type(result))  # note: recipe_id first, user_id second
    if result is None:
        return jsonify({"error": "recipe not found"}), 404
    if result == "forbidden":
        return jsonify({"error": "forbidden: not the owner"}), 403
    if result == "conflict":
        return jsonify({"error": "a recipe with that title already exists"}), 409
    return jsonify(result)


@recipes_bp.delete("/<int:recipe_id>")
def delete_recipe(recipe_id):
    auth_result = require_auth()
    if not isinstance(auth_result, tuple):
        return auth_result
    if len(auth_result) == 2:
        return auth_result
    user_id, username, role = auth_result

    result = delete_recipe_for_user(recipe_id, user_id)
    if result is None:
        return jsonify({"error": "recipe not found"}), 404
    if result == "forbidden":
        return jsonify({"error": "forbidden: not the owner"}), 403

    return "", 204

@recipes_bp.post("/<int:recipe_id>/ratings")
def create_rating(recipe_id):
    print("DEBUG: entering create_rating")
    auth_result = require_auth()
    if isinstance(auth_result, tuple) and len(auth_result) == 2:
        print("DEBUG auth_result:", auth_result, type(auth_result[0]))
        return auth_result
    user_id, username, role = auth_result
    data = request.get_json(silent=True) or {}
    body, status = create_rating_for_recipe(recipe_id, user_id, data)

    return jsonify(body), status


