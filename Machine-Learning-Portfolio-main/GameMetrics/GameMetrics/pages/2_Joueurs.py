import streamlit as st
import pandas as pd
from dashboard.db_utils import get_db, check_connection
from dashboard.services.player_service import (
    get_all_players,
    get_regions,
    get_player_by_id,
    compute_player_stats,
)
from dashboard.services.game_service import get_game_by_id
from dashboard.utils.styles import inject_css, section_title, divider
from dashboard.utils.formatters import format_hours, format_status, format_skill

st.set_page_config(
    page_title="Joueurs — GameMetrics",
    page_icon="👤",
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
        <h1>👤 Joueurs</h1>
        <p>Explorez les profils des joueurs et leur bibliothèque de jeux.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    players = get_all_players(db)
except Exception as e:
    st.error(f"Erreur lors du chargement des joueurs : {e}")
    st.stop()

if not players:
    st.warning("⚠️ La collection `players` est vide. Lancez d'abord `mongodb/insert_data.js`.")
    st.stop()

with st.sidebar:
    st.markdown("## 🔍 Filtres")

    regions = ["Toutes"] + get_regions(db)
    selected_region = st.selectbox("Région", regions)

    search = st.text_input("🔎 Pseudo", placeholder="ex: Yanis")

    st.divider()
    st.caption(f"{len(players)} joueurs au total")

filtered = players

if selected_region != "Toutes":
    filtered = [p for p in filtered if p.get("region") == selected_region]

if search.strip():
    q = search.strip().lower()
    filtered = [p for p in filtered if q in p.get("username", "").lower()]

section_title("📋", f"Résultats ({len(filtered)} joueur{'s' if len(filtered) > 1 else ''})")

if not filtered:
    st.info("Aucun joueur ne correspond aux filtres sélectionnés.")
else:
    rows = []
    for p in filtered:
        stats = compute_player_stats(p)
        rows.append(
            {
                "Pseudo": p.get("username", "N/A"),
                "Région": p.get("region", "N/A"),
                "Inscription": p.get("join_date", "N/A"),
                "Jeux": stats["game_count"],
                "Temps total": format_hours(stats["total_playtime"]),
                "Actifs": stats["active_count"],
                "Inactifs": stats["inactive_count"],
                "Désinstallés": stats["uninstalled_count"],
                "_id": p.get("_id"),
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
            "Jeux": st.column_config.NumberColumn("🎮 Jeux"),
            "Temps total": st.column_config.TextColumn("⏱️ Temps total"),
            "Actifs": st.column_config.NumberColumn("🟢 Actifs"),
            "Inactifs": st.column_config.NumberColumn("🟡 Inactifs"),
            "Désinstallés": st.column_config.NumberColumn("🔴 Désinstallés"),
        },
    )

    sel_indices = selected_rows.selection.get("rows", []) if selected_rows else []

    if sel_indices:
        player_id = df.iloc[sel_indices[0]]["_id"]
        player = get_player_by_id(db, player_id)

        if player:
            stats = compute_player_stats(player)
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
                        Fiche joueur
                    </span>
                    <h2 style="
                        margin:0.3rem 0 0;
                        color:#E2E8F0;
                        font-size:1.8rem;
                        font-weight:800;
                    ">
                        {player.get('username', 'N/A')}
                    </h2>
                    <span style="color:#94A3B8; font-size:0.9rem;">
                        {player.get('region', 'N/A')} · Inscrit le {player.get('join_date', 'N/A')}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            tab_profil, tab_library = st.tabs(["👤 Profil", "📚 Bibliothèque"])

            with tab_profil:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("🎮 Jeux possédés", stats["game_count"])
                c2.metric("⏱️ Temps total", format_hours(stats["total_playtime"]))
                c3.metric("🟢 Jeux actifs", stats["active_count"])
                c4.metric("🔴 Désinstallés", stats["uninstalled_count"])

                st.divider()
                c5, c6 = st.columns(2)
                c5.metric("Région", player.get("region", "N/A"))
                c6.metric("ID joueur", player.get("_id", "N/A"))

            with tab_library:
                library = player.get("library", [])
                if not library:
                    st.info("Bibliothèque vide.")
                else:
                    for item in library:
                        game_id = item.get("game_id", "")
                        game_doc = get_game_by_id(db, game_id)
                        game_title = game_doc.get("title", game_id) if game_doc else game_id
                        status = item.get("status", "")
                        skill = item.get("skill_level", "")
                        playtime = item.get("playtime", 0)
                        last_played = item.get("last_played", "N/A")

                        st.markdown(
                            f"""
                            <div class="review-card">
                                <div class="review-header">
                                    <span class="review-author" style="font-size:1rem;">
                                        🎮 {game_title}
                                    </span>
                                    <span>{format_status(status)}</span>
                                </div>
                                <div style="display:flex; gap:2rem; margin-top:0.5rem; flex-wrap:wrap;">
                                    <span style="color:#94A3B8; font-size:0.85rem;">
                                        ⏱️ <b style="color:#E2E8F0;">{format_hours(playtime)}</b> de jeu
                                    </span>
                                    <span style="color:#94A3B8; font-size:0.85rem;">
                                        🎯 Niveau : <b style="color:#E2E8F0;">{format_skill(skill)}</b>
                                    </span>
                                    <span style="color:#94A3B8; font-size:0.85rem;">
                                        📅 Dernière session : <b style="color:#E2E8F0;">{last_played}</b>
                                    </span>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
        else:
            st.error("Joueur introuvable dans la base.")
    else:
        st.caption("👆 Cliquez sur une ligne du tableau pour voir la fiche détaillée.")