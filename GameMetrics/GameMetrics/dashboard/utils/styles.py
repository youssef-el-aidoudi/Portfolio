import streamlit as st

# Palette de couleurs cohérente avec config.toml
COLORS = {
    "primary": "#7C3AED",
    "primary_light": "#9F67FF",
    "secondary": "#4F46E5",
    "accent": "#06B6D4",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "bg": "#0F0F1A",
    "bg_secondary": "#16162A",
    "bg_card": "#1E1E3A",
    "text": "#E2E8F0",
    "text_muted": "#94A3B8",
    "border": "rgba(124, 58, 237, 0.25)",
    "border_hover": "rgba(124, 58, 237, 0.6)",
}

# Séquence de couleurs pour les graphiques Plotly
CHART_COLORS = [
    "#7C3AED", "#06B6D4", "#10B981", "#F59E0B",
    "#EF4444", "#EC4899", "#4F46E5", "#8B5CF6",
]


_CSS_CONTENT = (
    # Page header — utilisé dans toutes les pages secondaires (1_Jeux … 5_A_Propos)
    ".page-header {"
    "background:linear-gradient(135deg,#16162A 0%,#1E1E3A 60%,#0F0F1A 100%);"
    "border:1px solid rgba(124,58,237,0.2);border-radius:16px;"
    "padding:2rem 2.5rem;margin-bottom:2rem;position:relative;overflow:hidden;}"

    ".page-header::after{content:'';"
    "position:absolute;top:-60px;right:-60px;width:200px;height:200px;"
    "background:radial-gradient(circle,rgba(124,58,237,0.12) 0%,transparent 70%);"
    "border-radius:50%;}"

    ".page-header h1{"
    "font-size:2.4rem;font-weight:800;"
    "background:linear-gradient(135deg,#E2E8F0,#9F67FF);"
    "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
    "background-clip:text;margin:0 0 0.5rem 0;letter-spacing:-0.03em;}"

    ".page-header p{color:#94A3B8;font-size:1.05rem;margin:0;max-width:600px;}"

    # Review cards — utilisées dans 1_Jeux.py et 2_Joueurs.py
    ".review-card{background:#16162A;"
    "border:1px solid rgba(124,58,237,0.15);border-radius:10px;"
    "padding:1rem 1.2rem;margin:0.5rem 0;}"

    ".review-header{display:flex;justify-content:space-between;"
    "align-items:center;margin-bottom:0.5rem;}"

    ".review-author{font-weight:600;color:#E2E8F0;font-size:0.9rem;}"
    ".review-rating{font-weight:700;color:#7C3AED;font-size:1rem;}"

    ".review-comment{color:#94A3B8;font-size:0.85rem;"
    "font-style:italic;line-height:1.5;}"

    ".review-date{font-size:0.75rem;color:#475569;margin-top:0.4rem;}"

    # Navigation Streamlit automatique — masquée (navigation custom dans la sidebar)
    "[data-testid='stSidebarNav'],"
    "[data-testid='stSidebarNavItems'],"
    "[data-testid='stSidebarNavSeparator']{display:none!important;}"

    # Scrollbar
    "::-webkit-scrollbar{width:6px;height:6px;}"
    "::-webkit-scrollbar-track{background:#0F0F1A;}"
    "::-webkit-scrollbar-thumb{background:rgba(124,58,237,0.4);border-radius:3px;}"
    "::-webkit-scrollbar-thumb:hover{background:rgba(124,58,237,0.7);}"
)


def inject_css() -> None:
    """Injecte le CSS global GameMetrics dans la page courante.

    - Google Fonts via <link> (évite les problèmes d'@import dans st.markdown)
    - CSS classes via <style> construit sans saut de ligne initial pour que
      le parser Markdown de Streamlit 1.56 reconnaisse correctement le bloc HTML.
    """
    # Google Fonts — tag <link> séparé, plus fiable qu'@import CSS
    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter'
        ':wght@300;400;500;600;700;800&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    # CSS global — commence directement par <style> (pas de \n initial)
    st.markdown(
        "<style>" + _CSS_CONTENT + "</style>",
        unsafe_allow_html=True,
    )


def section_title(icon: str, title: str) -> None:
    """
    Affiche un titre de section avec style cohérent.
    Utilise des inline styles pour garantir le rendu indépendamment
    de l'injection CSS (plus fiable sous Streamlit 1.36+).
    """
    st.markdown(
        f'<div style="'
        f'font-size:1.35rem;font-weight:700;color:#E2E8F0;'
        f'margin:1.5rem 0 0.8rem 0;padding-bottom:0.5rem;'
        f'border-bottom:2px solid rgba(124,58,237,0.3);">'
        f'{icon}&nbsp;{title}</div>',
        unsafe_allow_html=True,
    )


def divider() -> None:
    """Affiche un diviseur décoratif avec gradient violet."""
    st.markdown(
        '<hr style="height:1px;border:none;'
        'background:linear-gradient(90deg,transparent,rgba(124,58,237,0.4),transparent);'
        'margin:1.5rem 0;">',
        unsafe_allow_html=True,
    )
