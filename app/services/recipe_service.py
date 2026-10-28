from app.helpers import recipe_to_dict
from app.data.auth_data import count_recipes
from app.extensions import db, cache
from app.models import Recipe
from flask import request, current_app
import jwt
from sqlalchemy.exc import IntegrityError

def create_recipe_for_user(user_id, data):
    instructions = data.get("instructioins", "")
    is_public_value = 1 if data.get("is_public", True) else 0

    recipe = Recipe(
        title=data["title"],
        ingredients=data["ingredients"],
        instructions=instructions,
        is_public=is_public_value,
        owner_id=user_id,
    )

    db.session.add(recipe)
    db.session.commit()
    cache.delete("recipes_list")

    return {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "is_public": recipe.is_public,
        "owner_id": recipe.owner_id,
    }

def update_recipe_for_user(recipe_id, user_id, role, data):
    recipe = Recipe.query.filter_by(id=recipe_id).first()

    if recipe is None:
        print("DEBUG: recipe is None")
        return None
    print("DEBUG owner_id/user_id/role:", recipe.owner_id, user_id, role)
    print("DEBUG: passing ownership check")
    recipe_owner_username = recipe.owner.username
    

    user_id = int(user_id)

    if role != "admin" and recipe.owner_id != user_id:
        return "forbidden"

    recipe.title = data.get("title", recipe.title)
    recipe.ingredients = data.get("ingredients", recipe.ingredients)
    recipe.instructions = data.get("instructions", recipe.instructions)
    if "is_public" in data:
        recipe.is_public = 1 if data["is_public"] else 0

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "conflict"
    cache.delete("recipes_list")


    return {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "is_public": recipe.is_public,
        "owner_id": recipe.owner_id,
    }

def delete_recipe_for_user(recipe_id, user_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe is None:
        return None

    if str(recipe.owner_id) != str(user_id):
        return "forbidden"

    db.session.delete(recipe)
    db.session.commit()
    cache.delete("recipes_list")
    return True

def list_recipes():
    recipes = (
        db.session.query(Recipe)
        .order_by(Recipe.id)
        .all()
    )
    return [
        {
        "id": r.id,
        "title": r.title,
        "ingredients": r.ingredients,
        "instructions": r.instructions,
        "is_public": r.is_public,
        "owner_id": r.owner_id,
        }
        for r in recipes
    ]

def get_recipe_by_id(recipe_id: int):
    recipe = (
        db.session.query(Recipe)
        .filter(Recipe.id == recipe_id)
        .first()
    )
    if recipe is None:
        return None

    return {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "is_public": recipe.is_public,
        "owner_id": recipe.owner_id,
    }
    
