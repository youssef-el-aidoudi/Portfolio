# Dataset utilisé



Le dataset utilisé dans ce projet peut être téléchargé ici :

https://www.kaggle.com/datasets/localbrain/bottles

Le dataset peut aussi être enrichi en ajoutant des images prises avec une caméra ou un smartphone
---

# Organisation du dataset

Après téléchargement, les images doivent être organisées avec la structure suivante :

dataset_qc/

train/
- conforme/
- non_conforme/

val/
- conforme/
- non_conforme/

test/
- conforme/
- non_conforme/

---

# Remarque

Les images du dataset ont été réorganisées pour créer un problème de classification binaire :

- **conforme**
- **non_conforme**
