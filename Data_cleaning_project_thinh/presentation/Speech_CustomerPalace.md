# Discours oral — CustomerPalace


## Durée et plan
- **Diapositive 1 ** Introduction
- **Diapositive 2 ** Diagnostic initial
- **Diapositive 3 ** Méthode et outils
- **Diapositive 4 ** Choix de nettoyage
- **Diapositive 5 ** Avant / après
- **Diapositive 6 ** Churn par formule
- **Diapositive 7 ** Satisfaction et appareil
- **Diapositive 8 :** Conclusion et limites

## Diapositive 1 — Introduction

Bonjour. Aujourd'hui, je vais vous présenter notre projet de Data Quality et Customer Analytics réalisé à partir des données de CustomerPalace, une entreprise fictive qui propose plusieurs formules d'abonnement. Le point de départ est simple : l'entreprise souhaite mieux comprendre ses clients et leurs résiliations, qu'on appelle aussi le churn. Mais avant de calculer des indicateurs, il faut savoir si le fichier est fiable. Nous nous sommes donc posé cette question : peut-on exploiter cette base pour éclairer des décisions métier ? Pour y répondre, nous avons travaillé en Python, uniquement avec Pandas, NumPy et Matplotlib.

## Diapositive 2 — Diagnostic initial

Nous avons commencé par un diagnostic avec Pandas. Le fichier d'origine contient 10 000 lignes et 19 colonnes. Nous avons trouvé 250 doublons stricts, c'est-à-dire des lignes entièrement identiques. Nous avons aussi repéré 17 libellés différents dans la colonne des formules d'abonnement, dont plusieurs variantes pour une même catégorie. Par exemple, « Std » et « Standard » correspondent à la même formule. Autre difficulté : des nombres étaient enregistrés comme du texte, tels que « 34 years » pour l'âge ou « 34.4k » pour un revenu. Enfin, certaines dates étaient dans des formats différents, et des valeurs étaient absentes ou incohérentes. Si on ne corrige pas ces problèmes, on risque de compter des clients deux fois ou de fausser les regroupements et les statistiques.

## Diapositive 3 — Méthode et outils

Nous avons volontairement choisi une méthode simple, pour que quelqu'un d'autre puisse refaire notre travail. Tout le code est dans un notebook Jupyter commenté. Pandas nous sert à charger les données, transformer les colonnes et faire les tableaux de synthèse. NumPy sert notamment à représenter des valeurs manquantes. Matplotlib sert à créer les graphiques. Notre démarche suit quatre étapes : charger le CSV brut, diagnostiquer les problèmes, appliquer des règles de nettoyage clairement expliquées, puis analyser les données préparées. Nous avons aussi conservé le fichier original pour ne pas perdre la possibilité de revenir en arrière.

## Diapositive 4 — Choix de nettoyage

C'est la partie centrale du projet : nos choix de nettoyage. D'abord, nous avons utilisé drop_duplicates pour retirer uniquement les copies exactes. Nous n'avons pas supprimé des lignes seulement parce qu'elles partageaient le même nom ou le même email : sans règle métier, ce serait risqué. Ensuite, nous avons harmonisé les catégories avec strip, lower et replace. Par exemple, « Std » devient « Standard », mais nous gardons séparées les formules dont la signification n'est pas certaine. Pour les nombres, nous avons converti les formats explicites : « 34 years » devient 34 et « 34.4k » devient 34 400. En revanche, un âge négatif ou une satisfaction supérieure à 10 est rendu manquant, au lieu de fabriquer une correction. Ces limites sont des hypothèses de contrôle, pas des règles officielles de l'entreprise. Enfin, nous avons gardé les revenus inhabituellement élevés tant que nous n'avions pas de preuve d'erreur. Et nous avons retiré les colonnes identifiantes du fichier analytique final. Notre logique est donc de corriger ce qu'on comprend, et de signaler ce qu'on ne peut pas vérifier.

## Diapositive 5 — Avant / après 

Après les traitements, nous passons de 10 000 à 9 750 lignes, car seuls les 250 doublons exacts ont été supprimés. Le fichier final contient 16 colonnes, contre 19 au départ, puisque nous avons retiré les identifiants, les noms et les emails. Pour évaluer notre travail, nous avons comparé les valeurs convertibles avant et après, sur les mêmes lignes dédupliquées. C'est important pour éviter une comparaison trompeuse. Les dates d'inscription exploitables passent d'environ 92 à 99,4 %, et les revenus annuels d'environ 93 à 96,4 %. Nous avons également ramené les libellés de formules de 17 à 7. Mais améliorer la qualité ne veut pas dire faire disparaître tous les manquants : 133 valeurs numériques ont été invalidées parce qu'elles ne respectaient pas nos règles. Et surtout, ces pourcentages prouvent que les formats sont plus facilement exploitables, pas que toutes les informations sont vraies.

