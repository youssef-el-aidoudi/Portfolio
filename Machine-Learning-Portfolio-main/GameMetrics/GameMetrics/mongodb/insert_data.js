use("ye855175");

db.games.deleteMany({});
db.players.deleteMany({});

db.games.insertMany([
  {
    _id: "game_valorant",
    title: "Valorant",
    developer: "Riot Games",
    release_date: "2020-06-02",
    genre: "FPS",
    specifications: {
      subgenre: "Hero Shooter",
      platforms: ["PC"],
      business_model: "Free-to-play",
      team_format: "5v5",
      perspective: "First-person",
      ranked_mode: true,
      voice_chat: true,
      anti_cheat: "Vanguard",
      main_modes: ["Unrated", "Competitive", "Deathmatch", "Spike Rush"],
      weapon_categories: ["Pistols", "SMGs", "Rifles", "Sniper Rifles", "Shotguns"],
      avg_match_duration_min: 35,
      play_style: "Tactical",
      competitive_scene: true
    },
    reviews: [
      {
        author_id: "player_yanis",
        rating: 9,
        recommended: true,
        comment: "Excellent jeu compétitif, gameplay précis et bonne variété d'agents.",
        date: "2026-04-10"
      },
      {
        author_id: "player_lina",
        rating: 8,
        recommended: true,
        comment: "Très bon FPS tactique, mais le matchmaking peut parfois être frustrant.",
        date: "2026-04-12"
      },
      {
        author_id: "player_nabil",
        rating: 6,
        recommended: false,
        comment: "Le jeu est solide, mais la communauté devient parfois être toxique.",
        date: "2026-04-18"
      }
    ],
    metrics: {
      avg_rating: 0,
      positive_ratio: 0,
      review_count: 0,
      engagement_score: 0
    }
  },
  {
    _id: "game_overwatch2",
    title: "Overwatch 2",
    developer: "Blizzard Entertainment",
    release_date: "2022-10-04",
    genre: "FPS",
    specifications: {
      subgenre: "Hero Shooter",
      platforms: ["PC", "PS5", "Xbox Series"],
      business_model: "Free-to-play",
      team_format: "5v5",
      perspective: "First-person",
      ranked_mode: true,
      voice_chat: true,
      anti_cheat: "Defense Matrix",
      main_modes: ["Quick Play", "Competitive", "Arcade"],
      hero_roles: ["Tank", "Damage", "Support"],
      avg_match_duration_min: 18,
      play_style: "Fast-paced",
      competitive_scene: true
    },
    reviews: [
      {
        author_id: "player_yanis",
        rating: 5,
        recommended: false,
        comment: "Le gameplay reste fun, mais beaucoup de contenu semble moins généreux qu'avant.",
        date: "2026-04-09"
      },
      {
        author_id: "player_sara",
        rating: 4,
        recommended: false,
        comment: "Bon visuellement, mais j'ai fini par désinstaller après peu de temps.",
        date: "2026-04-14"
      }
    ],
    metrics: {
      avg_rating: 0,
      positive_ratio: 0,
      review_count: 0,
      engagement_score: 0
    }
  },
  {
    _id: "game_lol",
    title: "League of Legends",
    developer: "Riot Games",
    release_date: "2009-10-27",
    genre: "MOBA",
    specifications: {
      subgenre: "Competitive Arena",
      platforms: ["PC"],
      business_model: "Free-to-play",
      team_format: "5v5",
      perspective: "Top-down",
      ranked_mode: true,
      voice_chat: false,
      champion_count: 160,
      avg_match_duration_min: 32,
      map_name: "Summoner's Rift",
      play_style: "Strategic",
      competitive_scene: true
    },
    reviews: [
      {
        author_id: "player_yanis",
        rating: 7,
        recommended: true,
        comment: "Très profond stratégiquement, mais demande beaucoup d'investissement.",
        date: "2026-04-08"
      },
      {
        author_id: "player_nabil",
        rating: 8,
        recommended: true,
        comment: "Toujours un des meilleurs jeux compétitifs à long terme.",
        date: "2026-04-16"
      }
    ],
    metrics: {
      avg_rating: 0,
      positive_ratio: 0,
      review_count: 0,
      engagement_score: 0
    }
  },
  {
    _id: "game_ffxiv",
    title: "Final Fantasy XIV",
    developer: "Square Enix",
    release_date: "2013-08-27",
    genre: "MMORPG",
    specifications: {
      subgenre: "Fantasy MMORPG",
      platforms: ["PC", "PS5"],
      business_model: "Subscription",
      perspective: "Third-person",
      cross_platform: true,
      classes: ["Paladin", "White Mage", "Black Mage", "Dragoon", "Scholar"],
      raid_size: 8,
      guild_system: true,
      trading_system: true,
      role_system: ["Tank", "Healer", "DPS"],
      avg_session_duration_min: 90,
      play_style: "Cooperative",
      competitive_scene: false
    },
    reviews: [
      {
        author_id: "player_lina",
        rating: 9,
        recommended: true,
        comment: "Excellent MMORPG avec une communauté très accueillante.",
        date: "2026-04-11"
      },
      {
        author_id: "player_sara",
        rating: 10,
        recommended: true,
        comment: "Très riche en contenu et superbe narration.",
        date: "2026-04-19"
      }
    ],
    metrics: {
      avg_rating: 0,
      positive_ratio: 0,
      review_count: 0,
      engagement_score: 0
    }
  },
  {
    _id: "game_deeprock",
    title: "Deep Rock Galactic",
    developer: "Ghost Ship Games",
    release_date: "2020-05-13",
    genre: "Co-op Shooter",
    specifications: {
      subgenre: "Cooperative PvE",
      platforms: ["PC", "PS5", "Xbox Series"],
      business_model: "Paid",
      team_format: "4-player co-op",
      perspective: "First-person",
      class_system: ["Driller", "Engineer", "Gunner", "Scout"],
      procedural_generation: true,
      voice_chat: true,
      avg_mission_duration_min: 28,
      play_style: "Cooperative",
      competitive_scene: false
    },
    reviews: [
      {
        author_id: "player_nabil",
        rating: 9,
        recommended: true,
        comment: "Super jeu coopératif, très fun entre amis.",
        date: "2026-04-13"
      }
    ],
    metrics: {
      avg_rating: 0,
      positive_ratio: 0,
      review_count: 0,
      engagement_score: 0
    }
  }
]);

