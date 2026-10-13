# Rapport d'analyse — CustomerPalace (version simple)

## Problématique
Le jeu de données est-il exploitable pour des analyses clients ?

## Diagnostic
- Dataset initial : **10000 lignes et 19 colonnes**.
- Doublons stricts retirés : **250**.
- Après nettoyage : **9750 lignes et 16 colonnes**.
- Problèmes observés : catégories écrites de plusieurs façons, dates hétérogènes,
  nombres contenant des unités, valeurs absentes et valeurs hors plage.

## Choix et justifications
1. **Doublons :** supprimer seulement les lignes entièrement identiques ; ne pas dédupliquer sur nom/email.
2. **Catégories :** uniformiser les synonymes manifestes ; garder les formules inhabituelles distinctes.
3. **Nombres :** convertir les unités explicites, puis mettre en NA les valeurs impossibles selon nos bornes.
4. **Dates :** accepter uniquement des formats connus ; date impossible = NaT.
5. **Valeurs extrêmes :** ne pas supprimer un revenu élevé sans preuve d'erreur.
6. **Confidentialité :** ne pas exporter ID, nom et email dans le jeu analytique.

## Effet mesuré
- Lignes retirées : **250**.
- Libellés distincts d'abonnement : **17 avant**, **7 après** harmonisation.
- Dates d'inscription convertibles avant (ISO uniquement) : **91.98 %**.
- Dates d'inscription convertibles après : **99.41 %**.
- Nombre d'anomalies numériques rendues manquantes : **133**.
- Connexions antérieures à l'inscription invalidées : **3**.

Les taux avant/après sont comparés sur les mêmes 9750 lignes dédupliquées.
Ils mesurent la proportion de valeurs **convertibles**, pas une exactitude vérifiée.
Tableau détaillé : `reports/comparaison_qualite.csv`.

## Trois constats métier
- Taux global de churn observé : **13.79 %**.
- **Formules :** Basic = **16.52 %** (n=4020),
  contre Premium = **10.42 %** (n=1891).
- **Appareil :** Mobile = **14.33 %** (n=6272),
  Desktop = **12.59 %** (n=2589).
- **Satisfaction :** score 5 = **24.36 %** (n=940),
  score 9 = **6.31 %** (n=1348).

Les tableaux complets et les graphiques sont dans `reports/`. Les écarts
sont descriptifs et n'impliquent aucune causalité.

## Limites et conclusion
Le dataset est **utilisable pour une exploration descriptive prudente**, mais pas
pour démontrer une causalité ou automatiser des décisions individuelles.
Nous n'avons ni dictionnaire métier officiel, ni date de résiliation, ni contrôle
externe des revenus extrêmes. Les dates et valeurs inconnues restent manquantes.
La définition exacte des formules et la date de référence doivent être confirmées.
