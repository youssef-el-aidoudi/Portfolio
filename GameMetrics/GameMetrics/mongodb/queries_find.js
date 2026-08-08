use("gamemetrics");

print("===== REQUÊTES FIND =====");
print("\n1. Jeux de genre FPS :");
printjson(
  db.games.find(
    { genre: "FPS" },
    { _id: 1, title: 1, genre: 1 }
  ).toArray()
);
print("\n2. Jeux avec mode classé :");
printjson(
  db.games.find(
    { "specifications.ranked_mode": true },
    { _id: 1, title: 1, "specifications.ranked_mode": 1 }
  ).toArray()
);
print("\n3. Jeux ayant au moins un avis négatif :");
printjson(
  db.games.find(
    { "reviews.recommended": false },
    { _id: 1, title: 1, reviews: 1 }
  ).toArray()
);
print("\n4. Joueurs ayant au moins un jeu désinstallé :");
printjson(
  db.players.find(
    { "library.status": "uninstalled" },
    { _id: 1, username: 1, library: 1 }
  ).toArray()
);
print("\n5. Joueurs de la région EUW :");
printjson(
  db.players.find(
    { region: "EUW" },
    { _id: 1, username: 1, region: 1 }
  ).toArray()
);
print("\n6. Jeux free-to-play :");
printjson(
  db.games.find(
    { "specifications.business_model": "Free-to-play" },
    { _id: 1, title: 1, "specifications.business_model": 1 }
  ).toArray()
);
print("\n7. Joueurs ayant plus de 2 jeux :");
printjson(
  db.players.find(
    { "library.2": { $exists: true } },
    { _id: 1, username: 1, library: 1 }
  ).toArray()
);
print("\n8. Jeux sortis après 2015 :");
printjson(
  db.games.find(
    { release_date: { $gt: "2015-12-31" } },
    { _id: 1, title: 1, release_date: 1 }
  ).sort({ release_date: 1 }).toArray()
);