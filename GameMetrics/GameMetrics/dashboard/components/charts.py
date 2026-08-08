import plotly.graph_objects as go
from dashboard.utils.styles import CHART_COLORS

_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color="#E2E8F0", size=12),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(
        bgcolor="rgba(22, 22, 42, 0.8)",
        bordercolor="rgba(124, 58, 237, 0.3)",
        borderwidth=1,
    ),
)

_AXIS_STYLE = dict(
    gridcolor="rgba(148, 163, 184, 0.08)",
    linecolor="rgba(148, 163, 184, 0.15)",
    tickfont=dict(color="#94A3B8", size=11),
    title_font=dict(color="#CBD5E1", size=12),
    zerolinecolor="rgba(148, 163, 184, 0.1)",
)


def _apply_layout(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#E2E8F0"), x=0.01),
        **_LAYOUT_BASE,
    )
    return fig


def _safe_max(values, default=1):
    if not values:
        return default
    m = max(values)
    return m if m and m > 0 else default


def _empty_chart(message: str = "Aucune donnée") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=14, color="#64748B"),
    )
    _apply_layout(fig)
    return fig


def chart_games_by_genre(data: list[dict]) -> go.Figure:
    if not data:
        return _empty_chart("Aucune donnée disponible")

    labels = [d.get("genre", "?") for d in data]
    values = [d.get("total_games", 0) or 0 for d in data]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(
                colors=CHART_COLORS[:len(data)],
                line=dict(color="#0F0F1A", width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=12, color="#E2E8F0"),
            hovertemplate="<b>%{label}</b><br>%{value} jeux<br>%{percent}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(text="Jeux par genre", font=dict(size=15, color="#E2E8F0"), x=0.01),
        showlegend=True,
        **_LAYOUT_BASE,
        annotations=[
            dict(
                text=f"<b>{sum(values)}</b><br>jeux",
                x=0.5,
                y=0.5,
                font=dict(size=16, color="#9F67FF"),
                showarrow=False,
            )
        ],
    )
    return fig


def chart_avg_rating(data: list[dict]) -> go.Figure:
    if not data:
        return _empty_chart("Aucune donnée disponible")

    titles = [d.get("title", "?") for d in data]
    ratings = [d.get("avg_rating", 0) or 0 for d in data]
    max_rating = _safe_max(ratings, 1)

    colors = [
        f"rgba(124, 58, 237, {0.4 + 0.6 * (r / max_rating)})"
        for r in ratings
    ]

    fig = go.Figure(
        go.Bar(
            x=ratings,
            y=titles,
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(color="rgba(124, 58, 237, 0.6)", width=1),
            ),
            text=[f"{r:.1f}" for r in ratings],
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=11),
            hovertemplate="<b>%{y}</b><br>Note : %{x:.2f} / 10<extra></extra>",
        )
    )

    fig.update_xaxes(range=[0, 11], **_AXIS_STYLE, title_text="Note moyenne / 10")
    fig.update_yaxes(**_AXIS_STYLE)
    _apply_layout(fig, "Note moyenne par jeu")
    return fig


def chart_positive_ratio(data: list[dict]) -> go.Figure:
    if not data:
        return _empty_chart("Aucune donnée disponible")

    titles = [d.get("title", "?") for d in data]
    ratios = [d.get("positive_ratio_pct", 0) or 0 for d in data]

    def ratio_color(r):
        if r >= 70:
            return "#10B981"
        if r >= 50:
            return "#F59E0B"
        return "#EF4444"

    fig = go.Figure(
        go.Bar(
            x=titles,
            y=ratios,
            marker=dict(
                color=[ratio_color(r) for r in ratios],
                line=dict(color="rgba(255,255,255,0.05)", width=1),
                opacity=0.85,
            ),
            text=[f"{r:.0f}%" for r in ratios],
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=11),
            hovertemplate="<b>%{x}</b><br>Positifs : %{y:.1f}%<extra></extra>",
        )
    )

    fig.update_xaxes(**_AXIS_STYLE)
    fig.update_yaxes(range=[0, 115], **_AXIS_STYLE, title_text="% d'avis recommandés")
    _apply_layout(fig, "Ratio d'avis positifs par jeu")
    return fig


def chart_engagement_score(data: list[dict]) -> go.Figure:
    if not data:
        return _empty_chart("Aucune donnée disponible")

    titles = [d.get("title", "?") for d in data]
    scores = [d.get("engagement_score", 0) or 0 for d in data]

    fig = go.Figure(
        go.Bar(
            x=titles,
            y=scores,
            marker=dict(
                color=scores,
                colorscale=[[0, "#4F46E5"], [0.5, "#7C3AED"], [1, "#06B6D4"]],
                showscale=False,
                line=dict(color="rgba(124, 58, 237, 0.5)", width=1),
            ),
            text=[f"{s:.1f}" for s in scores],
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=11),
            hovertemplate="<b>%{x}</b><br>Engagement : %{y:.2f}<extra></extra>",
        )
    )

    fig.update_xaxes(**_AXIS_STYLE)
    fig.update_yaxes(**_AXIS_STYLE, title_text="Score d'engagement")
    _apply_layout(fig, "Score d'engagement par jeu")
    return fig


