import streamlit as st
from dashboard.db_utils import get_db, check_connection
from dashboard.services import analytics_service as agg
from dashboard.components import charts
from dashboard.utils.styles import inject_css, section_title, divider

st.set_page_config(
    page_title="Analyses — GameMetrics",
    page_icon="📊",
    layout="wide",
)

inject_css()
st.markdown(
    '<style>[data-testid="stSidebarNav"],[data-testid="stSidebarNavItems"]{display:none!important;}</style>',
    unsafe_allow_html=True,
)

ok, msg = check_connection()
if not ok:
    st.error(f"❌ MongoDB inaccessible : {msg}")
    st.stop()

db = get_db()

st.markdown(
    """
    <div class="page-header">
        <h1>📊 Analyses</h1>
        <p>
            Visualisations produites par des pipelines d'agrégation MongoDB côté serveur.
            Aucun re-groupement Pandas — MongoDB fait le travail.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

def show_chart(fetch_fn, chart_fn, title: str, chart_key: str, pipeline_help: str | None = None):
    try:
        data = fetch_fn(db)
    except Exception as e:
        st.error(f"Erreur MongoDB : {e}")
        return

    if pipeline_help:
        with st.expander("🔍 Pipeline MongoDB utilisé", expanded=False):
            st.code(pipeline_help, language="javascript")

    if not data:
        st.info(f"Aucune donnée disponible pour : {title}")
        return

    try:
        fig = chart_fn(data)
        st.plotly_chart(fig, use_container_width=True, key=chart_key)
    except Exception as e:
        st.error(f"Erreur lors de la génération du graphique « {title} » : {e}")

section_title("🎮", "Distribution & Notations")

col1, col2 = st.columns(2)

with col1:
    show_chart(
        agg.games_by_genre,
        charts.chart_games_by_genre,
        "Jeux par genre",
        "fig_games_by_genre",
        pipeline_help="""[
  { $group: { _id: "$genre", total_games: { $sum: 1 } } },
  { $sort:  { total_games: -1 } }
]""",
    )

with col2:
    show_chart(
        agg.review_count_per_game,
        charts.chart_review_count,
        "Nombre d'avis par jeu",
        "fig_review_count_per_game",
        pipeline_help="""[
  { $project: { title: 1, review_count: { $size: "$reviews" } } },
  { $sort: { review_count: -1 } }
]""",
    )

divider()

section_title("⭐", "Métriques de qualité")

col3, col4 = st.columns(2)

with col3:
    show_chart(
        agg.avg_rating_per_game,
        charts.chart_avg_rating,
        "Note moyenne par jeu",
        "fig_avg_rating_per_game",
        pipeline_help="""[
  { $project: { title: 1, avg_rating: "$metrics.avg_rating" } },
  { $sort: { avg_rating: -1 } }
]""",
    )

with col4:
    show_chart(
        agg.positive_ratio_per_game,
        charts.chart_positive_ratio,
        "Ratio d'avis positifs par jeu",
        "fig_positive_ratio_per_game",
        pipeline_help="""[
  { $unwind: "$reviews" },
  { $group: {
      _id: "$title",
      total_reviews: { $sum: 1 },
      recommended_count: { $sum: { $cond: ["$reviews.recommended", 1, 0] } }
  }},
  { $project: {
      title: "$_id",
      positive_ratio_pct: { $multiply: [
        { $divide: ["$recommended_count", "$total_reviews"] }, 100
      ]}
  }},
  { $sort: { positive_ratio_pct: -1 } }
]""",
    )

divider()

section_title("🔥", "Score d'engagement")

show_chart(
    agg.engagement_score_per_game,
    charts.chart_engagement_score,
    "Score d'engagement par jeu",
    "fig_engagement_score_per_game",
    pipeline_help="""[
  { $project: { title: 1, engagement_score: "$metrics.engagement_score" } },
  { $sort: { engagement_score: -1 } }
]
/* Formule :
   engagement_score = (avg_rating * 0.4)
                    + (positive_ratio * 100 * 0.3)
                    + (avg_playtime * 0.3)
   Calculé par python/update_game_metrics.py */""",
)

divider()

section_title("👤", "Comportement des joueurs")

col5, col6 = st.columns(2)

with col5:
    show_chart(
        agg.playtime_per_player,
        charts.chart_playtime_per_player,
        "Temps de jeu total par joueur",
        "fig_playtime_per_player",
        pipeline_help="""[
  { $unwind: "$library" },
  { $group: { _id: "$username", total_playtime: { $sum: "$library.playtime" } } },
  { $sort: { total_playtime: -1 } }
]""",
    )

with col6:
    show_chart(
        agg.most_uninstalled_games,
        charts.chart_most_uninstalled,
        "Jeux les plus désinstallés",
        "fig_most_uninstalled_games",
        pipeline_help="""[
  { $unwind: "$library" },
  { $match: { "library.status": "uninstalled" } },
  { $group: { _id: "$library.game_id", uninstall_count: { $sum: 1 } } },
  { $lookup: { from: "games", localField: "_id",
               foreignField: "_id", as: "game_info" } },
  { $sort: { uninstall_count: -1 } }
]""",
    )