db.players.insertMany([
  {
    _id: "player_yanis",
    username: "YanisDZ",
    region: "EUW",
    join_date: "2024-09-15",
    library: [
      {
        game_id: "game_valorant",
        playtime: 420,
        status: "active",
        last_played: "2026-04-20",
        skill_level: "advanced"
      },
      {
        game_id: "game_lol",
        playtime: 310,
        status: "active",
        last_played: "2026-04-17",
        skill_level: "intermediate"
      },
      {
        game_id: "game_overwatch2",
        playtime: 85,
        status: "uninstalled",
        last_played: "2026-03-02",
        skill_level: "beginner"
      }
    ]
  },
  {
    _id: "player_lina",
    username: "LinaFR",
    region: "EUW",
    join_date: "2025-01-10",
    library: [
      {
        game_id: "game_valorant",
        playtime: 160,
        status: "active",
        last_played: "2026-04-19",
        skill_level: "intermediate"
      },
      {
        game_id: "game_ffxiv",
        playtime: 540,
        status: "active",
        last_played: "2026-04-20",
        skill_level: "advanced"
      }
    ]
  },
  {
    _id: "player_nabil",
    username: "NabilX",
    region: "EUW",
    join_date: "2023-11-21",
    library: [
      {
        game_id: "game_lol",
        playtime: 690,
        status: "active",
        last_played: "2026-04-18",
        skill_level: "advanced"
      },
      {
        game_id: "game_valorant",
        playtime: 140,
        status: "inactive",
        last_played: "2026-02-26",
        skill_level: "intermediate"
      },
      {
        game_id: "game_deeprock",
        playtime: 95,
        status: "active",
        last_played: "2026-04-13",
        skill_level: "beginner"
      }
    ]
  },
  {
    _id: "player_sara",
    username: "SaraNova",
    region: "NA",
    join_date: "2025-06-03",
    library: [
      {
        game_id: "game_overwatch2",
        playtime: 42,
        status: "uninstalled",
        last_played: "2026-03-01",
        skill_level: "beginner"
      },
      {
        game_id: "game_ffxiv",
        playtime: 610,
        status: "active",
        last_played: "2026-04-20",
        skill_level: "expert"
      }
    ]
  },
  {
    _id: "player_omar",
    username: "OmarPlay",
    region: "MENA",
    join_date: "2024-05-28",
    library: [
      {
        game_id: "game_valorant",
        playtime: 260,
        status: "active",
        last_played: "2026-04-18",
        skill_level: "intermediate"
      },
      {
        game_id: "game_deeprock",
        playtime: 210,
        status: "active",
        last_played: "2026-04-16",
        skill_level: "intermediate"
      }
    ]
  }
]);

print("Données insérées avec succès dans gamemetrics.");