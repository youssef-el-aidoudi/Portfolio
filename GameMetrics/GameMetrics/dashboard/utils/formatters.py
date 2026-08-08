from typing import Any


# ---------------------------------------------------------------------------
# Accès sécurisé aux données
# ---------------------------------------------------------------------------

def safe_get(data: dict, key: str, default: Any = "N/A") -> Any:
    """Retourne data[key] si présent et non None, sinon default."""
    val = data.get(key)
    return val if val is not None else default


def safe_nested(data: dict, *keys: str, default: Any = "N/A") -> Any:
    """Accès sécurisé en profondeur : safe_nested(d, 'a', 'b') = d['a']['b']."""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current


# ---------------------------------------------------------------------------
# Formatage des valeurs
# ---------------------------------------------------------------------------

def format_hours(minutes: int | float) -> str:
    """Convertit des minutes en format 'Xh Ymin' lisible."""
    if minutes is None:
        return "N/A"
    minutes = int(minutes)
    h = minutes // 60
    m = minutes % 60
    if h > 0 and m > 0:
        return f"{h}h {m}min"
    elif h > 0:
        return f"{h}h"
    else:
        return f"{m}min"


def format_ratio(ratio: float, precision: int = 1) -> str:
    """Convertit un ratio [0–1] en pourcentage formaté."""
    if ratio is None:
        return "N/A"
    return f"{ratio * 100:.{precision}f}%"


def format_score(value: float, precision: int = 2) -> str:
    """Formate un score numérique avec le bon nombre de décimales."""
    if value is None:
        return "N/A"
    return f"{value:.{precision}f}"


def format_rating(value: float) -> str:
    """Formate une note (avg_rating) avec 1 décimale sur 10."""
    if value is None:
        return "N/A"
    return f"{value:.1f} / 10"

def format_spec_value(value: Any) -> str:
    """
    Convertit une valeur de 'specifications' en chaîne lisible.
    Gère les listes, booléens, entiers et chaînes.
    """
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    if isinstance(value, bool):
        return "✅ Oui" if value else "❌ Non"
    if value is None:
        return "N/A"
    return str(value)


def specs_to_rows(specifications: dict) -> list[dict]:
    """
    Transforme le dict 'specifications' en liste de {Propriété, Valeur}
    pour affichage dans un tableau Streamlit, même avec schéma polymorphique.
    """
    if not isinstance(specifications, dict):
        return []

    # Labels plus lisibles pour les clés courantes
    labels = {
        "subgenre": "Sous-genre",
        "platforms": "Plateformes",
        "business_model": "Modèle économique",
        "team_format": "Format d'équipe",
        "perspective": "Perspective",
        "ranked_mode": "Mode classé",
        "voice_chat": "Chat vocal",
        "anti_cheat": "Anti-cheat",
        "main_modes": "Modes de jeu",
        "weapon_categories": "Catégories d'armes",
        "avg_match_duration_min": "Durée moyenne (min)",
        "avg_session_duration_min": "Durée session (min)",
        "avg_mission_duration_min": "Durée mission (min)",
        "play_style": "Style de jeu",
        "competitive_scene": "Scène compétitive",
        "hero_roles": "Rôles",
        "classes": "Classes",
        "cross_platform": "Cross-platform",
        "raid_size": "Taille de raid",
        "guild_system": "Système de guilde",
        "trading_system": "Système d'échange",
        "role_system": "Système de rôles",
        "champion_count": "Nombre de champions",
        "map_name": "Carte principale",
        "class_system": "Système de classes",
        "procedural_generation": "Génération procédurale",
    }

    rows = []
    for key, value in specifications.items():
        label = labels.get(key, key.replace("_", " ").capitalize())
        rows.append({"Propriété": label, "Valeur": format_spec_value(value)})
    return rows


# ---------------------------------------------------------------------------
# Statuts bibliothèque
# ---------------------------------------------------------------------------

STATUS_LABELS = {
    "active": "🟢 Actif",
    "inactive": "🟡 Inactif",
    "uninstalled": "🔴 Désinstallé",
}

SKILL_LABELS = {
    "beginner": "🔰 Débutant",
    "intermediate": "⚔️ Intermédiaire",
    "advanced": "🏆 Avancé",
    "expert": "💎 Expert",
}


def format_status(status: str) -> str:
    return STATUS_LABELS.get(status, status)


def format_skill(skill: str) -> str:
    return SKILL_LABELS.get(skill, skill)
