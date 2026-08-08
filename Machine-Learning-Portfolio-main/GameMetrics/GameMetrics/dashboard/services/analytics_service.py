import streamlit as st




@st.cache_data(ttl=60, show_spinner=False)
def games_by_genre(_db) -> list[dict]:
    """Nombre de jeux par genre, trié par total décroissant."""
    pipeline = [
        {"$group": {"_id": "$genre", "total_games": {"$sum": 1}}},
        {"$sort": {"total_games": -1}},
        {"$project": {"_id": 0, "genre": "$_id", "total_games": 1}},
    ]
    return list(_db.games.aggregate(pipeline))




@st.cache_data(ttl=60, show_spinner=False)
def avg_rating_per_game(_db) -> list[dict]:
    """Note moyenne calculée (metrics.avg_rating) par jeu, décroissant."""
    pipeline = [
        {"$project": {
            "_id": 0,
            "title": 1,
            "avg_rating": "$metrics.avg_rating",
        }},
        {"$sort": {"avg_rating": -1}},
    ]
    return list(_db.games.aggregate(pipeline))

@st.cache_data(ttl=60, show_spinner=False)
def positive_ratio_per_game(_db) -> list[dict]:
    """
    Ratio d'avis recommandés calculé en temps réel depuis les reviews,
    identique au pipeline queries_aggregate.js §2.
    """
    pipeline = [
        {"$unwind": "$reviews"},
        {"$group": {
            "_id": "$title",
            "total_reviews": {"$sum": 1},
            "recommended_count": {
                "$sum": {"$cond": [{"$eq": ["$reviews.recommended", True]}, 1, 0]}
            },
        }},
        {"$project": {
            "_id": 0,
            "title": "$_id",
            "total_reviews": 1,
            "recommended_count": 1,
            "positive_ratio_pct": {
                "$multiply": [
                    {"$divide": ["$recommended_count", "$total_reviews"]},
                    100,
                ]
            },
        }},
        {"$sort": {"positive_ratio_pct": -1}},
    ]
    return list(_db.games.aggregate(pipeline))



@st.cache_data(ttl=60, show_spinner=False)
def engagement_score_per_game(_db) -> list[dict]:
    """Score d'engagement (metrics.engagement_score) par jeu, décroissant."""
    pipeline = [
        {"$project": {
            "_id": 0,
            "title": 1,
            "engagement_score": "$metrics.engagement_score",
        }},
        {"$sort": {"engagement_score": -1}},
    ]
    return list(_db.games.aggregate(pipeline))

@st.cache_data(ttl=60, show_spinner=False)
def review_count_per_game(_db) -> list[dict]:
    """Nombre d'avis par jeu, décroissant. Pipeline identique à §3 de queries_aggregate.js."""
    pipeline = [
        {"$project": {
            "_id": 0,
            "title": 1,
            "review_count": {"$size": "$reviews"},
        }},
        {"$sort": {"review_count": -1}},
    ]
    return list(_db.games.aggregate(pipeline))

@st.cache_data(ttl=60, show_spinner=False)
def playtime_per_player(_db) -> list[dict]:
    """Temps de jeu cumulé (minutes) par joueur. Pipeline identique à §4."""
    pipeline = [
        {"$unwind": "$library"},
        {"$group": {
            "_id": "$username",
            "total_playtime": {"$sum": "$library.playtime"},
        }},
        {"$sort": {"total_playtime": -1}},
        {"$project": {"_id": 0, "username": "$_id", "total_playtime": 1}},
    ]
    return list(_db.players.aggregate(pipeline))


@st.cache_data(ttl=60, show_spinner=False)
def most_uninstalled_games(_db) -> list[dict]:
    """
    Jeux les plus désinstallés, avec résolution du titre via $lookup.
    Étend le pipeline §5 de queries_aggregate.js avec un join MongoDB.
    """
    pipeline = [
        {"$unwind": "$library"},
        {"$match": {"library.status": "uninstalled"}},
        {"$group": {
            "_id": "$library.game_id",
            "uninstall_count": {"$sum": 1},
        }},
        # $lookup pour récupérer le titre du jeu
        {"$lookup": {
            "from": "games",
            "localField": "_id",
            "foreignField": "_id",
            "as": "game_info",
        }},
        {"$unwind": {"path": "$game_info", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 0,
            "game_id": "$_id",
            "title": {"$ifNull": ["$game_info.title", "$_id"]},
            "uninstall_count": 1,
        }},
        {"$sort": {"uninstall_count": -1}},
    ]
    return list(_db.players.aggregate(pipeline))


@st.cache_data(ttl=60, show_spinner=False)
def avg_playtime_per_game(_db) -> list[dict]:
    """Temps de jeu moyen et nombre de joueurs par jeu. Pipeline §6 + $lookup."""
    pipeline = [
        {"$unwind": "$library"},
        {"$group": {
            "_id": "$library.game_id",
            "avg_playtime": {"$avg": "$library.playtime"},
            "player_count": {"$sum": 1},
        }},
        {"$lookup": {
            "from": "games",
            "localField": "_id",
            "foreignField": "_id",
            "as": "game_info",
        }},
        {"$unwind": {"path": "$game_info", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 0,
            "title": {"$ifNull": ["$game_info.title", "$_id"]},
            "avg_playtime": {"$round": ["$avg_playtime", 1]},
            "player_count": 1,
        }},
        {"$sort": {"avg_playtime": -1}},
    ]
    return list(_db.players.aggregate(pipeline))


@st.cache_data(ttl=60, show_spinner=False)
def get_insights_data(_db) -> dict:
    """
    Agrège toutes les données nécessaires à la page Insights
    en un minimum de requêtes MongoDB.
    """
    # Jeux triés par différentes métriques
    games = list(_db.games.find(
        {},
        {"title": 1, "metrics": 1, "reviews": 1, "genre": 1}
    ))

    def metric(g, key):
        return g.get("metrics", {}).get(key) or 0

    if not games:
        return {}

    best_rated    = max(games, key=lambda g: metric(g, "avg_rating"))
    best_positive = max(games, key=lambda g: metric(g, "positive_ratio"))
    best_engage   = max(games, key=lambda g: metric(g, "engagement_score"))
    most_reviewed = max(games, key=lambda g: len(g.get("reviews", [])))

    # Jeu le plus désinstallé
    uninstalled = most_uninstalled_games(_db)
    worst_retain = uninstalled[0] if uninstalled else None

    # Joueur le plus actif (temps de jeu total)
    playtimes = playtime_per_player(_db)
    top_player = playtimes[0] if playtimes else None

    # Joueur dédié : le plus de jeux possédés
    players = list(_db.players.find({}, {"username": 1, "library": 1}))
    most_games_player = max(
        players, key=lambda p: len(p.get("library", [])), default=None
    ) if players else None

    return {
        "best_rated": best_rated,
        "best_positive": best_positive,
        "best_engage": best_engage,
        "most_reviewed": most_reviewed,
        "worst_retain": worst_retain,
        "top_player": top_player,
        "most_games_player": most_games_player,
        "total_games": len(games),
        "total_players": len(players),
    }
