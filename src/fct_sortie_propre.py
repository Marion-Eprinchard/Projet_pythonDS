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
    style = (
        df_importances.style
        .background_gradient(cmap=cmap, subset=["importance"])
        .format({"importance": "{:.4f}"})
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
    style = (
        df_corr.style
        .background_gradient(
            cmap="coolwarm",
            subset=["corr"]
        )
        .background_gradient(
            cmap="Purples",
            subset=["abs_corr"]
        )
        .format({
            "corr": "{:.4f}",
            "abs_corr": "{:.4f}"
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
