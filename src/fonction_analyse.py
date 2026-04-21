import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import chi2_contingency



def tableau_propre(dataframe, par_dep=False):
    """
    Formatage en tableaux propre des dataframes

    par_dep=False : tableau national
    par_dep=True : tableau par département

    """

    if par_dep:
        subtitle = "Résultats des votes du premier tour par département"
        labels = dict(
            code_departement="Code departement",
            candidat="Candidat",
            voix="Nombre de votes (total)",
            pourcentage="Score (% votes exprimés)"
        )
    else:
        subtitle = "Résultats des votes du premier tour"
        labels = dict(
            candidat="Candidat",
            voix="Nombre de votes (total)",
            pourcentage="Score (% votes exprimés)"
        )

    table = (
        GT(dataframe)
        .fmt_number(columns="voix", decimals=0, sep_mark=" ")
        .fmt_percent(columns="pourcentage", decimals=2, dec_mark=",")
        .tab_header(
            title="Élections",
            subtitle=subtitle
        )
        .cols_label(**labels)
    )

    return table



def compter_par_mois(
    df: pd.DataFrame,
    variable: str,
    condition_grav: list[str] | None = None
) -> pd.DataFrame:
    """Fonction qui compte le nombre d'événements ou d'occurrences pour
    chaque mois pour une variable donnée.

    La fonction a à l'origine été créée pour compter le nombre d'accidents
    et d'usagers par mois.
    Il est possible de compter en posant une condition sur la gravité
    associée à la variable comptée.

    Parameters
    ----------
    df : DataFrame
        Le DataFrame sur lequel on applique la fonction.
    variable : str
        Variable dont on souhaite compter les occurrences distinctes.
    condition_grav : list(str) or None
        Condition posée sur la gravité, s'il y en a.

    Returns
    -------
    pd.DataFrame
    """
    filtre = df
    if condition_grav is not None:
        filtre = df[df["grav"].isin(condition_grav)]
    return (
        filtre
        .drop_duplicates(subset=variable)
        .assign(periode=lambda x: x["date"].dt.to_period("M"))
        .groupby("periode")
        .size()
        .reset_index(name="nb")
    )


def evolution_mensuelle(df: pd.DataFrame) -> None:
    """Trace le graphique de l'évolution du nombre d'accidents, d'usagers
    impliqués et de victimes au cours du temps, mois par mois.

    Parameters
    ----------
    df : pd.DataFrame
        Le DataFrame sur lequel appliquer la fonction.
    """

    accidents = compter_par_mois(df, "Num_Acc")
    usagers = compter_par_mois(df, "id_usager")
    victimes = compter_par_mois(
        df,
        "id_usager",
        condition_grav=["Blessé léger", "Blessé hospitalisé", "Tué"]
    )

    dates = accidents["periode"].dt.to_timestamp()
    labels_xticks = dates.dt.strftime("%b %Y")

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(range(len(accidents)), accidents["nb"], label="Accidents")
    ax.plot(range(len(usagers)), usagers["nb"], label="Usagers impliqués")
    ax.plot(
        range(len(victimes)),
        victimes["nb"],
        label="Victimes non indemnes"
    )

    ax.set_xticks(range(len(accidents)))
    ax.set_xticklabels(labels_xticks, rotation=45, ha="right")
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre")
    ax.set_title("Évolution mensuelle des accidents et usagers impliqués")

    handles, labels_legende = ax.get_legend_handles_labels()
    ordre_legende = [1, 2, 0]
    ax.legend(
        [handles[i] for i in ordre_legende],
        [labels_legende[i] for i in ordre_legende]
    )

    plt.grid(axis="both")
    plt.tight_layout()
    plt.show()


