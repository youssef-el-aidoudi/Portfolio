import streamlit as st
from dashboard.db_utils import get_db, check_connection
from dashboard.services.game_service import get_kpi_data
from dashboard.services.metrics_updater import run_metrics_update
from dashboard.components.kpi_cards import kpi_row
from dashboard.utils.styles import inject_css, section_title, divider
from dashboard.utils.formatters import format_rating, format_score

# ---------------------------------------------------------------------------
# Configuration de la page
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="GameMetrics Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS global + masquage navigation automatique Streamlit
# ---------------------------------------------------------------------------
inject_css()
st.markdown("""
<style>
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"] { display: none !important; }
/* Amélioration padding top sidebar */
section[data-testid="stSidebar"] > div:first-child { padding-top: 0; }
/* Réduire le gap des st.columns dans les KPI */
div[data-testid="column"] > div { height: 100%; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Vérification connexion MongoDB
# ---------------------------------------------------------------------------
ok, msg = check_connection()
if not ok:
    st.error(f"❌ **Connexion MongoDB impossible** — {msg}")
    st.info("Vérifiez que MongoDB est démarré et que `.env` contient `MONGO_URI`.")
    st.stop()

db = get_db()
with st.sidebar:

    # — Branding —
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1.4rem 0.5rem 1rem;
        border-bottom: 1px solid rgba(124,58,237,0.15);
        margin-bottom: 0.2rem;
    ">
        <div style="
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 54px; height: 54px;
            border-radius: 15px;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            font-size: 1.7rem;
            margin-bottom: 0.65rem;
            box-shadow: 0 4px 16px rgba(124,58,237,0.35);
        ">🎮</div>
        <div style="
            font-size: 1.08rem;
            font-weight: 700;
            color: #E2E8F0;
            letter-spacing: -0.01em;
        ">GameMetrics</div>
        <div style="
            font-size: 0.68rem;
            color: #4B5563;
            margin-top: 0.18rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        ">MongoDB Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    # — Navigation —
    st.markdown("""
    <p style="
        font-size: 0.65rem;
        color: #4B5563;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 0.9rem 0 0.25rem 0.1rem;
    ">Pages</p>
    """, unsafe_allow_html=True)

    st.page_link("app.py",             label="🏠  Accueil")
    st.page_link("pages/1_Jeux.py",    label="🎮  Jeux")
    st.page_link("pages/2_Joueurs.py", label="👤  Joueurs")
    st.page_link("pages/3_Analyses.py",label="📊  Analyses")
    st.page_link("pages/4_Insights.py",label="💡  Insights")
    st.page_link("pages/5_A_Propos.py",label="📖  À Propos")

    # — Actions —
    st.markdown("""
    <p style="
        font-size: 0.65rem;
        color: #4B5563;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 1rem 0 0.35rem 0.1rem;
    ">Actions</p>
    """, unsafe_allow_html=True)

    if st.button("⚡ Recalculer les métriques",
                 use_container_width=True, type="primary"):
        with st.spinner("Lancement de `python/update_game_metrics.py`…"):
            success, output = run_metrics_update()
        if success:
            st.success("✅ Métriques mises à jour !")
            st.cache_data.clear()
            with st.expander("Voir la sortie", expanded=False):
                st.code(output, language="text")
        else:
            st.error("❌ Échec du recalcul")
            st.code(output, language="text")

    if st.button("🔃 Rafraîchir les données", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # — Statut base de données —
    st.markdown("""
    <div style="
        margin-top: 1rem;
        background: rgba(16,185,129,0.07);
        border: 1px solid rgba(16,185,129,0.2);
        border-radius: 9px;
        padding: 0.6rem 0.85rem;
    ">
        <div style="
            font-size: 0.73rem;
            color: #10B981;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        ">
            <span style="
                display:inline-block;width:6px;height:6px;
                border-radius:50%;background:#10B981;
                box-shadow:0 0 5px #10B981;
            "></span>
            MongoDB connectée
        </div>
        <div style="font-size:0.67rem;color:#374151;margin-top:0.15rem;">
            Base : <span style="color:#6B7280;">gamemetrics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("""
<div style="
    background: linear-gradient(145deg, #12122A 0%, #191930 45%, #0E0E1C 100%);
    border: 1px solid rgba(124, 58, 237, 0.22);
    border-radius: 18px;
    padding: 2.2rem 2.6rem 2rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
">
    <div style="
        position:absolute; top:-60px; right:-40px;
        width:240px; height:240px; border-radius:50%;
        background:radial-gradient(circle, rgba(124,58,237,0.13) 0%, transparent 68%);
        pointer-events:none;
    "></div>
    <div style="
        position:absolute; bottom:-70px; left:30px;
        width:190px; height:190px; border-radius:50%;
        background:radial-gradient(circle, rgba(6,182,212,0.07) 0%, transparent 70%);
        pointer-events:none;
    "></div>
    <div style="
        font-size:0.7rem; font-weight:700; color:#7C3AED;
        text-transform:uppercase; letter-spacing:0.12em;
        margin-bottom:0.55rem;
    ">Projet Master 1 — Base de données NoSQL</div>
    <div style="
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(130deg, #F1F5F9 20%, #C4B5FD 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.05;
        letter-spacing: -0.04em;
        margin-bottom: 0.6rem;
    ">🎮 GameMetrics</div>
    <div style="
        color: #94A3B8;
        font-size: 1rem;
        max-width: 560px;
        line-height: 1.7;
        margin-bottom: 1.3rem;
    ">
        Analyse de l'engagement des joueurs et des évaluations de la communauté
        sur les jeux multijoueurs populaires
    </div>
    <div style="display:flex; gap:0.45rem; flex-wrap:wrap; align-items:center;">
        <span style="background:rgba(124,58,237,0.14);border:1px solid rgba(124,58,237,0.32);
            border-radius:20px;padding:0.18rem 0.75rem;font-size:0.7rem;font-weight:600;
            color:#A78BFA;letter-spacing:0.04em;">&#x25CF; MongoDB</span>
        <span style="background:rgba(6,182,212,0.1);border:1px solid rgba(6,182,212,0.28);
            border-radius:20px;padding:0.18rem 0.75rem;font-size:0.7rem;font-weight:600;
            color:#22D3EE;letter-spacing:0.04em;">&#x25CF; Streamlit</span>
        <span style="background:rgba(16,185,129,0.09);border:1px solid rgba(16,185,129,0.25);
            border-radius:20px;padding:0.18rem 0.75rem;font-size:0.7rem;font-weight:600;
            color:#34D399;letter-spacing:0.04em;">&#x25CF; Python 3</span>
        <span style="background:rgba(245,158,11,0.09);border:1px solid rgba(245,158,11,0.25);
            border-radius:20px;padding:0.18rem 0.75rem;font-size:0.7rem;font-weight:600;
            color:#FCD34D;letter-spacing:0.04em;">&#x25CF; Plotly</span>
        <span style="background:rgba(148,163,184,0.07);border:1px solid rgba(148,163,184,0.18);
            border-radius:20px;padding:0.18rem 0.75rem;font-size:0.7rem;font-weight:600;
            color:#6B7280;letter-spacing:0.04em;">pymongo</span>
    </div>
</div>
""", unsafe_allow_html=True)

section_title("📊", "Indicateurs clés")

try:
    kpi = get_kpi_data(db)

    kpi_row([
        ("🎮", kpi["total_games"],   "Jeux analysés"),
        ("👤", kpi["total_players"], "Joueurs enregistrés"),
        ("💬", kpi["total_reviews"], "Avis communautaires"),
    ])

    st.write("")   # respiraton verticale entre les 2 lignes

    kpi_row([
        ("🏆", kpi["best_engagement"],
         "Meilleur engagement",
         f"Score : {format_score(kpi['best_engagement_score'])}"),
        ("⭐", kpi["best_rated"],
         "Meilleure note moyenne",
         format_rating(kpi["best_rated_score"])),
        ("💬", kpi["most_reviewed"],
         "Plus d'avis",
         f"{kpi['most_reviewed_count']} avis recensés"),
    ])

except Exception as e:
    st.error(f"Impossible de charger les KPI : {e}")

divider()
section_title("📋", "À propos du projet")

col_desc, col_stack = st.columns([3, 2], gap="large")

with col_desc:
    st.markdown("""
    <div style="
        background: linear-gradient(150deg, #13132A 0%, #1A1A30 100%);
        border: 1px solid rgba(124,58,237,0.15);
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        height: 100%;
        box-sizing: border-box;
    ">
        <p style="margin:0 0 0.9rem;font-size:0.95rem;color:#CBD5E1;font-weight:600;
            letter-spacing:-0.01em;">
            Conception et exploitation d'une base MongoDB NoSQL
        </p>
        <p style="margin:0 0 0.7rem;font-size:0.85rem;color:#94A3B8;line-height:1.7;">
            GameMetrics explore les capacités de MongoDB pour la modélisation
            de données hétérogènes et les analyses communautaires sur les
            jeux multijoueurs populaires.
        </p>
        <div style="display:flex;flex-direction:column;gap:0.4rem;margin-top:0.8rem;">
            <div style="display:flex;align-items:flex-start;gap:0.6rem;font-size:0.83rem;color:#94A3B8;">
                <span style="color:#7C3AED;font-weight:700;flex-shrink:0;">▸</span>
                <span><b style="color:#CBD5E1;">Schéma polymorphique</b> — specifications adapté à chaque genre de jeu</span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:0.6rem;font-size:0.83rem;color:#94A3B8;">
                <span style="color:#7C3AED;font-weight:700;flex-shrink:0;">▸</span>
                <span><b style="color:#CBD5E1;">Documents imbriqués</b> — reviews directement dans chaque jeu</span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:0.6rem;font-size:0.83rem;color:#94A3B8;">
                <span style="color:#7C3AED;font-weight:700;flex-shrink:0;">▸</span>
                <span><b style="color:#CBD5E1;">Références croisées</b> — library des joueurs référence les jeux</span>
            </div>
            <div style="display:flex;align-items:flex-start;gap:0.6rem;font-size:0.83rem;color:#94A3B8;">
                <span style="color:#7C3AED;font-weight:700;flex-shrink:0;">▸</span>
                <span><b style="color:#CBD5E1;">Agrégation avancée</b> — pipelines MongoDB côté serveur</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_stack:
    st.markdown("""
    <div style="
        background: linear-gradient(150deg, #13132A 0%, #1A1A30 100%);
        border: 1px solid rgba(124,58,237,0.15);
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        height: 100%;
        box-sizing: border-box;
    ">
        <p style="margin:0 0 1rem;font-size:0.95rem;color:#CBD5E1;font-weight:600;
            letter-spacing:-0.01em;">Stack technique</p>
        <div style="display:flex;flex-direction:column;gap:0.55rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;
                font-size:0.82rem;padding:0.35rem 0;
                border-bottom:1px solid rgba(124,58,237,0.1);">
                <span style="color:#64748B;font-weight:500;">Base de données</span>
                <span style="color:#A78BFA;font-weight:600;">MongoDB</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                font-size:0.82rem;padding:0.35rem 0;
                border-bottom:1px solid rgba(124,58,237,0.1);">
                <span style="color:#64748B;font-weight:500;">Driver Python</span>
                <span style="color:#A78BFA;font-weight:600;">pymongo</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                font-size:0.82rem;padding:0.35rem 0;
                border-bottom:1px solid rgba(124,58,237,0.1);">
                <span style="color:#64748B;font-weight:500;">Dashboard</span>
                <span style="color:#22D3EE;font-weight:600;">Streamlit</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                font-size:0.82rem;padding:0.35rem 0;
                border-bottom:1px solid rgba(124,58,237,0.1);">
                <span style="color:#64748B;font-weight:500;">Graphiques</span>
                <span style="color:#FCD34D;font-weight:600;">Plotly</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;
                font-size:0.82rem;padding:0.35rem 0;">
                <span style="color:#64748B;font-weight:500;">Configuration</span>
                <span style="color:#34D399;font-weight:600;">python-dotenv</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ██████  SECTION — Collections MongoDB
# ---------------------------------------------------------------------------
divider()
section_title("🗄️", "Collections MongoDB")

col_games, col_players = st.columns(2, gap="large")

_field_row = lambda label, note="": (
    f'<div style="display:flex;align-items:baseline;gap:0.5rem;'
    f'padding:0.3rem 0;border-bottom:1px solid rgba(124,58,237,0.07);'
    f'font-size:0.82rem;">'
    f'<code style="background:rgba(124,58,237,0.1);color:#A78BFA;'
    f'border-radius:4px;padding:0.05rem 0.35rem;font-size:0.78rem;">{label}</code>'
    + (f'<span style="color:#475569;font-size:0.75rem;">{note}</span>' if note else '')
    + '</div>'
)

with col_games:
    st.markdown(f"""
    <div style="
        background: linear-gradient(150deg, #13132A 0%, #1A1A30 100%);
        border: 1px solid rgba(124,58,237,0.18);
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        height: 100%;
    ">
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.9rem;">
            <div style="
                font-size:1.25rem;
                background:rgba(124,58,237,0.15);
                border-radius:8px;padding:0.3rem 0.45rem;
                line-height:1;
            ">🎮</div>
            <div>
                <div style="font-size:0.95rem;font-weight:700;color:#E2E8F0;">
                    Collection <code style="color:#A78BFA;background:rgba(124,58,237,0.12);
                    border-radius:4px;padding:0.1rem 0.4rem;font-size:0.85rem;">games</code>
                </div>
                <div style="font-size:0.72rem;color:#4B5563;margin-top:0.1rem;">
                    Jeux multijoueurs analysés
                </div>
            </div>
        </div>
        {_field_row('_id, title', '— identifiant et titre')}
        {_field_row('developer, genre', '— éditeur et genre')}
        {_field_row('release_date', '— date de sortie')}
        {_field_row('specifications', '— schéma polymorphique (varie par genre)')}
        {_field_row('reviews[ ]', '— tableau imbriqué d\'évaluations')}
        {_field_row('metrics', '— calculé par le script Python')}
    </div>
    """, unsafe_allow_html=True)

with col_players:
    st.markdown(f"""
    <div style="
        background: linear-gradient(150deg, #13132A 0%, #1A1A30 100%);
        border: 1px solid rgba(6,182,212,0.18);
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        height: 100%;
    ">
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.9rem;">
            <div style="
                font-size:1.25rem;
                background:rgba(6,182,212,0.12);
                border-radius:8px;padding:0.3rem 0.45rem;
                line-height:1;
            ">👤</div>
            <div>
                <div style="font-size:0.95rem;font-weight:700;color:#E2E8F0;">
                    Collection <code style="color:#22D3EE;background:rgba(6,182,212,0.1);
                    border-radius:4px;padding:0.1rem 0.4rem;font-size:0.85rem;">players</code>
                </div>
                <div style="font-size:0.72rem;color:#4B5563;margin-top:0.1rem;">
                    Profils joueurs enregistrés
                </div>
            </div>
        </div>
        {_field_row('_id, username', '— identifiant et pseudo')}
        {_field_row('region', '— zone géographique (EUW, NA, MENA…)')}
        {_field_row('join_date', '— date d\'inscription')}
        {_field_row('library[ ]', '— tableau de références par game_id')}
        {_field_row('playtime, status', '— engagement par jeu')}
        {_field_row('skill_level', '— beginner → expert')}
    </div>
    """, unsafe_allow_html=True)
