import pandas as pd
import os
import ast
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from util.logger import logger
from config import config


def recipe_recommendation(available_ingredients):
    dataset_path = config.DATASET_PATH
    logger.info(f"Loading dataset: {dataset_path}")
    df = pd.read_csv(dataset_path)
    logger.info(f"Top 5 rows: \n{df.head(5)}")

    # Join all ingredient list.
    df["ingredients"] = df["ingredients_list"].apply(lambda x: " ".join(ast.literal_eval(x)))

    # save trained model
    model_path = config.MODEL_PATH
    is_model_exist = os.path.exists(model_path)
    logger.info(f"Trained model found: {is_model_exist}")
    if is_model_exist:
        # open trained model
        logger.info(f"loading trained model.")
        with open(model_path, "rb") as f:
            model_tfidfv = pickle.load(f)
    else:
        # Train model
        logger.info(f"training model...")
        model_tfidfv = TfidfVectorizer()
        model_tfidfv.fit(df['ingredients'])

        with open(model_path, "wb") as f:
            pickle.dump(model_tfidfv, f)
        logger.info(f"save trained model.")

    recipe_v = model_tfidfv.transform(df['ingredients'])

    # Transform available ingredients into vector form
    ingredients_transform = model_tfidfv.transform([available_ingredients])

    # Check cosine similarity with all recipe data
    scores = list(map(lambda x: cosine_similarity(ingredients_transform, x), recipe_v))

    # Sort top 5 match recipe.  
    def rec_recipe(df, scores):
        top_five = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]
        rec_recipe = pd.DataFrame(columns = ['recipe', 'ingredient_measurements', 'score', 'url', 'ingredients'])
        count = 0
        for i in top_five:
            rec_recipe.at[count, 'recipe'] = df['recipe_name'][i]
            
            rec_recipe.at[count, 'ingredient_measurements'] = df['ingredients_measurements'][i]
            
            rec_recipe.at[count, 'url'] = df['recipe_urls'][i]
            rec_recipe.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
            rec_recipe.at[count, 'ingredients'] = df['ingredients'][i]
            
            count += 1
        return rec_recipe

    top_five_recipe_df = rec_recipe(df, scores)
    logger.info(f"Predicted top five recipes: \n{top_five_recipe_df}")

    # Check ingredient are available in predicted recipe ingredient.
    tf_list = top_five_recipe_df['ingredients'].to_list()

    ingre_set = set(available_ingredients.split(" "))
    rec_index = 0
    for i, ingre in enumerate(tf_list):
        rec_set = set(ingre.split(" "))
        comman_ingre = ingre_set.intersection(rec_set)
        if len(comman_ingre) >= len(ingre_set)-1:
            rec_index = i
            break

    match_recipe = top_five_recipe_df.iloc[rec_index].fillna('').to_dict()
    logger.info(f"Predicted recipe: {match_recipe}.")
    return match_recipe
