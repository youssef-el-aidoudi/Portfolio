import streamlit as st
_PRIMARY   = "#7C3AED"
_PRIMARY_V = "#A78BFA"   # violet clair pour la valeur principale
_GRAD_TOP  = "linear-gradient(90deg, #7C3AED 0%, #06B6D4 100%)"
_BG_CARD   = "linear-gradient(150deg, #15152A 0%, #1C1C36 100%)"
_BORDER    = "rgba(124, 58, 237, 0.22)"
_TEXT      = "#E2E8F0"
_MUTED     = "#94A3B8"
_DIM       = "#475569"
_ACCENT    = "#7C3AED"   # sublabel — violet discret


def _kpi_html(icon: str, value: str, label: str, sublabel: str = "") -> str:
    """
    Carte KPI en HTML inline.
    - Valeur principale : plus grande, plus impactante
    - Label : uppercase compact en muted
    - Sublabel : accent violet discret pour la sous-info
    """
    # Taille dynamique selon longueur de la valeur
    if len(value) > 14:
        val_size   = "1.15rem"
        val_weight = "700"
    elif len(value) > 8:
        val_size   = "1.6rem"
        val_weight = "800"
    else:
        val_size   = "2.4rem"
        val_weight = "800"

    sub_block = (
        f'<p style="'
        f'margin:0.22rem 0 0;'
        f'font-size:0.7rem;'
        f'color:{_ACCENT};'
        f'font-weight:600;'
        f'letter-spacing:0.01em;'
        f'">{sublabel}</p>'
        if sublabel else ""
    )

    return f"""
    <div style="
        background: {_BG_CARD};
        border: 1px solid {_BORDER};
        border-radius: 13px;
        padding: 1.25rem 0.9rem 1.1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        min-height: 122px;
        box-sizing: border-box;
    ">
        <div style="
            position: absolute; top: 0; left: 0; right: 0; height: 2px;
            background: {_GRAD_TOP};
        "></div>
        <p style="margin:0 0 0.28rem; font-size:1.75rem; line-height:1;">{icon}</p>
        <p style="
            margin: 0 0 0.05rem;
            font-size: {val_size};
            font-weight: {val_weight};
            color: {_PRIMARY_V};
            line-height: 1.15;
            letter-spacing: -0.025em;
            word-break: break-word;
        ">{value}</p>
        <p style="
            margin: 0.28rem 0 0;
            font-size: 0.66rem;
            color: {_MUTED};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.09em;
        ">{label}</p>
        {sub_block}
    </div>"""


def kpi_row(cards: list[tuple]) -> None:
    """
    Affiche N cartes KPI côte à côte (st.columns natif Streamlit).
    Chaque card : (icon, value, label) ou (icon, value, label, sublabel).
    """
    cols = st.columns(len(cards), gap="medium")
    for col, card in zip(cols, cards):
        col.markdown(
            _kpi_html(
                icon     = card[0],
                value    = str(card[1]),
                label    = card[2],
                sublabel = card[3] if len(card) > 3 else "",
            ),
            unsafe_allow_html=True,
        )


def insight_card(icon: str, category: str, value: str, detail: str = "") -> None:
    """
    Carte d'insight — bordure gauche violette, inline styles.
    Utilisée sur la page Insights.
    """
    detail_block = (
        f'<p style="margin:0.12rem 0 0;font-size:0.81rem;color:{_MUTED};line-height:1.5;">'
        f'{detail}</p>'
        if detail else ""
    )
    st.markdown(f"""
    <div style="
        background: {_BG_CARD};
        border: 1px solid rgba(124,58,237,0.18);
        border-left: 3px solid {_PRIMARY};
        border-radius: 10px;
        padding: 1rem 1.3rem;
        margin: 0.4rem 0;
    ">
        <p style="
            margin: 0 0 0.22rem;
            font-size: 0.72rem;
            font-weight: 700;
            color: {_ACCENT};
            text-transform: uppercase;
            letter-spacing: 0.09em;
        ">{icon} {category}</p>
        <p style="
            margin: 0;
            font-size: 1.08rem;
            font-weight: 700;
            color: {_TEXT};
            line-height: 1.3;
        ">{value}</p>
        {detail_block}
    </div>""", unsafe_allow_html=True)
