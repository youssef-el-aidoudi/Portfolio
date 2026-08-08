

import streamlit as st
from dashboard.db_utils import get_db, check_connection
from dashboard.services.analytics_service import get_insights_data
from dashboard.components.kpi_cards import insight_card
from dashboard.utils.styles import inject_css, section_title, divider
from dashboard.utils.formatters import (
    format_rating, format_ratio, format_score, format_hours,
)

st.set_page_config(
    page_title="Insights — GameMetrics",
    page_icon="💡",
    layout="wide",
)
inject_css()
st.markdown('<style>[data-testid="stSidebarNav"],[data-testid="stSidebarNavItems"]{display:none!important;}</style>', unsafe_allow_html=True)

ok, msg = check_connection()
if not ok:
    st.error(f"❌ MongoDB inaccessible : {msg}")
    st.stop()
db = get_db()

# ---------------------------------------------------------------------------
# En-tête
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="page-header">
        <h1>💡 Insights</h1>
        <p>
            Conclusions automatiques extraites par agrégation MongoDB.
            Ces résultats sont recalculés à chaque chargement de la page.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Chargement des données
# ---------------------------------------------------------------------------
try:
    with st.spinner("Analyse des données en cours…"):
        data = get_insights_data(db)
except Exception as e:
    st.error(f"Erreur lors de l'analyse : {e}")
    st.stop()

if not data:
    st.warning("⚠️ Aucune donnée disponible. Vérifiez votre base MongoDB.")
    st.stop()


section_title("🏆", "Champions par catégorie")

col1, col2 = st.columns(2)

with col1:
    g = data.get("best_rated", {})
    m = g.get("metrics", {}) if g else {}
    insight_card(
        "⭐", "Jeu le mieux noté",
        g.get("title", "N/A") if g else "N/A",
        f"Note : {format_rating(m.get('avg_rating'))} — {m.get('review_count', 0)} avis"
        if g else "",
    )

    g = data.get("best_engage", {})
    m = g.get("metrics", {}) if g else {}
    insight_card(
        "🔥", "Meilleur score d'engagement",
        g.get("title", "N/A") if g else "N/A",
        f"Score : {format_score(m.get('engagement_score'))} (note × ratio × temps de jeu)"
        if g else "",
    )

with col2:
    g = data.get("best_positive", {})
    m = g.get("metrics", {}) if g else {}
    insight_card(
        "👍", "Jeu le plus apprécié",
        g.get("title", "N/A") if g else "N/A",
        f"{format_ratio(m.get('positive_ratio'))} d'avis recommandés"
        if g else "",
    )

    g = data.get("most_reviewed", {})
    insight_card(
        "💬", "Jeu avec le plus d'avis",
        g.get("title", "N/A") if g else "N/A",
        f"{len(g.get('reviews', []))} avis communautaires" if g else "",
    )

divider()


section_title("📉", "Rétention & Abandons")

worst = data.get("worst_retain")
if worst:
    insight_card(
        "🚫", "Jeu le plus désinstallé",
        worst.get("title", worst.get("game_id", "N/A")),
        f"{worst.get('uninstall_count', 0)} désinstallation(s) enregistrée(s) — "
        "indique un problème de rétention ou d'attentes non satisfaites.",
    )
else:
    st.info("Aucune désinstallation enregistrée dans la base.")

divider()


section_title("👤", "Joueurs remarquables")

col3, col4 = st.columns(2)

with col3:
    top = data.get("top_player")
    if top:
        hours = round(top.get("total_playtime", 0) / 60, 1)
        insight_card(
            "⏱️", "Joueur le plus actif (temps de jeu)",
            top.get("username", "N/A"),
            f"{format_hours(top.get('total_playtime', 0))} cumulées — véritable habitué.",
        )
    else:
        st.info("Données joueurs non disponibles.")

with col4:
    mgp = data.get("most_games_player")
    if mgp:
        nb = len(mgp.get("library", []))
        insight_card(
            "🎮", "Joueur avec la plus grande bibliothèque",
            mgp.get("username", "N/A"),
            f"{nb} jeu{'x' if nb > 1 else ''} dans sa bibliothèque.",
        )
    else:
        st.info("Données joueurs non disponibles.")

divider()


section_title("📊", "Synthèse générale")

total_g = data.get("total_games", 0)
total_p = data.get("total_players", 0)

st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #16162A, #1E1E3A);
        border: 1px solid rgba(124,58,237,0.2);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        color: #94A3B8;
        line-height: 2;
        font-size: 0.95rem;
    ">
        La base <b style="color:#E2E8F0;">GameMetrics</b> recense
        <b style="color:#9F67FF;">{total_g} jeux</b> multijoueurs analysés
        et <b style="color:#9F67FF;">{total_p} joueurs</b> enregistrés.<br>
        Les métriques sont calculées via un script Python utilisant pymongo,
        combinant note moyenne, ratio d'avis positifs et temps de jeu moyen
        dans une formule d'engagement pondérée.<br>
        Les pipelines d'agrégation MongoDB permettent d'obtenir ces résultats
        directement côté serveur, sans traitement Pandas côté client.
    </div>
    """,
    unsafe_allow_html=True,
)
