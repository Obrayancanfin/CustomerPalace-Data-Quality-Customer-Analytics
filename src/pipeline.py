"""Reproducible quality audit and cleaning pipeline for CustomerPalace."""
from __future__ import annotations

import json
from pathlib import Path
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "dataset_tp_cleaning.csv"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
OUTPUTS = ROOT / "outputs"
AS_OF = pd.Timestamp("2026-10-12")

NUMERIC_RULES = {
    "age": (18, 100),
    "annual_income_eur": (0, None),
    "monthly_spend_eur": (0, None),
    "tenure_months": (0, None),
    "satisfaction_score": (0, 10),
    "support_tickets_12m": (0, None),
}
BOOL_MAP = {
    "yes": "Yes", "y": "Yes", "true": "Yes", "1": "Yes",
    "no": "No", "n": "No", "false": "No", "0": "No",
}
GENDER_MAP = {
    "male": "Male", "m": "Male", "man": "Male", "homme": "Male",
    "female": "Female", "f": "Female", "woman": "Female", "femme": "Female",
    "non-binary": "Non-binary", "non binary": "Non-binary",
    "nonbinary": "Non-binary", "nb": "Non-binary",
}
PLAN_MAP = {
    "basic": "Basic", "basic plan": "Basic",
    "standard": "Standard", "std": "Standard",
    "premium": "Premium",
}
PAYMENT_MAP = {
    "card": "Card", "cb": "Card", "credit card": "Card",
    "paypal": "PayPal", "pay pal": "PayPal",
    "bank transfer": "Bank Transfer", "banktransfer": "Bank Transfer",
    "wire": "Bank Transfer",
    "direct debit": "Direct Debit", "directdebit": "Direct Debit",
    "sepa": "Direct Debit",
}
DEVICE_MAP = {
    "mobile": "Mobile", "phone": "Mobile", "smartphone": "Mobile",
    "desktop": "Desktop", "pc": "Desktop", "computer": "Desktop",
    "tablet": "Tablet", "tab": "Tablet",
}
COUNTRY_MAP = {
    "france": "France", "fr": "France",
    "belgium": "Belgium", "belgique": "Belgium", "be": "Belgium",
    "spain": "Spain", "espagne": "Spain", "es": "Spain",
    "germany": "Germany", "allemagne": "Germany", "de": "Germany",
    "italy": "Italy", "italie": "Italy", "it": "Italy",
}

def normalise_text(series: pd.Series) -> pd.Series:
    result = series.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    return result.mask(result.eq("") | result.str.lower().isin(["?", "unknown", "n/a", "na", "null"]))

def category_clean(series: pd.Series, mapping: dict[str, str]) -> pd.Series:
    cleaned = normalise_text(series)
    keys = cleaned.str.lower()
    mapped = keys.map(mapping)
    # Preserve categories not covered by a defensible alias rule, with consistent casing.
    fallback = cleaned.str.title()
    return mapped.fillna(fallback).astype("string")

