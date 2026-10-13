# Oral 5 minutes

** Sujet.** CustomerPalace veut savoir si son export clients permet de calculer des indicateurs fiables. Nous avons uniquement utilisé NumPy, Pandas et Matplotlib.

** Diagnostic.** Il y avait 10 000 lignes et 19 colonnes, 250 doublons stricts, plusieurs façons d'écrire les mêmes catégories et des nombres/dates mal formatés. Ces anomalies risquent de fausser les analyses.

** Choix.** Nous avons utilisé `drop_duplicates()` pour ne retirer que les copies exactes. Avec `str.strip()`, `str.lower()` et `replace()`, nous avons harmonisé les catégories sûres. Avec `pd.to_numeric(errors='coerce')`, nous avons converti les unités connues et mis en `NaN` les valeurs impossibles, sans calculer des moyennes artificielles. Nous avons interprété uniquement des formats de date explicites avec `pd.to_datetime()`. Nous avons conservé les extrêmes plausibles et retiré les données directement identifiantes du CSV final.

** Preuve.** Le jeu nettoyé comporte 9 750 lignes. Nous avons comparé la part de valeurs convertibles avant/après **sur les mêmes lignes**, et sauvegardé le tableau et le graphique. Le but n'était pas de remplir artificiellement toutes les cases.

** Métier.** Nous avons calculé le churn en faisant la moyenne de la variable `churned` convertie en 0/1, puis étudié ce taux par formule, appareil et satisfaction. Les tableaux affichent aussi les effectifs, pour interpréter prudemment les petits groupes.

** Conclusion.** Les données conviennent mieux à l'analyse descriptive, à condition d'expliquer les transformations. Nous n'avons ni dictionnaire officiel, ni date de résiliation, donc nous ne démontrons pas de causalité et ne recommandons pas de décisions automatiques sans vérification supplémentaire.
