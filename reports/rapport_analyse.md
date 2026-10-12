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