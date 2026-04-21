import pandas as pd
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns


def beau_report(y_test, y_pred, cmap="Blues"):
    """
    Tableau joli, coloré pour classification_report
    """
    # Récupérer le report
    report = classification_report(y_test, y_pred, output_dict=True)

    # Conversion en DataFrame
    df = pd.DataFrame(report).T

    # Réordonner les colonnes dans le même ordre que le texte
    df = df[["precision", "recall", "f1-score", "support"]]

    # Convertir support en entier
    df["support"] = pd.to_numeric(df["support"], errors="coerce").fillna(0).astype(int)

    # Fixer le support de accuracy = somme des supports des classes
    total_support = df.loc[df.index.isin(["1", "2", "3", "4"]), "support"].sum()
    df.loc["accuracy", "support"] = total_support

    # Styliser : couleurs + espacement
    style = (
        df.style
        .background_gradient(cmap=cmap, subset=["precision", "recall", "f1-score"])
        .format({
            "precision": "{:.3f}",
            "recall": "{:.3f}",
            "f1-score": "{:.3f}",
            "support": "{:d}"
        })
        .set_table_styles(
            [
                {"selector": "th", "props": [("padding", "8px 16px")]},
                {"selector": "td", "props": [("padding", "6px 18px")]},
            ]
        )
        .set_properties(**{"font-size": "13pt"})
    )

    return style


def matrice_confusion(donnees):
    """
    Belle matrice de confusion
    """
    plt.figure(figsize=(6, 4))
    sns.heatmap(donnees, annot=True, fmt='d', cmap='Purples',
                xticklabels=['Prédit 1', 'Prédit 2', 'Prédit 3', 'Prédit 4'],
                yticklabels=['Réel 1', 'Réel 2', 'Réel 3', 'Réel 4'])
    plt.xlabel('Prédictions')
    plt.ylabel('Réel')
    plt.title('Matrice de confusion')
    plt.show()


def beau_importances(df_importances, cmap="Blues"):
    """
    Retourne un beau tableau pour les importances de variables
    """
    df2 = df_importances.copy()
    df2.columns = [col.capitalize() for col in df2.columns]

    style = (
        df2.style
        .background_gradient(cmap=cmap, subset=["Importance"])
        .format({"Importance": "{:.4f}"})
        .set_table_styles(
            [
                {"selector": "th", "props": [("padding", "8px 16px")]},
                {"selector": "td", "props": [("padding", "6px 18px")]},
            ]
        )
        .set_properties(**{"font-size": "13pt"})
    )
    return style


def beau_importance_gravite(df_corr):
    """
    Tableau propre et coloré pour l'influence des variable sur la prédiction des gravité :
    - rouge = corrélation positive
    - bleu = corrélation négative
    - intensité = force de la corrélation
    """
    df2 = df_corr.copy()

    # Renommage clair des colonnes
    df2 = df2.rename(columns={
        "corr": "Correlation",
        "abs_corr": "Correlation absolue"
    })

    style = (
        df2.style
        .background_gradient(
            cmap="coolwarm",
            subset=["Correlation"]
        )
        .background_gradient(
            cmap="Purples",
            subset=["Correlation absolue"]
        )
        .format({
            "Correlation": "{:.4f}",
            "Correlation absolue": "{:.4f}"
        })
        .set_table_styles(
            [
                {"selector": "th", "props": [("padding", "8px 20px")]},
                {"selector": "td", "props": [("padding", "6px 22px")]},
            ]
        )
        .set_properties(**{"font-size": "13pt"})
    )
    return style


def belle_colonnes(df, max_lines=2):
    """
    Affiche les colonnes d'un DataFrame
    """
    cols = list(df.columns)
    n = len(cols)

    # Nombre de colonnes par ligne
    per_line = (n + max_lines - 1) // max_lines

    # Découpage en lignes
    rows = [cols[i:i+per_line] for i in range(0, n, per_line)]

    df_cols = pd.DataFrame(rows)

    style = (
        df_cols.style
        .hide(axis="index")
        .hide(axis="columns")
        .set_properties(**{"font-size": "13pt", "padding": "6px 14px"})
    )
    return style


def belle_head(df, n=5):
    """
    Affiche les n premières lignes d'un DataFrame dans un tableau propre
    """
    df_head = df.head(n)

    style = (
        df_head.style
        .set_properties(**{"font-size": "11pt", "padding": "8px 15px"})
    )
    return style