def chart_review_count(data: list[dict]) -> go.Figure:
    if not data:
        return _empty_chart("Aucune donnée disponible")

    titles = [d.get("title", "?") for d in data]
    counts = [d.get("review_count", 0) or 0 for d in data]

    fig = go.Figure(
        go.Bar(
            x=titles,
            y=counts,
            marker=dict(
                color=CHART_COLORS[:len(data)],
                line=dict(color="rgba(255,255,255,0.05)", width=1),
                opacity=0.9,
            ),
            text=counts,
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=12),
            hovertemplate="<b>%{x}</b><br>%{y} avis<extra></extra>",
        )
    )

    fig.update_xaxes(**_AXIS_STYLE)
    fig.update_yaxes(**_AXIS_STYLE, title_text="Nombre d'avis")
    _apply_layout(fig, "Nombre d'avis par jeu")
    return fig


def chart_playtime_per_player(data: list[dict]) -> go.Figure:
    if not data:
        return _empty_chart("Aucune donnée disponible")

    usernames = [d.get("username", "?") for d in data]
    playtimes = [d.get("total_playtime", 0) or 0 for d in data]
    hours = [round(p / 60, 1) for p in playtimes]

    fig = go.Figure(
        go.Bar(
            x=hours,
            y=usernames,
            orientation="h",
            marker=dict(
                color=CHART_COLORS[:len(data)],
                line=dict(color="rgba(255,255,255,0.05)", width=1),
            ),
            text=[f"{h}h" for h in hours],
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=11),
            hovertemplate="<b>%{y}</b><br>%{x}h de jeu<br>(%{customdata} min)<extra></extra>",
            customdata=playtimes,
        )
    )

    fig.update_xaxes(**_AXIS_STYLE, title_text="Temps de jeu (heures)")
    fig.update_yaxes(**_AXIS_STYLE)
    _apply_layout(fig, "Temps de jeu total par joueur")
    return fig


def chart_most_uninstalled(data: list[dict]) -> go.Figure:
    if not data:
        return _empty_chart("Aucune désinstallation enregistrée")

    titles = [d.get("title", d.get("game_id", "?")) for d in data]
    counts = [d.get("uninstall_count", 0) or 0 for d in data]
    max_count = _safe_max(counts, 1)

    fig = go.Figure(
        go.Bar(
            x=titles,
            y=counts,
            marker=dict(
                color="#EF4444",
                opacity=[0.5 + 0.5 * (c / max_count) for c in counts],
                line=dict(color="rgba(239, 68, 68, 0.5)", width=1),
            ),
            text=counts,
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=12),
            hovertemplate="<b>%{x}</b><br>%{y} désinstallation(s)<extra></extra>",
        )
    )

    fig.update_xaxes(**_AXIS_STYLE)
    fig.update_yaxes(
        **_AXIS_STYLE,
        title_text="Nombre de désinstallations",
        dtick=1,
    )
    _apply_layout(fig, "Jeux les plus désinstallés")
    return fig


def chart_game_radar(game: dict) -> go.Figure:
    metrics = game.get("metrics", {})
    avg_rating = (metrics.get("avg_rating") or 0) / 10 * 100
    positive_ratio = (metrics.get("positive_ratio") or 0) * 100
    review_count = min((metrics.get("review_count") or 0) * 20, 100)
    engagement = min((metrics.get("engagement_score") or 0), 100)

    categories = ["Note", "Recommandations", "Volume d'avis", "Engagement"]
    values = [avg_rating, positive_ratio, review_count, engagement]

    fig = go.Figure(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(124, 58, 237, 0.2)",
            line=dict(color="#7C3AED", width=2),
            marker=dict(color="#9F67FF", size=6),
            hovertemplate="<b>%{theta}</b><br>%{r:.1f}<extra></extra>",
        )
    )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(148, 163, 184, 0.1)",
                tickfont=dict(color="#64748B", size=9),
                showticklabels=True,
            ),
            angularaxis=dict(
                tickfont=dict(color="#E2E8F0", size=11),
                gridcolor="rgba(148, 163, 184, 0.1)",
                linecolor="rgba(148, 163, 184, 0.2)",
            ),
        ),
        **_LAYOUT_BASE,
        title=dict(
            text=f"Profil — {game.get('title', '')}",
            font=dict(size=14, color="#E2E8F0"),
            x=0.01,
        ),
    )
    return fig