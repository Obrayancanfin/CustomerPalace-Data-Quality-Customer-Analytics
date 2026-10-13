# PROJET M1 — DATA QUALITY & CUSTOMER ANALYTICS

**Durée :** 2 jours  
**Niveau :** Master 1  
**Format :** groupe de 3 à 4, selon les consignes de l'enseignant  
**Dataset :** `dataset_tp_cleaning.csv`  
**Technologies :** Python - bibliothèques et outils au choix des étudiants  
**Bonus facultatif :** introduction au machine learning

---

## 1. Contexte professionnel

Vous intervenez en tant que **Data Analyst / Data Engineer junior** pour **CustomerPalace**, une entreprise fictive commercialisant plusieurs formules d'abonnement.

L'entreprise possède un export de sa base clients. Elle souhaite mieux comprendre les caractéristiques de sa clientèle, ses habitudes de consommation et les éventuels facteurs associés à la résiliation des abonnements (*churn*).

Cependant, les équipes métiers ne savent pas si l'export peut être exploité de manière fiable. Votre mission consiste à reprendre ce jeu de données, à évaluer sa qualité et à en faire une source pertinente pour de futures analyses.

Vous disposez uniquement du fichier fourni. Vous n'avez ni dictionnaire de données officiel, ni règle métier complémentaire, ni procédure de nettoyage prédéfinie.

**Votre rôle est de faire vos propres choix techniques et méthodologiques et de pouvoir les défendre.**

## 2. Mission

À l'issue du projet, votre équipe doit être en mesure de répondre à la question suivante :

> **Ce dataset peut-il être utilisé de manière fiable pour analyser les clients et éclairer les décisions de l'entreprise ? Si oui, sous quelles conditions ?**

Votre mission comprend quatre volets indissociables :

**A — Construire un projet Python exploitable**  
Proposer une organisation de travail cohérente, compréhensible par un autre développeur et permettant de reproduire les traitements réalisés.

**B — Évaluer la qualité des données**  
Présenter un diagnostic argumenté du dataset initial : sa structure, ses limites, ses incohérences et les risques qu'il pourrait faire courir à une analyse métier.

**C — Préparer un jeu de données fiable**  
Décider librement des traitements nécessaires, les implémenter, puis produire une version exploitable du dataset. Chaque décision qui modifie ou exclut des données doit être justifiée.

**D — Valoriser les résultats**  
Démontrer en quoi les transformations améliorent — ou n'améliorent pas — la qualité du jeu de données et présenter des constats métier issus de votre travail.

**Il n'existe pas de méthode de nettoyage attendue ou de fichier final unique.** Deux équipes peuvent produire des résultats différents et obtenir une très bonne évaluation si leurs décisions sont cohérentes, mesurées et défendables.

## 3. Liberté et responsabilité

Le projet principal est **volontairement non guidé**.

- Aucune architecture de dossiers n'est imposée.
- Aucune technique de nettoyage, d'imputation ou de transformation n'est imposée.
- Aucun seuil de valeurs aberrantes ni taux de suppression acceptable n'est fourni.
- Aucune bibliothèque spécifique, à l'exception du langage Python, n'est imposée.
- Aucune liste des problèmes présents dans le dataset ne sera communiquée.
- Le choix des colonnes conservées, transformées ou écartées appartient aux étudiants.

La liberté de choix **n'exonère pas** de démontrer que le travail est rigoureux. Toute hypothèse non vérifiable avec les données doit être clairement présentée comme une hypothèse, et non comme un fait.

## 4. Attendus du projet principal

### 4.1. Organisation du projet

Le dépôt doit permettre à une personne extérieure de comprendre son fonctionnement, d'identifier les principaux livrables et de reproduire les résultats sur le fichier initial.

Les étudiants choisissent eux-mêmes leur architecture, leurs modules, leur mode d'exécution et leur gestion des dépendances.

### 4.2. Diagnostic initial

Produire un état des lieux argumenté de la qualité des données, mettant en évidence les problèmes jugés importants, leur ampleur et leurs conséquences potentielles.

Il ne suffit pas d'affirmer qu'une colonne « contient des erreurs » : une analyse de qualité doit apporter des éléments vérifiables.

### 4.3. Nettoyage et transformation

