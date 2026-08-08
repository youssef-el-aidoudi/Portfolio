import streamlit as st
from typing import Optional
@st.cache_data(ttl=60, show_spinner=False)
def get_all_games(_db) -> list[dict]:
    """Retourne tous les jeux de la collection 'games'."""
    return list(_db.games.find())


@st.cache_data(ttl=60, show_spinner=False)
def get_genres(_db) -> list[str]:
    """Liste unique et triée des genres disponibles."""
    return sorted(_db.games.distinct("genre"))


@st.cache_data(ttl=60, show_spinner=False)
def get_developers(_db) -> list[str]:
    """Liste unique et triée des développeurs disponibles."""
    return sorted(_db.games.distinct("developer"))


@st.cache_data(ttl=60, show_spinner=False)
def get_business_models(_db) -> list[str]:
    """
    Liste unique des modèles économiques présents dans specifications.
    Filtre les valeurs None (schéma polymorphique — tous les jeux n'ont
    pas forcément ce champ).
    """
    values = _db.games.distinct("specifications.business_model")
    return sorted(v for v in values if v is not None)


def get_game_by_id(_db, game_id: str) -> Optional[dict]:
    """Retourne le document complet d'un jeu par son _id."""
    return _db.games.find_one({"_id": game_id})


@st.cache_data(ttl=60, show_spinner=False)
def get_kpi_data(_db) -> dict:
    """
    Calcule les KPI principaux en une seule passe sur la collection.
    Retourne un dict prêt à l'emploi pour les cartes d'accueil.
    """
    games = list(_db.games.find(
        {},
        {"title": 1, "metrics": 1, "reviews": 1}
    ))

    if not games:
        return {
            "total_games": 0,
            "total_players": 0,
            "total_reviews": 0,
            "best_engagement": "N/A",
            "best_engagement_score": 0.0,
            "best_rated": "N/A",
            "best_rated_score": 0.0,
            "most_reviewed": "N/A",
            "most_reviewed_count": 0,
        }

    players_count = _db.players.count_documents({})
    total_reviews = sum(len(g.get("reviews", [])) for g in games)

    def metric(g: dict, key: str) -> float:
        return g.get("metrics", {}).get(key, 0) or 0

    best_eng = max(games, key=lambda g: metric(g, "engagement_score"))
    best_rat = max(games, key=lambda g: metric(g, "avg_rating"))
    most_rev = max(games, key=lambda g: len(g.get("reviews", [])))

    return {
        "total_games": len(games),
        "total_players": players_count,
        "total_reviews": total_reviews,
        "best_engagement": best_eng.get("title", "N/A"),
        "best_engagement_score": metric(best_eng, "engagement_score"),
        "best_rated": best_rat.get("title", "N/A"),
        "best_rated_score": metric(best_rat, "avg_rating"),
        "most_reviewed": most_rev.get("title", "N/A"),
        "most_reviewed_count": len(most_rev.get("reviews", [])),
    }
