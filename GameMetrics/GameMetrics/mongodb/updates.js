use("gamemetrics");

print("===== REQUÊTES UPDATE =====");

db.games.updateOne(
  { _id: "game_valorant" },
  {
    $push: {
      reviews: {
        author_id: "player_omar",
        rating: 8,
        recommended: true,
        comment: "Très bon jeu compétitif, agréable à jouer avec des amis.",
        date: "2026-04-21"
      }
    }
  }
);

print("\n1. Avis ajouté à game_valorant.");
printjson(
  db.games.findOne(
    { _id: "game_valorant" },
    { _id: 1, title: 1, reviews: 1 }
  )
);
db.players.updateOne(
  {
    _id: "player_omar",
    "library.game_id": "game_deeprock"
  },
  {
    $set: {
      "library.$.status": "inactive",
      "library.$.last_played": "2026-04-21"
    }
  }
);

print("\n2. Statut modifié dans la bibliothèque de player_omar.");
printjson(
  db.players.findOne(
    { _id: "player_omar" },
    { _id: 1, username: 1, library: 1 }
  )
);

db.players.updateOne(
  {
    _id: "player_yanis",
    "library.game_id": "game_valorant"
  },
  {
    $inc: {
      "library.$.playtime": 15
    }
  }
);

print("\n3. Temps de jeu de player_yanis augmenté sur Valorant.");
printjson(
  db.players.findOne(
    { _id: "player_yanis" },
    { _id: 1, username: 1, library: 1 }
  )
);
db.players.updateOne(
  { _id: "player_sara" },
  {
    $set: { region: "NA-East" }
  }
);

print("\n4. Région de player_sara mise à jour.");
printjson(
  db.players.findOne(
    { _id: "player_sara" },
    { _id: 1, username: 1, region: 1 }
  )
);
db.games.updateOne(
  { _id: "game_ffxiv" },
  {
    $set: { "metrics.review_count": 2 }
  }
);

print("\n5. metrics.review_count mis à jour pour game_ffxiv.");
printjson(
  db.games.findOne(
    { _id: "game_ffxiv" },
    { _id: 1, title: 1, metrics: 1 }
  )
);