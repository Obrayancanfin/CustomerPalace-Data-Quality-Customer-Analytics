# CustomerPalace — Diagnostic de qualité des données

> Rapport généré automatiquement à partir du fichier source. Date de référence des contrôles temporels : 2026-10-12.

## 1. Synthèse exécutive

Le fichier initial contient **10,000 lignes et 19 colonnes**. Après suppression des doublons exacts, résolution des identifiants clients répétés et exclusion des lignes sans identifiant exploitable, le dataset analytique contient **9,716 lignes et 17 colonnes**.

Le fichier n'est pas directement fiable sans préparation : les colonnes sont importées comme texte, plusieurs champs numériques comportent des valeurs hors plage, des dates sont absentes ou incohérentes, et certaines catégories sont représentées par plusieurs variantes. Les noms et emails sont exclus du dataset analytique afin de limiter les données directement identifiantes.

## 2. Diagnostic initial quantifié

- Doublons de lignes strictement identiques : **250**.
- Lignes appartenant à un groupe où `customer_id` est répété : **533**.
- Identifiants clients manquants : **35**.
- Valeurs manquantes brutes, toutes colonnes confondues : **1,413**.

Le détail colonne par colonne est disponible dans `outputs/diagnostic_colonnes.csv`.

### Validations numériques

| Colonne | Valeurs non numériques | Valeurs hors plage | Règle retenue |
|---|---:|---:|---|
| `age` | 81 | 58 | 18 à 100 ans |
| `annual_income_eur` | 314 | 15 | >= 0 |
| `monthly_spend_eur` | 225 | 18 | >= 0 |
| `tenure_months` | 81 | 18 | >= 0 |
| `satisfaction_score` | 139 | 29 | 0 à 10 |
| `support_tickets_12m` | 49 | 13 | >= 0 |

Les valeurs hors plage sont converties en valeurs manquantes, et non remplacées par une valeur inventée. Les seuils sont des contrôles de plausibilité choisis pour l'analyse; ils ne proviennent pas d'un dictionnaire métier officiel.

### Dates et catégories

- Dates non interprétables : `signup_date` = 781, `last_login` = 610.
- Dates d'inscription postérieures à la date de référence remises à manquant : **0**.
- Dernières connexions antérieures à la date d'inscription remises à manquant : **3**.
- Les variantes reconnues de genre, formule, moyen de paiement, appareil, pays et booléens sont harmonisées. Les valeurs ambiguës ou non reconnues sont conservées pour ne pas supposer une équivalence métier.

## 3. Décisions de préparation et justification

| Problème | Décision | Justification et compromis |
|---|---|---|
| Doublons exacts | Suppression | Une ligne identique n'ajoute pas d'information; le nombre supprimé est mesuré. |
| `customer_id` répété | Conserver la ligne la plus complète par identifiant | Produit une clé unique pour l'analyse. C'est une hypothèse de travail à valider si les lignes représentent des états successifs. |
| Identifiant client absent | Exclure la ligne | Sans clé, il est impossible de garantir l'unicité du client ou de résoudre les doublons de façon fiable. |
| Valeurs numériques invalides | Convertir en manquant | Évite d'inventer une valeur; les analyses de chaque indicateur doivent préciser leur effectif disponible. |
| Variantes de catégories | Harmoniser seulement les alias défendables | Réduit les catégories artificiellement séparées sans fusionner des offres dont l'équivalence n'est pas prouvée. |
| Dates incohérentes | Convertir en manquant | Préserve la ligne tout en empêchant d'utiliser une date chronologiquement impossible. |
| Nom et email | Exclure de la sortie analytique | Principe de minimisation; ces champs ne sont pas nécessaires aux constats agrégés. |

## 4. Évaluation après préparation

La comparaison par colonne se trouve dans `outputs/comparaison_qualite.csv`. Elle permet de vérifier les valeurs manquantes restantes et le nombre de valeurs distinctes après harmonisation. Le fichier `data/processed/customers_clean.csv` est la sortie analytique; le fichier brut est conservé inchangé dans `data/raw/`.

- Valeurs manquantes dans le fichier brut : **1,413**.
- Valeurs manquantes dans le dataset analytique préparé : **3,765**.
- Une augmentation du nombre de valeurs manquantes peut être attendue : les valeurs impossibles ont été invalidées plutôt que laissées comme des nombres apparemment fiables.

## 5. Constats métier

1. **Résiliations observées.** Le taux de churn parmi les lignes dont le libellé est interprétable est de **13.79%**. Il s'agit du taux dans cet export, pas nécessairement du taux réel de l'ensemble de la clientèle.
2. **Différences entre formules.** Parmi les formules comptant au moins 30 clients étiquetés, le taux de churn varie de **10.46%** pour `Premium` à **16.56%** pour `Basic`. Les écarts sont descriptifs et ne prouvent pas que la formule cause la résiliation.
3. **Satisfaction et churn.** Le score moyen de satisfaction est de **6.22/10** chez les clients étiquetés résiliés et de **7.31/10** chez les clients non résiliés, sur les scores disponibles. Cette association doit être vérifiée avec les effectifs et ne démontre pas de causalité.
4. **Tickets de support et churn.** Le nombre moyen de tickets sur 12 mois est de **2.08** pour les clients étiquetés résiliés, contre **1.31** pour les non-résiliés. Le lien peut refléter plusieurs phénomènes et ne suffit pas à conclure à une relation causale.

Les chiffres et tableaux sources sont disponibles dans `outputs/` et les visualisations dans `reports/figures/`. Les constats sont recalculés à chaque exécution.

## 6. Limites et recommandations

- Demander au métier un dictionnaire de données, la définition exacte du churn et le moment où chaque variable est mesurée.
- Valider la règle de dédoublonnage de `customer_id` avec le propriétaire de la donnée.
- Examiner les catégories non reconnues (ex. formules atypiques) avant toute fusion ou exclusion.
- Définir des règles officielles de contrôle, des seuils d'alerte et un suivi périodique de la qualité.
- Avant un modèle prédictif, évaluer les fuites de données, les variables disponibles au moment de la prédiction et la représentativité de l'échantillon.
- Ne pas publier les données brutes ni les données potentiellement identifiantes sur un dépôt public sans autorisation.

## 7. Reproduction

Depuis la racine du dépôt, activer l'environnement Python, installer `requirements.txt`, puis lancer `python src/pipeline.py`. Les fichiers de sortie sont générés dans `data/processed/`, `outputs/` et `reports/`.

## 8. Bonus facultatif : modèle de classification

Le script `src/ml_bonus.py` compare une référence majoritaire à une régression logistique sur un jeu de test séparé. Sur cette exécution, la référence majoritaire obtient une accuracy de 0,8621, mais un rappel de 0,0 pour la classe churn : elle ne détecte aucune résiliation. La régression logistique obtient une accuracy de 0,6521, une précision de 0,2210, un rappel de 0,6030 et un F1-score de 0,3235 sur le jeu de test.

Cette comparaison illustre pourquoi l'accuracy seule est insuffisante lorsque les classes sont déséquilibrées. Ces scores ne démontrent pas que le modèle est prêt pour l'entreprise : la définition de `churned`, la temporalité des variables et leur disponibilité avant résiliation doivent être confirmées. Les résultats reproductibles sont dans `outputs/ml_baseline_metrics.json` et `outputs/ml_confusion_matrix.csv`.
