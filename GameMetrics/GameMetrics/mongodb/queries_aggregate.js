use("gamemetrics");

print("===== REQUÊTES AGGREGATE =====");

/*
1) Nombre de jeux par genre
*/
print("\n1. Nombre de jeux par genre :");
printjson(
  db.games.aggregate([
    {
      $group: {
        _id: "$genre",
        total_games: { $sum: 1 }
      }
    },
    {
      $sort: { total_games: -1 }
    }
  ]).toArray()
);

/*
2) Ratio d'avis recommandés par jeu
*/
print("\n2. Ratio d'avis recommandés par jeu :");
printjson(
  db.games.aggregate([
    { $unwind: "$reviews" },
    {
      $group: {
        _id: "$title",
        total_reviews: { $sum: 1 },
        recommended_count: {
          $sum: {
            $cond: [{ $eq: ["$reviews.recommended", true] }, 1, 0]
          }
        }
      }
    },
    {
      $project: {
        _id: 0,
        title: "$_id",
        total_reviews: 1,
        recommended_count: 1,
        positive_ratio_percent: {
          $multiply: [
            { $divide: ["$recommended_count", "$total_reviews"] },
            100
          ]
        }
      }
    },
    {
      $sort: { positive_ratio_percent: -1 }
    }
  ]).toArray()
);

/*
3) Jeux avec le plus d'avis
*/
print("\n3. Jeux avec le plus d'avis :");
printjson(
  db.games.aggregate([
    {
      $project: {
        _id: 0,
        title: 1,
        review_count: { $size: "$reviews" }
      }
    },
    {
      $sort: { review_count: -1 }
    }
  ]).toArray()
);

/*
4) Temps de jeu total par joueur
*/
print("\n4. Temps de jeu total par joueur :");
printjson(
  db.players.aggregate([
    { $unwind: "$library" },
    {
      $group: {
        _id: "$username",
        total_playtime: { $sum: "$library.playtime" }
      }
    },
    {
      $sort: { total_playtime: -1 }
    }
  ]).toArray()
);

/*
5) Jeux les plus désinstallés
*/
print("\n5. Jeux les plus désinstallés :");
printjson(
  db.players.aggregate([
    { $unwind: "$library" },
    { $match: { "library.status": "uninstalled" } },
    {
      $group: {
        _id: "$library.game_id",
        uninstall_count: { $sum: 1 }
      }
    },
    {
      $sort: { uninstall_count: -1 }
    }
  ]).toArray()
);

/*
6) Temps de jeu moyen par jeu
*/
print("\n6. Temps de jeu moyen par jeu :");
printjson(
  db.players.aggregate([
    { $unwind: "$library" },
    {
      $group: {
        _id: "$library.game_id",
        avg_playtime: { $avg: "$library.playtime" },
        player_count: { $sum: 1 }
      }
    },
    {
      $sort: { avg_playtime: -1 }
    }
  ]).toArray()
);

/*
7) Joueurs hardcore (plus de 500h cumulées)
*/
print("\n7. Joueurs hardcore :");
printjson(
  db.players.aggregate([
    { $unwind: "$library" },
    {
      $group: {
        _id: "$username",
        total_playtime: { $sum: "$library.playtime" },
        games_owned: { $sum: 1 }
      }
    },
    {
      $match: { total_playtime: { $gt: 500 } }
    },
    {
      $sort: { total_playtime: -1 }
    }
  ]).toArray()
);

/*
8) Nombre d'avis par auteur
*/
print("\n8. Nombre d'avis par auteur :");
printjson(
  db.games.aggregate([
    { $unwind: "$reviews" },
    {
      $group: {
        _id: "$reviews.author_id",
        total_reviews_written: { $sum: 1 }
      }
    },
    {
      $sort: { total_reviews_written: -1 }
    }
  ]).toArray()
);