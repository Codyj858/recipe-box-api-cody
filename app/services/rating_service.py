from app.extensions import db, cache
from app.models import Rating, Recipe
from sqlalchemy import func

def create_rating_for_recipe(recipe_id, user_id, data):
    score = data.get("score")
    if not isinstance(score, int) or score < 1 or score > 5:
        return {"error": "score must be 1-5"}, 400

    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return {"error": "recipe not found"}, 404

    rating = Rating(
        score=score,
        user_id=user_id,
        recipe_id=recipe_id,
    )
    db.session.add(rating)
    db.session.commit()
    cache.delete(f"recipe:{recipe_id}:avg_rating")


    return {
        "id": rating.id,
        "score": rating.score,
        "user_id": rating.user_id,
        "recipe_id": rating.recipe_id,
    }, 201

def get_average_rating(recipe_id):
    cache_key = f"recipe:{recipe_id}:avg_rating"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    avg = (
        db.session.query(func.avg(Rating.score))
        .filter(Rating.recipe_id == recipe_id)
        .scalar()
    )
    avg = float(avg) if avg is not None else None
    cache.set(cache_key, avg, timeout=30)
    return avg