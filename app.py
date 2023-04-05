from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.api.core.recipe_recommendation import recipe_recommendation
from util.logger import logger

app = FastAPI()


@app.get("/get_recipe")
def get_recipe(ingredients: str):
    logger.info(f"checking recipe for ingredients: {ingredients}")
    ingredients = " ".join(ingredients.split(","))
    recipe = recipe_recommendation(ingredients)
    return JSONResponse(content=recipe)


@app.get("/")
def read_root():
    return "Recipe recommendation system service is up."