def save_bar(series: pd.Series, title: str, filename: str, xlabel: str = "Nombre de clients") -> None:
    counts = series.value_counts(dropna=False).head(12).sort_values()
    if counts.empty:
        return
    fig, ax = plt.subplots(figsize=(9, 5))
    counts.plot(kind="barh", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(FIGURES / filename, dpi=150)
    plt.close(fig)

def main() -> None:
    for folder in (PROCESSED, REPORTS, FIGURES, OUTPUTS):
        folder.mkdir(parents=True, exist_ok=True)
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Fichier source introuvable : {RAW_PATH}")

    raw = pd.read_csv(RAW_PATH, dtype="string")
    original_rows, original_cols = raw.shape
    raw_missing = raw.isna().sum().to_dict()
    raw_exact_duplicates = int(raw.duplicated().sum())
    raw_id_duplicate_rows = int(raw["customer_id"].duplicated(keep=False).sum())
    raw_missing_ids = int(normalise_text(raw["customer_id"]).isna().sum())

    # Audit table before any transformations.
    audit_rows = []
    for col in raw.columns:
        s = raw[col]
        audit_rows.append({
            "column": col,
            "dtype_initial": str(s.dtype),
            "missing_count": int(s.isna().sum()),
            "missing_pct": round(float(s.isna().mean() * 100), 2),
            "distinct_non_null": int(s.nunique(dropna=True)),
            "top_values": " | ".join(f"{k}: {v}" for k, v in s.value_counts(dropna=False).head(5).items()),
        })
    pd.DataFrame(audit_rows).to_csv(OUTPUTS / "diagnostic_colonnes.csv", index=False)

    df = raw.copy()
    # Remove only exact row duplicates; they contain no additional information.
    df = df.drop_duplicates().copy()

    # Normalise whitespace and missing-value tokens for text fields.
    for col in df.columns:
        if col not in NUMERIC_RULES:
            df[col] = normalise_text(df[col])

    # IDs are needed to identify customers and detect duplicate records.
    df["customer_id"] = normalise_text(df["customer_id"])
    df = df[df["customer_id"].notna()].copy()

    # If an ID appears more than once, keep the record with the most non-missing fields.
    # Stable sort makes the choice reproducible when completeness ties.
    df["_completeness"] = df.notna().sum(axis=1)
    df = df.sort_values(["_completeness", "customer_id"], ascending=[False, True], kind="stable")
    df = df.drop_duplicates(subset=["customer_id"], keep="first").drop(columns="_completeness")

    # Numeric parsing and range validation: invalid values become missing, never guessed.
    numeric_invalid = {}
    for col, (minimum, maximum) in NUMERIC_RULES.items():
        parsed = pd.to_numeric(df[col].str.replace(",", ".", regex=False), errors="coerce")
        invalid_parse = int((df[col].notna() & parsed.isna()).sum())
        out_of_range = pd.Series(False, index=df.index)
        if minimum is not None:
            out_of_range |= parsed < minimum
        if maximum is not None:
            out_of_range |= parsed > maximum
        out_of_range = out_of_range.fillna(False)
        numeric_invalid[col] = {"unparseable": invalid_parse, "out_of_range": int(out_of_range.sum())}
        parsed.loc[out_of_range] = pd.NA
        df[col] = parsed

    # Date parsing. Invalid or missing dates remain missing; impossible chronology is flagged.
    date_invalid = {}
    for col in ["signup_date", "last_login"]:
        parsed = pd.to_datetime(df[col], errors="coerce")
        date_invalid[col] = int((df[col].notna() & parsed.isna()).sum())
        df[col] = parsed
    signup_future = int((df["signup_date"] > AS_OF).sum())
    df.loc[df["signup_date"] > AS_OF, "signup_date"] = pd.NaT
    last_before_signup = df["last_login"].notna() & df["signup_date"].notna() & (df["last_login"] < df["signup_date"])
    chronology_issues = int(last_before_signup.sum())
    df.loc[last_before_signup, "last_login"] = pd.NaT

    # Canonicalise known aliases only. Unmapped categories are preserved for review.
    if "gender" in df:
        df["gender"] = category_clean(df["gender"], GENDER_MAP)
    if "plan" in df:
        df["plan"] = category_clean(df["plan"], PLAN_MAP)
    if "payment_method" in df:
        df["payment_method"] = category_clean(df["payment_method"], PAYMENT_MAP)
    if "device" in df:
        df["device"] = category_clean(df["device"], DEVICE_MAP)
    if "country" in df:
        df["country"] = category_clean(df["country"], COUNTRY_MAP)
    if "city" in df:
        df["city"] = normalise_text(df["city"]).str.title()
    for col in ["marketing_opt_in", "churned"]:
        if col in df:
            cleaned = normalise_text(df[col]).str.lower()
            df[col] = cleaned.map(BOOL_MAP).astype("string")

    # Direct identifiers are excluded from the analytical output (data minimisation).
    # Keep customer_id as a pseudonymous key for row-level traceability.
    removed_identifiers = [c for c in ["full_name", "email"] if c in df.columns]
    analytical = df.drop(columns=removed_identifiers).copy()

    # Quality comparison: comparable at dataset level; invalid numeric values now count as missing.
    final_rows, final_cols = analytical.shape
    final_missing = analytical.isna().sum().to_dict()
    comparison = []
    for col in analytical.columns:
        before = int(raw[col].isna().sum()) if col in raw.columns else 0
        after = int(analytical[col].isna().sum())
        comparison.append({
            "column": col,
            "missing_initial_raw": before,
            "missing_final": after,
            "missing_final_pct": round(after / max(len(analytical), 1) * 100, 2),
            "distinct_final": int(analytical[col].nunique(dropna=True)),
        })
    pd.DataFrame(comparison).to_csv(OUTPUTS / "comparaison_qualite.csv", index=False)

    # Save prepared dataset, keeping dates in ISO format.
    analytical.to_csv(PROCESSED / "customers_clean.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")

    # Business insights from cleaned data, with denominators made explicit.
    insights = {}
    if "churned" in analytical:
        churn = analytical["churned"].value_counts(dropna=False)
        valid_churn = analytical["churned"].isin(["Yes", "No"])
        churn_rate = float((analytical.loc[valid_churn, "churned"] == "Yes").mean() * 100) if valid_churn.any() else None
        insights["churn_rate_pct_among_valid_labels"] = round(churn_rate, 2) if churn_rate is not None else None
        insights["churn_label_counts"] = {str(k): int(v) for k, v in churn.items()}
    if "plan" in analytical and "churned" in analytical:
        tmp = analytical[analytical["churned"].isin(["Yes", "No"])].groupby("plan", dropna=False)["churned"].agg(
            customers="size", churned=lambda s: int((s == "Yes").sum()), churn_rate=lambda s: float((s == "Yes").mean() * 100)
        ).reset_index()
        tmp["churn_rate_pct"] = tmp["churn_rate"].round(2)
        tmp.drop(columns="churn_rate").to_csv(OUTPUTS / "churn_par_formule.csv", index=False)
        insights["churn_by_plan"] = tmp.drop(columns="churn_rate").to_dict("records")
    if "satisfaction_score" in analytical and "churned" in analytical:
        tmp = analytical[analytical["churned"].isin(["Yes", "No"])].groupby("churned")["satisfaction_score"].agg(["count", "mean", "median"]).round(2)
        tmp.to_csv(OUTPUTS / "satisfaction_par_churn.csv")
        insights["satisfaction_by_churn"] = {str(idx): {k: (None if pd.isna(v) else float(v)) for k, v in row.items()} for idx, row in tmp.to_dict("index").items()}
    if "support_tickets_12m" in analytical and "churned" in analytical:
        tmp = analytical[analytical["churned"].isin(["Yes", "No"])].groupby("churned")["support_tickets_12m"].agg(["count", "mean", "median"]).round(2)
        tmp.to_csv(OUTPUTS / "tickets_par_churn.csv")
        insights["tickets_by_churn"] = {str(idx): {k: (None if pd.isna(v) else float(v)) for k, v in row.items()} for idx, row in tmp.to_dict("index").items()}

    if "churned" in analytical:
        save_bar(analytical["churned"].fillna("Missing"), "Répartition de la variable churned", "churn_distribution.png")
    if "plan" in analytical:
        save_bar(analytical["plan"].fillna("Missing"), "Répartition des formules après normalisation", "plan_distribution.png")
    if "churned" in analytical and "plan" in analytical:
        rates = analytical[analytical["churned"].isin(["Yes", "No"])].groupby("plan")["churned"].apply(lambda s: (s == "Yes").mean() * 100).sort_values()
        fig, ax = plt.subplots(figsize=(9, 5))
        rates.plot(kind="barh", ax=ax)
        ax.set_title("Taux de churn observé par formule")
        ax.set_xlabel("Churn (%)")
        ax.set_ylabel("")
        fig.tight_layout()
        fig.savefig(FIGURES / "churn_by_plan.png", dpi=150)
        plt.close(fig)

    summary = {
        "as_of_date": str(AS_OF.date()),
        "input_file": "data/raw/dataset_tp_cleaning.csv",
        "initial_rows": int(original_rows),
        "initial_columns": int(original_cols),
        "initial_exact_duplicate_rows": raw_exact_duplicates,
        "initial_duplicate_customer_id_rows": raw_id_duplicate_rows,
        "initial_missing_customer_ids": raw_missing_ids,
        "rows_after_exact_dedup_and_id_resolution": int(final_rows),
        "columns_initial": int(original_cols),
        "columns_final": int(final_cols),
        "removed_direct_identifiers": removed_identifiers,
        "numeric_validation": numeric_invalid,
        "invalid_dates": date_invalid,
        "future_signup_dates_reset_to_missing": signup_future,
        "last_login_before_signup_reset_to_missing": chronology_issues,
        "missing_initial_total": int(raw.isna().sum().sum()),
        "missing_final_total": int(analytical.isna().sum().sum()),
        "missing_final_by_column": {k: int(v) for k, v in final_missing.items()},
        "insights": insights,
        "limitations": [
            "Aucun dictionnaire métier officiel n'était fourni.",
            "Les catégories non reconnues sont conservées plutôt que fusionnées arbitrairement.",
            "Les valeurs invalides sont converties en valeurs manquantes, sans imputation.",
            "La déduplication par customer_id conserve la ligne la plus complète; si deux lignes concurrentes représentent des états métier différents, une règle métier est nécessaire.",
            "Les associations observées ne démontrent pas de causalité."
        ],
    }
    (OUTPUTS / "quality_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    make_report(summary, analytical, raw_exact_duplicates, raw_id_duplicate_rows, raw_missing_ids, numeric_invalid, date_invalid, signup_future, chronology_issues)
    print("Pipeline terminé.")
    print(f"Source : {RAW_PATH.relative_to(ROOT)}")
    print(f"Dataset préparé : {(PROCESSED / 'customers_clean.csv').relative_to(ROOT)}")
    print(f"Rapport : {(REPORTS / 'rapport_qualite.md').relative_to(ROOT)}")
    print(f"Lignes initiales : {original_rows:,} | lignes finales : {final_rows:,}")
    print(f"Colonnes initiales : {original_cols} | colonnes finales : {final_cols}")

def make_report(summary, analytical, exact_dups, duplicate_id_rows, missing_ids, numeric_invalid, date_invalid, signup_future, chronology_issues):
    insights = summary["insights"]
    lines = [
        "# CustomerPalace — Diagnostic de qualité des données",
        "",
        f"> Rapport généré automatiquement à partir du fichier source. Date de référence des contrôles temporels : {summary['as_of_date']}.",
        "",
        "## 1. Synthèse exécutive",
        "",
        f"Le fichier initial contient **{summary['initial_rows']:,} lignes et {summary['initial_columns']} colonnes**. Après suppression des doublons exacts, résolution des identifiants clients répétés et exclusion des lignes sans identifiant exploitable, le dataset analytique contient **{summary['rows_after_exact_dedup_and_id_resolution']:,} lignes et {summary['columns_final']} colonnes**.",
        "",
        "Le fichier n'est pas directement fiable sans préparation : les colonnes sont importées comme texte, plusieurs champs numériques comportent des valeurs hors plage, des dates sont absentes ou incohérentes, et certaines catégories sont représentées par plusieurs variantes. Les noms et emails sont exclus du dataset analytique afin de limiter les données directement identifiantes.",
        "",
        "## 2. Diagnostic initial quantifié",
        "",
        f"- Doublons de lignes strictement identiques : **{exact_dups}**.",
        f"- Lignes appartenant à un groupe où `customer_id` est répété : **{duplicate_id_rows}**.",
        f"- Identifiants clients manquants : **{missing_ids}**.",
        f"- Valeurs manquantes brutes, toutes colonnes confondues : **{summary['missing_initial_total']:,}**.",
        "",
        "Le détail colonne par colonne est disponible dans `outputs/diagnostic_colonnes.csv`.",
        "",
        "### Validations numériques",
        "",
        "| Colonne | Valeurs non numériques | Valeurs hors plage | Règle retenue |",
        "|---|---:|---:|---|",
    ]
    rule_text = {
        "age": "18 à 100 ans",
        "annual_income_eur": ">= 0",
        "monthly_spend_eur": ">= 0",
        "tenure_months": ">= 0",
        "satisfaction_score": "0 à 10",
        "support_tickets_12m": ">= 0",
    }
    for col, vals in numeric_invalid.items():
        lines.append(f"| `{col}` | {vals['unparseable']} | {vals['out_of_range']} | {rule_text[col]} |")
    lines += [
        "",
        "Les valeurs hors plage sont converties en valeurs manquantes, et non remplacées par une valeur inventée. Les seuils sont des contrôles de plausibilité choisis pour l'analyse; ils ne proviennent pas d'un dictionnaire métier officiel.",
        "",
        "### Dates et catégories",
        "",
        f"- Dates non interprétables : `signup_date` = {date_invalid.get('signup_date', 0)}, `last_login` = {date_invalid.get('last_login', 0)}.",
        f"- Dates d'inscription postérieures à la date de référence remises à manquant : **{signup_future}**.",
        f"- Dernières connexions antérieures à la date d'inscription remises à manquant : **{chronology_issues}**.",
        "- Les variantes reconnues de genre, formule, moyen de paiement, appareil, pays et booléens sont harmonisées. Les valeurs ambiguës ou non reconnues sont conservées pour ne pas supposer une équivalence métier.",
        "",
        "## 3. Décisions de préparation et justification",
        "",
        "| Problème | Décision | Justification et compromis |",
        "|---|---|---|",
        "| Doublons exacts | Suppression | Une ligne identique n'ajoute pas d'information; le nombre supprimé est mesuré. |",
        "| `customer_id` répété | Conserver la ligne la plus complète par identifiant | Produit une clé unique pour l'analyse. C'est une hypothèse de travail à valider si les lignes représentent des états successifs. |",
        "| Identifiant client absent | Exclure la ligne | Sans clé, il est impossible de garantir l'unicité du client ou de résoudre les doublons de façon fiable. |",
        "| Valeurs numériques invalides | Convertir en manquant | Évite d'inventer une valeur; les analyses de chaque indicateur doivent préciser leur effectif disponible. |",
        "| Variantes de catégories | Harmoniser seulement les alias défendables | Réduit les catégories artificiellement séparées sans fusionner des offres dont l'équivalence n'est pas prouvée. |",
        "| Dates incohérentes | Convertir en manquant | Préserve la ligne tout en empêchant d'utiliser une date chronologiquement impossible. |",
        "| Nom et email | Exclure de la sortie analytique | Principe de minimisation; ces champs ne sont pas nécessaires aux constats agrégés. |",
        "",
        "## 4. Évaluation après préparation",
        "",
        "La comparaison par colonne se trouve dans `outputs/comparaison_qualite.csv`. Elle permet de vérifier les valeurs manquantes restantes et le nombre de valeurs distinctes après harmonisation. Le fichier `data/processed/customers_clean.csv` est la sortie analytique; le fichier brut est conservé inchangé dans `data/raw/`.",
        "",
        f"- Valeurs manquantes dans le fichier brut : **{summary['missing_initial_total']:,}**.",
        f"- Valeurs manquantes dans le dataset analytique préparé : **{summary['missing_final_total']:,}**.",
        "- Une augmentation du nombre de valeurs manquantes peut être attendue : les valeurs impossibles ont été invalidées plutôt que laissées comme des nombres apparemment fiables.",
        "",
        "## 5. Constats métier",
        "",
    ]
    if insights.get("churn_rate_pct_among_valid_labels") is not None:
        lines.append(f"1. **Résiliations observées.** Le taux de churn parmi les lignes dont le libellé est interprétable est de **{insights['churn_rate_pct_among_valid_labels']:.2f}%**. Il s'agit du taux dans cet export, pas nécessairement du taux réel de l'ensemble de la clientèle.")
    plan_rows = insights.get("churn_by_plan", [])
    if plan_rows:
        ordered = sorted([r for r in plan_rows if r.get("plan") is not None and r.get("customers", 0) >= 30], key=lambda x: x.get("churn_rate_pct", 0))
        if ordered:
            low, high = ordered[0], ordered[-1]
            lines.append(f"2. **Différences entre formules.** Parmi les formules comptant au moins 30 clients étiquetés, le taux de churn varie de **{low['churn_rate_pct']:.2f}%** pour `{low['plan']}` à **{high['churn_rate_pct']:.2f}%** pour `{high['plan']}`. Les écarts sont descriptifs et ne prouvent pas que la formule cause la résiliation.")
    sat = insights.get("satisfaction_by_churn", {})
    if "Yes" in sat and "No" in sat and sat["Yes"].get("mean") is not None and sat["No"].get("mean") is not None:
        lines.append(f"3. **Satisfaction et churn.** Le score moyen de satisfaction est de **{sat['Yes']['mean']:.2f}/10** chez les clients étiquetés résiliés et de **{sat['No']['mean']:.2f}/10** chez les clients non résiliés, sur les scores disponibles. Cette association doit être vérifiée avec les effectifs et ne démontre pas de causalité.")
    tickets = insights.get("tickets_by_churn", {})
    if "Yes" in tickets and "No" in tickets and tickets["Yes"].get("mean") is not None and tickets["No"].get("mean") is not None:
        lines.append(f"4. **Tickets de support et churn.** Le nombre moyen de tickets sur 12 mois est de **{tickets['Yes']['mean']:.2f}** pour les clients étiquetés résiliés, contre **{tickets['No']['mean']:.2f}** pour les non-résiliés. Le lien peut refléter plusieurs phénomènes et ne suffit pas à conclure à une relation causale.")
    lines += [
        "",
        "Les chiffres et tableaux sources sont disponibles dans `outputs/` et les visualisations dans `reports/figures/`. Les constats sont recalculés à chaque exécution.",
        "",
        "## 6. Limites et recommandations",
        "",
        "- Demander au métier un dictionnaire de données, la définition exacte du churn et le moment où chaque variable est mesurée.",
        "- Valider la règle de dédoublonnage de `customer_id` avec le propriétaire de la donnée.",
        "- Examiner les catégories non reconnues (ex. formules atypiques) avant toute fusion ou exclusion.",
        "- Définir des règles officielles de contrôle, des seuils d'alerte et un suivi périodique de la qualité.",
        "- Avant un modèle prédictif, évaluer les fuites de données, les variables disponibles au moment de la prédiction et la représentativité de l'échantillon.",
        "- Ne pas publier les données brutes ni les données potentiellement identifiantes sur un dépôt public sans autorisation.",
        "",
        "## 7. Reproduction",
        "",
        "Depuis la racine du dépôt, activer l'environnement Python, installer `requirements.txt`, puis lancer `python src/pipeline.py`. Les fichiers de sortie sont générés dans `data/processed/`, `outputs/` et `reports/`.",
        "",
    ]
    (REPORTS / "rapport_qualite.md").write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    main()
