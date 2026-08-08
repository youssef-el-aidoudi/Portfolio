import streamlit as st
from typing import Optional


@st.cache_data(ttl=60, show_spinner=False)
def get_all_players(_db) -> list[dict]:
    """Retourne tous les joueurs de la collection 'players'."""
    return list(_db.players.find())


@st.cache_data(ttl=60, show_spinner=False)
def get_regions(_db) -> list[str]:
    """Liste unique et triée des régions disponibles."""
    return sorted(_db.players.distinct("region"))

def get_player_by_id(_db, player_id: str) -> Optional[dict]:
    """Retourne le document complet d'un joueur par son _id."""
    return _db.players.find_one({"_id": player_id})
def compute_player_stats(player: dict) -> dict:
    library = player.get("library", [])

    total_playtime = sum(item.get("playtime", 0) for item in library)

    status_counts = {"active": 0, "inactive": 0, "uninstalled": 0}
    for item in library:
        status = item.get("status", "")
        if status in status_counts:
            status_counts[status] += 1

    return {
        "total_playtime": total_playtime,
        "game_count": len(library),
        "active_count": status_counts["active"],
        "inactive_count": status_counts["inactive"],
        "uninstalled_count": status_counts["uninstalled"],
    }
