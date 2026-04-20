import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import chi2_contingency


def compter_par_mois(df, variable, condition_grav=None):
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


def evolution_mensuelle(df):

    accidents = compter_par_mois(df, "Num_Acc")
    usagers = compter_par_mois(df, "id_usager")
    victimes = compter_par_mois(
        df,
        "id_usager",
        condition_grav=["Blessé léger", "Blessé hospitalisé", "Tué"]
    )

    dates = accidents["periode"].dt.to_timestamp()
    labels_xticks = dates.dt.strftime("%b %Y")  # renommé

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(range(len(accidents)), accidents["nb"], label="Accidents")
    ax.plot(range(len(usagers)),   usagers["nb"],   label="Usagers impliqués")
    ax.plot(range(len(victimes)),  victimes["nb"],  label="Victimes non indemnes")

    ax.set_xticks(range(len(accidents)))
    ax.set_xticklabels(labels_xticks, rotation=45, ha="right")  # renommé
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Date")
    ax.set_ylabel("Nombre")
    ax.set_title("Évolution mensuelle des accidents et usagers impliqués")

    handles, labels_legende = ax.get_legend_handles_labels()  # renommé
    ordre_legende = [1, 2, 0]
    ax.legend(
        [handles[i] for i in ordre_legende],
        [labels_legende[i] for i in ordre_legende]
    )

    plt.grid(axis="both")
    plt.tight_layout()
    plt.show()


def nb_accidents_par(df, variable, nom_variable, ordre=None, afficher_nb=False):
    nb_accidents_groupe = df.drop_duplicates(subset="Acc_Num").groupby(variable).size().reset_index("Nombre d'accidents")

    if ordre is not None:
        nb_accidents_groupe = (
            nb_accidents_groupe
            .set_index(variable)
            .reindex(ordre)
            .reset_index()
        )

    bars = plt.bar(nb_accidents_groupe[variable], nb_accidents_groupe["Num_Acc"])

    if afficher_nb:
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{int(height)}",
                ha="center", va="bottom",
                fontsize=9
            )

    plt.grid(which="both", axis="y")
    plt.xticks(nb_accidents_groupe[variable])
    plt.xticks(rotation=45, ha="right")
    plt.xlabel(nom_variable)
    plt.ylabel("Accidents")
    plt.title(f"Nombre d'accidents selon leur {nom_variable.lower()}")
    plt.show()

# def nb_accidents_par(df, variable, nom_variable, afficher_nb=False):
#     nb_accidents_groupe = df.groupby(variable).count().reset_index()

#     bars = plt.bar(nb_accidents_groupe[variable], nb_accidents_groupe["Num_Acc"])

#     # Annotation sur chaque barre
#     if afficher_nb:
#         for bar in bars:
#             height = bar.get_height()
#             plt.text(
#                 bar.get_x() + bar.get_width() / 2,
#                 height,
#                 f"{int(height):_}",
#                 ha="center", va="bottom",
#                 fontsize=9
#             )

#     plt.grid(which="both", axis="y")
#     plt.xticks(nb_accidents_groupe[variable])
#     plt.xticks(rotation=45, ha="right")
#     plt.xlabel(nom_variable)
#     plt.ylabel("Accidents")
#     plt.title(f"Nombre d'accidents selon leur {nom_variable.lower()}")
#     plt.show()


def tab_cont_grav(df, variable, ordre_lignes, ordre_colonnes):
    tab = (
        pd.crosstab(df[variable], df["grav"], normalize='index')
        .reindex(columns=ordre_colonnes)
        .reindex(index=ordre_lignes)
    )
    return tab


def bar_chart(tc, label, titre):

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
