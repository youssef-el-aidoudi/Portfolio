

import streamlit as st
from dashboard.db_utils import get_db, check_connection
from dashboard.utils.styles import inject_css, section_title, divider

st.set_page_config(
    page_title="À Propos — GameMetrics",
    page_icon="📖",
    layout="wide",
)
inject_css()
st.markdown('<style>[data-testid="stSidebarNav"],[data-testid="stSidebarNavItems"]{display:none!important;}</style>', unsafe_allow_html=True)

ok, msg = check_connection()
if not ok:
    st.warning(f"⚠️ MongoDB non connectée : {msg}")
db = get_db() if ok else None


st.markdown(
    """
    <div class="page-header">
        <h1>📖 À Propos</h1>
        <p>
            Documentation technique et académique du projet GameMetrics — Master 1.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


section_title("🎓", "Contexte académique")

st.markdown("""
**GameMetrics** est un projet de Master 1 dont l'objectif est de concevoir et exploiter
une base de données MongoDB pour analyser l'engagement des joueurs et les évaluations
de la communauté sur les jeux multijoueurs populaires.

| Aspect | Détail |
|---|---|
| **Cours** | Bases de données NoSQL |
| **Niveau** | Master 1 |
| **Base de données** | MongoDB (locale) |
| **Collections** | `games`, `players` |
| **Script Python** | pymongo — recalcul des métriques |
| **Dashboard** | Streamlit + Plotly |
""")

divider()


section_title("🏗️", "Architecture du dashboard")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
**Arborescence**

```
GameMetrics/
├── app.py                   ← Point d'entrée
├── pages/
│   ├── 1_Jeux.py
│   ├── 2_Joueurs.py
│   ├── 3_Analyses.py
│   ├── 4_Insights.py
│   └── 5_A_Propos.py
├── dashboard/
│   ├── db_utils.py          ← Connexion MongoDB
│   ├── services/            ← Logique métier
│   │   ├── game_service.py
│   │   ├── player_service.py
│   │   ├── analytics_service.py
│   │   └── metrics_updater.py
│   ├── components/          ← UI réutilisable
│   │   ├── kpi_cards.py
│   │   └── charts.py
│   └── utils/
│       ├── formatters.py
│       └── styles.py
├── .streamlit/config.toml
├── .env
└── requirements.txt
```
    """)

with col2:
    st.markdown("""
**Principes architecturaux**

- **Séparation des responsabilités** : chaque couche a un rôle unique
- **Cache Streamlit** : `@st.cache_resource` pour la connexion MongoDB,
  `@st.cache_data(ttl=60)` pour les requêtes fréquentes
- **Zéro duplication** : `metrics_updater.py` appelle directement
  `python/update_game_metrics.py` en subprocess
- **Robustesse** : gestion des clés absentes (schéma polymorphique),
  base vide, timeout MongoDB
- **Sécurité** : URI MongoDB dans `.env`, jamais codée en dur

**Flux de données**
```
MongoDB ──→ services/ ──→ pages/
               │
               └──→ components/ ──→ Streamlit UI
```
    """)

divider()


section_title("🎮", "Schéma de la collection games")

st.markdown("""
```json
{
  "_id": "game_valorant",
  "title": "Valorant",
  "developer": "Riot Games",
  "release_date": "2020-06-02",
  "genre": "FPS",

  "specifications": {              // ← Schéma polymorphique
    "business_model": "Free-to-play",
    "team_format": "5v5",
    "ranked_mode": true,
    "anti_cheat": "Vanguard"
    // ... champs variables selon le genre
  },

  "reviews": [                     // ← Document imbriqué
    {
      "author_id": "player_yanis",
      "rating": 9,
      "recommended": true,
      "comment": "Excellent jeu compétitif...",
      "date": "2026-04-10"
    }
  ],

  "metrics": {                     // ← Calculé par Python
    "avg_rating": 7.75,
    "positive_ratio": 0.75,
    "review_count": 4,
    "engagement_score": 84.32
  }
}
```
""")

st.info("""
**Schéma polymorphique** : le champ `specifications` varie selon le genre du jeu.
Un FPS aura `weapon_categories` et `anti_cheat`, un MMORPG aura `classes` et `raid_size`.
MongoDB permet cette flexibilité nativement, contrairement aux bases relationnelles.
""")

divider()


section_title("👤", "Schéma de la collection players")

st.markdown("""
```json
{
  "_id": "player_yanis",
  "username": "YanisDZ",
  "region": "EUW",
  "join_date": "2024-09-15",

  "library": [                     // ← Référence par game_id
    {
      "game_id": "game_valorant",  // référence vers games._id
      "playtime": 420,             // en minutes
      "status": "active",          // active | inactive | uninstalled
      "last_played": "2026-04-20",
      "skill_level": "advanced"    // beginner | intermediate | advanced | expert
    }
  ]
}
```
""")

st.info("""
**Références croisées** : `library[].game_id` est une référence manuelle vers `games._id`.
Ce choix évite la duplication des données du jeu dans chaque joueur tout en permettant
des jointures via `$lookup` dans les pipelines d'agrégation.
""")

divider()


section_title("🔢", "Formule d'engagement")

st.markdown("""
Le `engagement_score` est calculé par `python/update_game_metrics.py` :

```python
engagement_score = round(
    (avg_rating       * 0.4) +   # Qualité perçue (note /10)
    (positive_ratio   * 100 * 0.3) +   # Satisfaction communautaire
    (avg_playtime     * 0.3),    # Temps de jeu moyen (minutes)
    2
)
```

| Facteur | Poids | Source |
|---|---|---|
| `avg_rating` | 40% | Moyenne des `reviews[].rating` |
| `positive_ratio` | 30% | % d'avis `recommended: true` |
| `avg_playtime` | 30% | Moyenne de `library[].playtime` par jeu |

Le recalcul peut être déclenché depuis la **sidebar de l'accueil** (bouton "Recalculer les métriques").
""")

divider()


section_title("⚙️", "Scripts MongoDB")

st.markdown("""
| Fichier | Rôle |
|---|---|
| `mongodb/insert_data.js` | Insertion des 5 jeux et 5 joueurs |
| `mongodb/queries_find.js` | Requêtes `find()` de base |
| `mongodb/queries_aggregate.js` | 8 pipelines d'agrégation |
| `mongodb/updates.js` | Exemples de `updateOne()` |
| `python/update_game_metrics.py` | Recalcul des métriques via pymongo |

**Lancer les scripts MongoDB Shell** :
```bash
mongosh gamemetrics mongodb/insert_data.js
mongosh gamemetrics mongodb/queries_find.js
mongosh gamemetrics mongodb/queries_aggregate.js
```
""")

divider()


section_title("🔌", "Statut de la connexion")

if ok and db is not None:
    try:
        stats = db.command("dbStats")
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("Base de données", db.name)
        col_s2.metric("Collections", stats.get("collections", "N/A"))
        col_s3.metric("Documents",   stats.get("objects", "N/A"))
        col_s4.metric("Taille",      f"{stats.get('dataSize', 0) / 1024:.1f} KB")
        st.success(f"✅ {msg}")
    except Exception as e:
        st.warning(f"Connexion établie mais statut indisponible : {e}")
else:
    st.error(f"❌ {msg}")
