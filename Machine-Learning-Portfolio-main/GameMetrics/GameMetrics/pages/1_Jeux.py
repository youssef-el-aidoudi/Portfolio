import streamlit as st
import pandas as pd
from dashboard.db_utils import get_db, check_connection
from dashboard.services.game_service import (
    get_all_games,
    get_genres,
    get_developers,
    get_business_models,
    get_game_by_id,
)
from dashboard.components.charts import chart_game_radar
from dashboard.utils.styles import inject_css, section_title, divider
from dashboard.utils.formatters import (
    format_rating,
    format_ratio,
    format_score,
    specs_to_rows,
)

st.set_page_config(
    page_title="Jeux — GameMetrics",
    page_icon="🎮",
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
        <h1>🎮 Catalogue des Jeux</h1>
        <p>Explorez, filtrez et analysez les jeux de la base GameMetrics.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    games = get_all_games(db)
except Exception as e:
    st.error(f"Erreur lors du chargement des jeux : {e}")
    st.stop()

if not games:
    st.warning("⚠️ La collection `games` est vide. Lancez d'abord `mongodb/insert_data.js`.")
    st.stop()

with st.sidebar:
    st.markdown("## 🔍 Filtres")
    genres = ["Tous"] + get_genres(db)
    selected_genre = st.selectbox("Genre", genres)

    devs = ["Tous"] + get_developers(db)
    selected_dev = st.selectbox("Développeur", devs)

    bm_list = get_business_models(db)
    if bm_list:
        bm_options = ["Tous"] + bm_list
        selected_bm = st.selectbox("Modèle économique", bm_options)
    else:
        selected_bm = "Tous"

    search = st.text_input("🔎 Recherche par titre", placeholder="ex: Valorant")
    st.divider()
    st.caption(f"{len(games)} jeux au total")

filtered = games

if selected_genre != "Tous":
    filtered = [g for g in filtered if g.get("genre") == selected_genre]

if selected_dev != "Tous":
    filtered = [g for g in filtered if g.get("developer") == selected_dev]

if selected_bm != "Tous":
    filtered = [
        g for g in filtered
        if g.get("specifications", {}).get("business_model") == selected_bm
    ]

if search.strip():
    q = search.strip().lower()
    filtered = [g for g in filtered if q in g.get("title", "").lower()]

section_title("📋", f"Résultats ({len(filtered)} jeu{'x' if len(filtered) > 1 else ''})")

if not filtered:
    st.info("Aucun jeu ne correspond aux filtres sélectionnés.")
else:
    rows = []
    for g in filtered:
        m = g.get("metrics", {})
        rows.append(
            {
                "Titre": g.get("title", "N/A"),
                "Genre": g.get("genre", "N/A"),
                "Développeur": g.get("developer", "N/A"),
                "Modèle": g.get("specifications", {}).get("business_model", "N/A"),
                "Note moy.": f"{(m.get('avg_rating') or 0):.1f} / 10",
                "Positifs": f"{(m.get('positive_ratio') or 0) * 100:.0f}%",
                "Avis": m.get("review_count") or 0,
                "Engagement": f"{(m.get('engagement_score') or 0):.2f}",
                "_id": g.get("_id"),
            }
        )

    df = pd.DataFrame(rows)
    display_df = df.drop(columns=["_id"])

    selected_rows = st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Note moy.": st.column_config.TextColumn("⭐ Note moy."),
            "Positifs": st.column_config.TextColumn("👍 Positifs"),
            "Avis": st.column_config.NumberColumn("💬 Avis"),
            "Engagement": st.column_config.TextColumn("🔥 Engagement"),
        },
    )

    sel_indices = selected_rows.selection.get("rows", []) if selected_rows else []

    if sel_indices:
        game_id = df.iloc[sel_indices[0]]["_id"]
        game = get_game_by_id(db, game_id)

        if game:
            divider()
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #16162A, #1E1E3A);
                    border: 1px solid rgba(124,58,237,0.3);
                    border-radius: 14px;
                    padding: 1.5rem 2rem;
                    margin-bottom: 1.5rem;
                ">
                    <span style="
                        font-size:0.78rem;
                        color:#7C3AED;
                        font-weight:600;
                        text-transform:uppercase;
                        letter-spacing:0.08em;
                    ">
                        Fiche jeu
                    </span>
                    <h2 style="
                        margin:0.3rem 0 0;
                        color:#E2E8F0;
                        font-size:1.8rem;
                        font-weight:800;
                    ">
                        {game.get('title', 'N/A')}
                    </h2>
                    <span style="color:#94A3B8; font-size:0.9rem;">
                        {game.get('developer','N/A')} · {game.get('genre','N/A')} · {game.get('release_date','N/A')}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            tab_general, tab_specs, tab_metrics, tab_reviews = st.tabs(
                ["📋 Général", "⚙️ Spécifications", "📈 Métriques", "💬 Avis"]
            )

            with tab_general:
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Titre", game.get("title", "N/A"))
                    st.metric("Développeur", game.get("developer", "N/A"))
                    st.metric("Genre", game.get("genre", "N/A"))
                with c2:
                    st.metric("Date de sortie", game.get("release_date", "N/A"))
                    bm = game.get("specifications", {}).get("business_model", "N/A")
                    st.metric("Modèle économique", bm or "N/A")
                    st.metric("ID", game.get("_id", "N/A"))

            with tab_specs:
                specs = game.get("specifications", {})
                if specs:
                    spec_rows = specs_to_rows(specs)
                    st.dataframe(
                        pd.DataFrame(spec_rows),
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info("Aucune spécification disponible pour ce jeu.")

            with tab_metrics:
                m = game.get("metrics", {})
                if any(v for v in m.values()):
                    col_m1, col_m2 = st.columns([2, 3])
                    with col_m1:
                        st.metric("⭐ Note moyenne", format_rating(m.get("avg_rating")))
                        st.metric("👍 Ratio positifs", format_ratio(m.get("positive_ratio")))
                        st.metric("💬 Nombre d'avis", m.get("review_count", 0))
                        st.metric("🔥 Engagement", format_score(m.get("engagement_score")))
                    with col_m2:
                        fig = chart_game_radar(game)
                        st.plotly_chart(
                            fig,
                            use_container_width=True,
                            key=f"radar_{game_id}",
                        )
                else:
                    st.warning(
                        "Les métriques n'ont pas encore été calculées. "
                        "Utilisez le bouton **Recalculer les métriques** dans la sidebar de l'accueil."
                    )

            with tab_reviews:
                reviews = game.get("reviews", [])
                if not reviews:
                    st.info("Aucun avis enregistré pour ce jeu.")
                else:
                    st.caption(f"{len(reviews)} avis pour ce jeu")
                    for rev in reviews:
                        recommended = rev.get("recommended", False)
                        rec_icon = "👍" if recommended else "👎"
                        rec_color = "#10B981" if recommended else "#EF4444"
                        st.markdown(
                            f"""
                            <div class="review-card">
                                <div class="review-header">
                                    <span class="review-author">{rev.get('author_id','Anonyme')}</span>
                                    <span class="review-rating">⭐ {rev.get('rating','?')} / 10</span>
                                </div>
                                <div class="review-comment">"{rev.get('comment','')}"</div>
                                <div class="review-date">
                                    <span style="color:{rec_color};">{rec_icon} {'Recommandé' if recommended else 'Non recommandé'}</span>
                                    &nbsp;·&nbsp; {rev.get('date','N/A')}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
        else:
            st.error("Jeu introuvable dans la base.")
    else:
        st.caption("👆 Cliquez sur une ligne du tableau pour voir la fiche détaillée.")