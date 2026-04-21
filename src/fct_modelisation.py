import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def y_x_train_test(df, var_y, list_var_x):
    """
    Création des données y et X puis des ensembles Train/Test
    """
    y = df[var_y].astype(str)

    # Création catégorie de l'heure
    df["heure_cat"] = pd.cut(
        df["hr"].astype(int),
        bins=[0, 6, 12, 18, 24],
        labels=["Nuit", "Matin", "Après-midi", "Soir"],
        right=False
    )

    list_var_x.append("heure_cat")
    X = df[list_var_x]
    X["an"] = X["an"].astype(str)

    X_encoded = pd.get_dummies(X, drop_first=True)

    # Train, test
    # startify pour les classes déséquilibrées
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=66, stratify=y
    )

    return X_train, X_test, y_train, y_test


def importance_variable(modele, X_train):
    """
    Dataframe des 10 variables les plus importantes en interne du modèle
    """
    importances = modele.feature_importances_
    cols = X_train.columns

    df_importances = pd.DataFrame({
        "variable": cols,
        "importance": importances
    }).sort_values("importance", ascending=False)

    return df_importances.head(10)


def importance_variable_gravite(modele, X_test, num_grav):
    """
    Dataframe de l'influence des variables sur les classes prédites
    Top 10
    """
    # calculs de la probabilité pour les gravités choisies
    proba = modele.predict_proba(X_test)
    proba_grav = proba[:, num_grav]

    # calcul de la corrélation
    df_corr = pd.DataFrame({
        "variable": X_test.columns,
        "corr": [np.corrcoef(X_test[col], proba_grav)[0, 1] for col in X_test.columns]
    })

    df_corr["abs_corr"] = df_corr["corr"].abs()

    return df_corr.sort_values("abs_corr", ascending=False).head(10)
