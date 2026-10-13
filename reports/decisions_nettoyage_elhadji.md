# Journal des décisions de nettoyage

Ce document résume les choix à défendre à l'oral.

| Règle | Pourquoi | Risque / limite |
|---|---|---|
| Supprimer les lignes exactement dupliquées | Elles n'ajoutent aucune information distincte | Supposition que la répétition est accidentelle |
| Résoudre les `customer_id` répétés en conservant la ligne la plus complète | Obtenir une ligne par client | Peut masquer des états successifs; validation métier requise |
| Écarter les lignes sans `customer_id` | Impossible de garantir l'unicité client | Perte de lignes qui pourraient contenir des informations utiles |
| Convertir les champs numériques en nombres | Permet calculs et contrôles | Les formats ambigus deviennent manquants |
| Mettre à manquant les valeurs hors plage | Ne pas traiter une valeur impossible comme fiable | Les seuils sont des hypothèses à faire valider |
| Harmoniser seulement les alias connus | Éviter de fusionner des catégories non équivalentes | Certaines catégories atypiques restent distinctes |
| Corriger les dates impossibles en manquant | Éviter des durées chronologiquement incohérentes | La vraie date ne peut pas être reconstruite |
| Retirer nom et email de la sortie analytique | Minimisation des données identifiantes | Ces champs ne sont pas disponibles pour une analyse de contact |
| Ne pas imputer les manquants | Éviter de fabriquer de l'information sans règle métier | Certaines analyses utilisent moins de lignes |

Pour chaque décision, les fichiers `outputs/diagnostic_colonnes.csv` et `outputs/comparaison_qualite.csv` apportent les éléments quantifiés. Le rapport généré précise les limites et les constats métier.
