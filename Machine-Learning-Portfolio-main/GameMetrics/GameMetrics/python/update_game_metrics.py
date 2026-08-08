from pathlib import Path
import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Charge le .env situé à la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")

if not mongo_uri or not mongo_db:
    raise RuntimeError(
        "Variables MONGO_URI et/ou MONGO_DB manquantes dans le fichier .env"
    )

client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client[mongo_db]

games_collection = db["games"]
players_collection = db["players"]

print("=== Mise à jour des métriques des jeux ===")
print(f"Base utilisée : {mongo_db}")

for game in games_collection.find():
    game_id = game["_id"]
    reviews = game.get("reviews", [])

    review_count = len(reviews)

    if review_count > 0:
        avg_rating = sum(review.get("rating", 0) for review in reviews) / review_count
        recommended_count = sum(
            1 for review in reviews if review.get("recommended", False)
        )
        positive_ratio = recommended_count / review_count
    else:
        avg_rating = 0
        positive_ratio = 0

    total_playtime = 0
    player_count = 0

    for player in players_collection.find({"library.game_id": game_id}):
        for item in player.get("library", []):
            if item.get("game_id") == game_id:
                total_playtime += item.get("playtime", 0)
                player_count += 1

    if player_count > 0:
        avg_playtime = total_playtime / player_count
    else:
        avg_playtime = 0

    engagement_score = round(
        (avg_rating * 0.4) + (positive_ratio * 100 * 0.3) + (avg_playtime * 0.3),
        2,
    )

    games_collection.update_one(
        {"_id": game_id},
        {
            "$set": {
                "metrics.avg_rating": round(avg_rating, 2),
                "metrics.positive_ratio": round(positive_ratio, 2),
                "metrics.review_count": review_count,
                "metrics.engagement_score": engagement_score,
            }
        },
    )

    print(f"Jeu mis à jour : {game['title']}")
    print(f"  avg_rating = {round(avg_rating, 2)}")
    print(f"  positive_ratio = {round(positive_ratio, 2)}")
    print(f"  review_count = {review_count}")
    print(f"  engagement_score = {engagement_score}")
    print("-" * 40)

print("Mise à jour terminée.")
client.close()