## Diapositive 6 — Churn par formule 

Passons aux résultats métier. Nous avons choisi d'étudier le churn, c'est-à-dire la proportion de clients marqués comme ayant résilié. Pour le calculer, nous avons harmonisé la colonne churned en 0 et 1, puis utilisé la moyenne avec Pandas. Le taux global observé est de 13,79 %. En regroupant les clients par formule, nous trouvons 16,52 % pour Basic, 12,52 % pour Standard et 10,42 % pour Premium. Il faut aussi regarder les effectifs : Basic représente 4 020 clients et Premium 1 891. On observe donc davantage de résiliations dans le groupe Basic. Pour l'entreprise, cela suggère un segment à examiner en priorité. Mais attention : cela ne démontre pas que l'abonnement Basic cause la résiliation, car les profils de clients peuvent être différents.

## Diapositive 7 — Satisfaction et appareil 
Nous avons ensuite analysé deux autres dimensions. Premièrement, la satisfaction. Parmi les personnes ayant donné la note de 5 sur 10, 24,36 % ont résilié dans notre fichier. Parmi celles ayant donné 9 sur 10, le taux n'est que de 6,31 %. On observe donc une différence importante. La satisfaction pourrait être un bon indicateur à suivre, mais nous ne savons pas si cette note a été enregistrée avant ou après la résiliation. Deuxièmement, l'appareil utilisé. Le taux de churn est de 14,33 % pour les clients sur mobile contre 12,59 % sur ordinateur. Cet écart est plus limité, et il peut dépendre d'autres caractéristiques des clients. Ces résultats sont des pistes d'investigation, pas des preuves de cause à effet. C'est pour cela que nous affichons aussi le nombre de clients pour chaque groupe.

## Diapositive 8 — Conclusion et limites
Pour conclure, notre réponse est nuancée : oui, le dataset est désormais plus cohérent et utile pour une analyse descriptive, à condition d'expliquer les règles de transformation. Nous avons supprimé les doublons exacts, harmonisé des formats et rendu visibles certaines anomalies, tout en conservant le fichier d'origine. En revanche, plusieurs limites restent importantes. Nous ne disposons pas de dictionnaire officiel pour confirmer toutes les règles métier. Nous n'avons pas la date exacte des résiliations, donc nous ne pouvons pas calculer un vrai taux sur une période précise ni établir une chronologie solide. Certains revenus très élevés restent à confirmer. Nous ne recommanderions donc pas d'utiliser directement ce fichier pour prendre des décisions automatiques sur les clients. Le principal enseignement de ce projet est que nettoyer une base ne consiste pas simplement à supprimer les valeurs gênantes : il faut pouvoir justifier ce qu'on transforme, mesurer les effets et reconnaître ce qu'on ne sait pas. Merci pour votre attention.

## Questions possibles après la présentation

**Pourquoi ne pas remplir les `NaN` par la moyenne ?**  Parce qu’une imputation systématique inventerait des valeurs, pourrait réduire artificiellement la variabilité et n’est pas justifiée par une règle métier.

**Pourquoi conserver les gros revenus ?**  Un extrême statistique n’est pas nécessairement une erreur. Sans preuve ni validation métier, le supprimer risquerait de biaiser l’analyse.

**Comment prouver le nettoyage ?**  Nous comparons sur les mêmes 9 750 lignes les proportions de valeurs convertibles, le nombre de doublons et les libellés harmonisés.

**Pourquoi ne pas conclure à une causalité ?**  On observe des groupes à un moment donné, sans garantie sur la chronologie ni sur les facteurs confondants.

**À quoi servent les trois bibliothèques ?**  Pandas pour les DataFrames, NumPy pour les valeurs manquantes et manipulations numériques, Matplotlib pour les visualisations.

**Pourquoi ne pas supprimer les lignes avec un email identique ?**  Sans règle métier confirmant qu’un email correspond à un seul client et à une seule ligne légitime, ce serait une suppression arbitraire.

**Point de vigilance :** les taux présentés correspondent à la proportion de résiliations observées parmi les statuts renseignés. Ils ne représentent pas un taux annuel vérifié.