Construire une version des données dont le périmètre, les règles de transformation et les limites sont explicitement documentés.

Les étudiants sont libres de retenir les traitements qu'ils jugent appropriés, y compris de ne pas modifier certains éléments. Un choix de **ne pas corriger** peut être justifié s'il repose sur une analyse convaincante.

### 4.4. Évaluation de la qualité obtenue

Présenter des éléments de comparaison entre les données initiales et les données produites. L'objectif est de démontrer les effets réels des décisions prises, y compris les éventuelles pertes d'information ou incertitudes persistantes.

### 4.5. Analyse métier

Formuler au moins **trois observations métier** tirées du jeu de données préparé. Chaque observation doit s'appuyer sur des résultats ou représentations vérifiables et préciser, lorsque cela est nécessaire, les limites de l'interprétation.

Les observations peuvent notamment porter sur les caractéristiques de la clientèle, les abonnements, la consommation, la satisfaction ou les résiliations. Aucun axe n'est obligatoire.

## 5. Livrables obligatoires

À remettre sous la forme d'un **dépôt Git** accessible à l'enseignant :

1. **Le projet Python** : code source et/ou notebooks organisés, permettant de retrouver les analyses et de reproduire la préparation des données.
2. **Un `README.md`** : objectif du projet, choix d'organisation, prérequis, installation, exécution et emplacement des résultats.
3. **Le dataset final** : fichier de données préparé, avec description des informations conservées. Si sa diffusion n'est pas appropriée, documenter précisément comment le régénérer.
4. **Un rapport d'analyse** (`.md`, `.pdf` ou notebook clairement structuré) présentant le diagnostic, les décisions de nettoyage, leurs justifications, les limites et la comparaison avant/après.
5. **Une synthèse métier** : au moins trois constats, avec éléments de preuve (tableaux, indicateurs ou visualisations au choix).
6. **Les dépendances du projet** : déclaration suffisamment précise pour permettre à un autre étudiant d'exécuter le travail dans un nouvel environnement.

**Important :** le dataset source ne doit pas être écrasé. Les données éventuellement identifiantes ne doivent pas être publiées sur un dépôt public sans autorisation explicite.

## 6. Justification des décisions : exigence centrale

Le rapport doit permettre de comprendre, pour les décisions de traitement significatives :

| Question évaluée | Ce qui est attendu |
|---|---|
| Quel problème ou risque a motivé ce choix ? | Une observation fondée sur le dataset |
| Quelle décision a été prise ? | Une règle ou un traitement explicite |
| Pourquoi ce choix plutôt qu'un autre ? | Un raisonnement technique ou métier |
| Quel est l'effet sur les données ? | Une mesure ou un constat vérifiable |
| Quelles limites subsistent ? | Une reconnaissance des incertitudes ou compromis |

Un traitement techniquement correct mais impossible à expliquer sera pénalisé. À l'inverse, une décision discutable peut être recevable si ses hypothèses, ses risques et ses conséquences sont évalués avec rigueur.

## 7. Organisation sur deux jours

Ces repères indiquent les **objectifs de production**, et non une procédure technique à suivre.

### Jour 1 — Prise en main et décisions

**Objectif de la journée :** disposer d'un projet initialisé, d'une compréhension argumentée du dataset et d'une première version du travail de préparation.

**Point d'étape de fin de journée :** être capable d'expliquer oralement les principaux risques détectés, les choix déjà effectués et les questions encore ouvertes.

### Jour 2 — Fiabilisation et restitution

**Objectif de la journée :** rendre les traitements reproductibles, contrôler les résultats, finaliser les analyses métier et préparer la restitution.

**Point d'étape final :** livrer le dépôt Git et présenter les conclusions, les arbitrages réalisés et les limites de la base produite.

Il n'est pas nécessaire que tous les groupes travaillent dans le même ordre.

## 8. Restitution orale

**Durée indicative : 5 minutes de présentation + 5 minutes de questions par groupe.**

L'oral doit permettre de défendre les choix réalisés, sans refaire la démonstration de toutes les lignes de code. Les étudiants doivent notamment être capables d'expliquer ce qu'ils considèrent comme une donnée fiable, ce qu'ils ont volontairement conservé ou écarté, les conséquences de leurs traitements et ce qu'il reste impossible d'affirmer avec le dataset disponible.

