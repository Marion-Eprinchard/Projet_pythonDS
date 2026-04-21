import matplotlib.pyplot as plt
from cartiflette import carti_download
import matplotlib.ticker as mtick


def initialisation_carte():
    """
    Récupération des informations pour générer des cartes
    """
    departement_borders = carti_download(
        values=["France"],
        crs=4326,
        borders="DEPARTEMENT",
        vectorfile_format="geojson",
        simplification=50,
        filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
        source="EXPRESS-COG-CARTO-TERRITOIRE",
        year=2022)

    departement_borders = departement_borders.rename(columns={"INSEE_DEP": "dep"})
    return departement_borders


def creation_df_carte(df, blessure=False, an=False):
    """
    Création des cartes à partir des dataframes par departement,
    possibilité de regroupement en fonction de la blessure et/ou de l'année
    """

    if not an:
        if not blessure:
            # nombre par departement
            df_victimes_dep = (
                df
                .groupby("dep")
                .size()
                .reset_index(name="nb_victimes")
            )
            total = df_victimes_dep["nb_victimes"].sum()

            df_victimes_dep["nb_victimes_tot"] = total
            # calcul de la proportion
            df_victimes_dep["proportion"] = df_victimes_dep["nb_victimes"] / total * 100

            df_final = df_victimes_dep

        else:
            # nombre par departement
            df_victimes_total = (
                df
                .groupby("dep")
                .size()
                .reset_index(name="nb_victimes_tot")
            )
            # nombre par departement et gravité
            df_victimes_dep = (
                df
                .groupby(["dep", "grav"])
                .size()
                .reset_index(name="nb_victimes")
            )

            df_final = df_victimes_dep.merge(df_victimes_total, on="dep", how="left")
            # calcul de la proportion
            df_final["proportion"] = df_final["nb_victimes"] / df_final["nb_victimes_tot"] * 100

    else:
        if not blessure:
            # nombre par année
            df_victimes_total = (
                df
                .groupby("an")
                .size()
                .reset_index(name="nb_victimes_tot")
            )
            # nombre par département et année
            df_victimes_dep = (
                df
                .groupby(["dep", "an"])
                .size()
                .reset_index(name="nb_victimes")
            )

            df_final = df_victimes_dep.merge(df_victimes_total, on=["an"], how="left")
            # calcul de la proportion
            df_final["proportion"] = df_final["nb_victimes"] / df_final["nb_victimes_tot"] * 100

        else:
            # nombre pas année et departement
            df_victimes_total = (
                df
                .groupby(["an", "dep"])
                .size()
                .reset_index(name="nb_victimes_tot")
            )
            # nombre par année, département et gravité de l'accident
            df_victimes_dep = (
                df
                .groupby(["an", "dep", "grav"])
                .size()
                .reset_index(name="nb_victimes"))

            df_final = df_victimes_dep.merge(df_victimes_total, on=["an", "dep"], how="left")
            # calcul de la proportion
            df_final["proportion"] = df_final["nb_victimes"] / df_final["nb_victimes_tot"] * 100

    # Jointure avec les données des cartes
    df_carte = initialisation_carte().merge(
        df_final,
        on="dep",
        how="left"
    )

    return df_carte


def carte_departement(df_carte, blessure=None, an=None, ax=None):
    """
    Fonction pour créer une carte en proportion

    df_carte : DataFrame produit par creation_df_carte()
    blessure : None, ou une valeur de gravité (ex : "Tué", "Blessé léger", ...)
    an       : None, ou une année (ex : 2022, ...)
    """

    df_carte = df_carte.copy()

    # Filtre blessure
    if blessure is not None:
        df_carte = df_carte[df_carte["grav"].str.lower() == blessure.lower()]

    # Filtre année
    if an is not None:
        df_carte = df_carte[df_carte["an"] == an]

    # Carte
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    m = df_carte.plot(
            column="proportion",
            cmap="RdBu_r",
            legend=True,
            edgecolor="black",
            linewidth=0.5,
            ax=ax
        )

    # Récupérer la colorbar
    cbar = m.get_figure().axes[-1]

    # Formater en pourcentage
    cbar.yaxis.set_major_formatter(mtick.PercentFormatter())

    # Titre dynamique
    titre = "Proportion de victimes par département"

    if blessure is not None:
        titre += f" – {blessure.lower()}"
    else:
        titre += " – toutes blessures"

    if an is not None:
        titre += f" – année {an}"
    else:
        titre += " – toutes années"

    ax.set_title(titre, fontsize=16)
    ax.axis("off")
