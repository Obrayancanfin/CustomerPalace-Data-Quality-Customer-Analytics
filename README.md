# CustomerPalace — Data Quality & Customer Analytics

## Présentation

Ce projet de Master 1 porte sur l’évaluation et l’amélioration de la qualité des données clients de **CustomerPalace**, une entreprise fictive proposant plusieurs formules d’abonnement.

L’objectif est de déterminer si le dataset peut être utilisé de manière fiable pour analyser les caractéristiques des clients, leurs habitudes de consommation et les facteurs éventuellement associés à la résiliation (*churn*).

Le projet s’appuie sur le fichier source `dataset_tp_cleaning.csv`. Les décisions de nettoyage et de transformation doivent être justifiées, mesurées et reproductibles.

## Objectifs

- Organiser un projet Python clair et reproductible.
- Réaliser un diagnostic de la qualité du dataset initial.
- Identifier et documenter les incohérences, valeurs manquantes, doublons ou autres problèmes observés.
- Appliquer des transformations justifiées, sans écraser les données sources.
- Comparer les données avant et après traitement.
- Présenter au moins trois observations métier vérifiables.
- Documenter les limites et les incertitudes restantes.

### Bonus facultatif : machine learning

Le projet peut inclure un premier modèle de classification visant à estimer la résiliation d’un abonnement, avec `churned` comme variable cible. Cette partie est facultative et doit présenter une évaluation correcte du modèle, une comparaison avec une référence simple et une discussion de ses limites.

## Dataset

Le fichier source attendu est :

```text
dataset_tp_cleaning.csv
```

Placez-le dans l’emplacement prévu par votre organisation de projet et adaptez les chemins utilisés dans le code si nécessaire.

> **Important :** conservez toujours le dataset source intact. Ne publiez pas de données potentiellement identifiantes dans un dépôt public sans autorisation explicite.

## Organisation du dépôt

L’organisation ci-dessous est une proposition à adapter à l’architecture réellement retenue par l’équipe :

```text
.
├── data/
│   ├── raw/                 # Données sources, non modifiées
│   └── processed/            # Dataset préparé
├── notebooks/                # Explorations et analyses éventuelles
├── src/                      # Code Python réutilisable
├── reports/                  # Rapport, tableaux et visualisations
├── requirements.txt          # Dépendances Python
└── README.md
```

Les dossiers et fichiers ci-dessus sont indicatifs : remplacez-les par la structure effectivement présente dans le dépôt.

## Prérequis

- Python 3 installé (la version exacte doit être précisée par l’équipe).
- Git.
- Le fichier `dataset_tp_cleaning.csv`.
- Les bibliothèques Python utilisées par le projet, déclarées dans `requirements.txt` ou dans un autre fichier de dépendances.

## Installation

Clonez le dépôt, puis placez-vous dans son répertoire :

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_DEPOT>
```

Créez et activez un environnement virtuel :

```bash
python -m venv .venv
```

Sous macOS/Linux :

```bash
source .venv/bin/activate
```

Sous Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

Installez les dépendances lorsque le fichier `requirements.txt` est disponible :

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si le projet utilise une autre méthode de gestion des dépendances, suivez les instructions correspondantes.

## Exécution

Les commandes exactes dépendent de l’architecture et des scripts retenus par l’équipe. Remplacez les exemples ci-dessous par les commandes réellement testées avant de publier le README.

Exemple pour un script Python :

```bash
python src/main.py
```

Exemple pour un notebook :

```bash
jupyter notebook
```

Exécutez les étapes dans l’ordre documenté par le projet. Vérifiez que les chemins vers les données sont corrects et que les résultats peuvent être régénérés à partir du fichier source.

## Méthodologie

### 1. Diagnostic initial

Décrire la structure du dataset, ses dimensions, les types de variables et les problèmes de qualité réellement observés. Quantifier les problèmes importants et expliquer leurs conséquences possibles sur les analyses.

### 2. Nettoyage et transformations

Pour chaque traitement significatif, documenter :

- le problème constaté ;
- la règle appliquée ;
- la justification du choix ;
- l’effet mesuré sur les données ;
- les limites ou pertes d’information éventuelles.

Une valeur inhabituelle ne doit pas être corrigée ou supprimée automatiquement sans justification. Il peut être pertinent de conserver certaines valeurs lorsque les données disponibles ne permettent pas de conclure qu’elles sont erronées.

### 3. Contrôle après traitement

Comparer les données initiales et préparées. Présenter les changements observés, les contrôles réalisés et les problèmes qui subsistent.

### 4. Analyse métier

Présenter au moins trois observations appuyées par des indicateurs, tableaux ou visualisations. Nuancer les conclusions lorsque le dataset ne permet pas d’établir une relation causale ou de vérifier une hypothèse.

### 5. Bonus machine learning (facultatif)

Si cette partie est réalisée, utiliser `churned` comme cible, séparer les données d’entraînement et de test, comparer le modèle à une référence simple et présenter des métriques adaptées, par exemple la précision, le rappel, le F1-score et la matrice de confusion. Vérifier les risques de fuite de données et expliciter les limites de généralisation.

## Résultats et livrables

Le dépôt doit contenir ou expliquer comment régénérer :

- le code source et/ou les notebooks ;
- le dataset final préparé, avec une description des informations conservées ;
- le rapport d’analyse du diagnostic, des décisions de nettoyage, de la comparaison avant/après et des limites ;
- une synthèse présentant au moins trois constats métier étayés ;
- le fichier de dépendances ;
- le cas échéant, les résultats du modèle de machine learning facultatif.

**Emplacement des résultats :** à compléter par l’équipe selon l’organisation réelle du dépôt, par exemple `data/processed/` pour le dataset préparé et `reports/` pour le rapport.

## Reproductibilité

Pour permettre à une autre personne de reproduire le travail :

1. conserver les données sources inchangées ;
2. déclarer les dépendances et, si possible, leurs versions ;
3. documenter les commandes d’exécution ;
4. préciser les entrées et sorties de chaque étape ;
5. vérifier les résultats depuis un environnement propre ;
6. expliquer les choix méthodologiques et les limites connues.

## Équipe

À compléter :

- Membres : Abdoulaye Izedine , Beye Elhadji , Tran Duc-Thinh , Canfin Obrayan 
- Formation : Master 1


## Limites

Les conclusions dépendent du contenu et de la qualité du dataset fourni. En l’absence de dictionnaire de données ou de règles métier officielles, les hypothèses doivent être clairement distinguées des faits vérifiables. Un modèle de machine learning performant sur ce dataset ne garantit pas des performances équivalentes sur de futurs clients.