L'enseignant pourra demander de retrouver dans le code la règle responsable d'un changement observé dans le rapport.

## 9. Critères d'évaluation — projet principal (/20)

| Critère | Points | Éléments appréciés |
|---|---:|---|
| Architecture et qualité du projet Python | 3 | Lisibilité, cohérence, reproductibilité, dépendances |
| Qualité du diagnostic initial | 4 | Pertinence, profondeur, quantification, interprétation des risques |
| Choix et mise en œuvre des traitements | 5 | Cohérence, robustesse, compréhension, absence de corrections arbitraires |
| Justification et traçabilité | 4 | Arguments, comparaison avant/après, compromis, limites |
| Analyse et communication métier | 2 | Pertinence des constats, preuves, prudence des conclusions |
| Documentation et soutenance | 2 | Autonomie du lecteur, clarté, capacité à défendre les choix |
| **Total** | **20** | |

**La quantité de lignes modifiées, le nombre de colonnes supprimées ou le recours à des méthodes complexes ne constituent pas des critères de réussite en soi.**

---

# BONUS FACULTATIF — PREMIER MODÈLE DE MACHINE LEARNING

**Ce bonus est le seul volet proposant des repères méthodologiques.** Il n'est pas obligatoire et ne remplace pas l'analyse de qualité des données.

## 10. Problématique

La direction souhaite savoir si les données disponibles permettent d'estimer la probabilité qu'un client résilie son abonnement.

**Mission bonus :** construire et évaluer un premier modèle de classification à partir du dataset préparé, en utilisant `churned` comme variable cible.

Le but n'est pas de trouver le meilleur modèle possible, mais de démontrer qu'une démarche expérimentale de machine learning peut être menée sans confondre apprentissage et évaluation.

## 11. Repères méthodologiques du bonus

Les étapes ci-dessous servent exclusivement d'aide au bonus. Elles ne constituent pas des instructions pour le nettoyage du projet principal.

**Repère 1 — Définir l'expérience.** Clarifier ce que signifie la variable `churned`, distinguer la cible des variables explicatives et expliciter quelles informations seraient réellement disponibles au moment d'une prédiction. Identifier les colonnes qui peuvent poser un problème d'identification ou de fuite de données.

**Repère 2 — Préparer l'évaluation.** Séparer les observations dédiées à l'apprentissage de celles réservées à l'évaluation. Éviter que les transformations apprises sur les données d'entraînement exploitent des informations issues du jeu de test.

**Repère 3 — Établir une référence.** Déterminer un score de référence simple, puis entraîner au moins un modèle de classification. Le choix du modèle est libre.

**Repère 4 — Mesurer la performance.** Examiner une matrice de confusion et plusieurs métriques adaptées au problème : par exemple précision, rappel et F1-score. Commenter la répartition des classes et expliquer pourquoi une simple accuracy peut être trompeuse.

**Repère 5 — Interpréter et nuancer.** Présenter les résultats, les principales limites, les risques de fuite d'information et les améliorations possibles. Un modèle performant sur ce fichier ne prouve pas qu'il fonctionnerait sur de futurs clients.

## 12. Livrables du bonus

- Code et instructions permettant de reproduire l'entraînement et l'évaluation.
- Présentation du modèle choisi et des variables retenues.
- Résultats chiffrés sur des données non utilisées à l'entraînement.
- Comparaison avec une référence simple.
- Court commentaire critique sur la valeur réelle du modèle.

**Valorisation indicative : jusqu'à +2 points de bonus sur la note du projet, note finale plafonnée à 20/20.** Le bonus n'est pas évalué sur la seule performance prédictive.

---

## 13. Conditions de réussite

Ce projet est réussi lorsque vous pouvez remettre votre dépôt à une personne qui ne connaît pas vos choix et qu'elle peut :

- comprendre l'état initial de la base
- identifier et reproduire vos transformations
- constater leurs effets
- vérifier vos principales conclusions
- comprendre ce que les données permettent — et ne permettent pas — de décider.

**La meilleure solution n'est pas nécessairement celle qui produit le dataset le plus « propre », mais celle dont la fiabilité, les arbitrages et les limites sont les mieux démontrés.**