def nb_accidents_par(
    df: pd.DataFrame,
    variable: str,
    nom_variable: str,
    ordre: list[str] | None = None,
    afficher_nb: bool = False
) -> None:
    """Compte le nombre d'accidents pour une variable voulue.

    Parameters
    ----------
    df : pd.DataFrame
        Le DataFrame sur lequel appliquer la fonction.
    variable : str
        La variable du DataFrame pour laquelle on veut compter le nombre d'accidents.
    ordre : list[str] or None
        L'ordre dans lequel on souhaite afficher les modalités.
        Si vaut None, l'ordre n'est pas précisé (l'ordre sera alors alphabétique).
    afficher_nb : bool
        Si vaut True, affiche le nombre exact d'accidents au-dessus de la barre du graphique.

    Returns
    -------
    None
    """

    nb_accidents_groupe = (
        df.drop_duplicates(subset="Num_Acc")
        .groupby(variable)
        .size()
        .reset_index(name="nb_accidents")
    )

    if ordre is not None:
        nb_accidents_groupe = (
            nb_accidents_groupe
            .set_index(variable)
            .reindex(ordre)
            .reset_index()
        )

    bars = plt.bar(nb_accidents_groupe[variable], nb_accidents_groupe["nb_accidents"])

    if afficher_nb:
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                int(height),
                ha="center", va="bottom",
                fontsize=9
            )

    plt.grid(which="both", axis="y")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel(nom_variable)
    plt.ylabel("Accidents")
    plt.title(f"Nombre d'accidents selon leur {nom_variable.lower()}")
    plt.show()


def tab_cont_grav(
    df: pd.DataFrame,
    variable: str,
    ordre_lignes: list[str],
    ordre_colonnes: list[str]
) -> pd.DataFrame:
    """Construit le tableau de contingence de la variable souhaitée et de la gravité.

    Parameters
    ----------
    df : pd.DataFrame
        Le DataFrame sur lequel appliquer la fonction.
    variable : str
        La variable du DataFrame pour laquelle on veut construire un tableau
        de contingence pour la gravité.
    ordre_lignes : list[str]
        L'ordre dans lequel afficher les modalités des lignes (utile pour construire un graphique).
    ordre_colonnes : list[str]
        L'ordre dans lequel afficher les modalités des colonnes.

    Returns
    -------
    pd.DataFrame
        Tableau de contingence.
    """
    # df = df.drop_duplicates(subset="id_usager")

    tab = (
        pd.crosstab(df[variable], df["grav"], normalize='index')
        .reindex(columns=ordre_colonnes)
        .reindex(index=ordre_lignes)
    )
    return tab


def bar_chart(tc: pd.DataFrame, label: str, titre: str) -> None:
    """Construit un stacked bar chart à partir d'un tableau de contingence.

    Parameters
    ----------
    tc : pd.DataFrame
        Le tableau de contingence.
    label : str
        L'étiquette associée à la variable x.
    titre : str
        Titre que l'on veut afficher pour le graphique.

    Returns
    -------
    None
    """

    n = len(tc.columns)
    colors = [cm.magma(i / (n - 1)) for i in range(n)][::-1]

    fig, ax = plt.subplots(figsize=(10, 6))

    tc.plot(kind="bar", stacked=True, ax=ax, color=colors)

    # Ajout des proportions sur chaque barre
    for bar_stack in ax.containers:
        for bar in bar_stack:
            height = bar.get_height()
            if height > 0.03:  # seuil pour éviter les labels illisibles
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 2,
                    f"{height:.1%}",
                    ha="center", va="center",
                    fontsize=8, color="black"
                )

    plt.xlabel(label)
    plt.ylabel("Gravité")
    plt.title(titre)
    plt.legend(title="Gravité", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def test_chi2(df, variable1, variable2):
    tc = pd.crosstab(df[variable1], df[variable2])
    chi2, p_value, dof, expected = chi2_contingency(tc)
    print(f"Chi² = {chi2:.2f}")
    print(f"p-value = {p_value:.4f}")
    print(f"Degrés de liberté = {dof}")


