import pandas as pd
from datetime import date
import numpy as np


# Fonction pour le recodage
def recodage(df, mapping):
    """
    Recodage du noms des variables

    df : dataframe a renommer
    mapping : table du dictionnaire avec le recodage
    """
    df2 = df.copy()
    for col, dic in mapping.items():
        df2[col] = df2[col].map(dic)
    return df2


def creation_mois_num(df):
    """
    """
    df["mois_num"] = df["mois"]
    return df


def mapping_renommer_colonnes():
    # MAPPING
    # caracteristique
    nouveau_mois = {
        1: "janvier",
        2: "février",
        3: "mars",
        4: "avril",
        5: "mai",
        6: "juin",
        7: "juillet",
        8: "août",
        9: "septembre",
        10: "octobre",
        11: "novembre",
        12: "décembre"
    }

    nouveau_lum = {
        1: "Plein jour",
        2: "Crépuscule ou aube",
        3: "Nuit sans éclairage public",
        4: "Nuit avec éclairage public non allumé",
        5: "Nuit avec éclairage public allumé"
    }

    nouveau_agg = {
        1: "Hors agglomération",
        2: "En agglomération"
    }

    nouveau_int = {
        1: "Hors intersection",
        2: "Intersection en X",
        3: "Intersection en T",
        4: "Intersection en Y",
        5: "Intersection à plus de 4 branches",
        6: "Giratoire",
        7: "Place",
        8: "Passage à niveau",
        9: "Autre intersection"
    }

    nouveau_atm = {
        -1: np.nan,
        1: "Normale",
        2: "Pluie légère",
        3: "Pluie forte",
        4: "Neige - grêle",
        5: "Brouillard - fumée",
        6: "Vent fort - tempête",
        7: "Temps éblouissant",
        8: "Temps couvert",
        9: "Autre"
    }

    nouveau_col = {
        -1: np.nan,
        1: "Deux véhicules - frontale",
        2: "Deux véhicules - par l'arrière",
        3: "Deux véhicules - par le côté",
        4: "Trois véhicules - en chaîne",
        5: "Trois véhicules - collisions multiples",
        6: "Autre collision",
        7: "Sans collision"
    }

    # lieux
    nouveau_catr = {
        1: "Autoroute",
        2: "Route nationale",
        3: "Route départementale",
        4: "Voie communale",
        5: "Hors réseau public",
        6: "Parc de stationnement ouvert à la circulation publique",
        7: "Route de métropole urbaine",
        9: "Autre"
    }

    nouveau_circ = {
        -1: np.nan,
        1: "À sens unique",
        2: "Bidirectionnelle",
        3: "À chaussées séparées",
        4: "Avec voies d'affectation variable"
    }

    nouveau_vosp = {
        -1: np.nan,
        0: "Sans objet",
        1: "Piste cyclable",
        2: "Bande cyclable",
        3: "Voie réservée"
    }

    nouveau_prof = {
        -1: np.nan,
        1: "Plat",
        2: "Pente",
        3: "Sommet de côte",
        4: "Bas de côte"
    }

    nouveau_plan = {
        -1: np.nan,
        1: "Partie rectiligne",
        2: "En courbe à gauche",
        3: "En courbe à droite",
        4: "En « S »"
    }

    nouveau_surf = {
        -1: np.nan,
        1: "Normale",
        2: "Mouillée",
        3: "Flaques",
        4: "Inondée",
        5: "Enneigée",
        6: "Boue",
        7: "Verglacée",
        8: "Corps gras - Huile",
        9: "Autre"
    }

    nouveau_infra = {
        -1: np.nan,
        0: "Aucun",
        1: "Souterrain - Tunnel",
        2: "Pont - Autopont",
        3: "Bretelle d'échangeur ou de raccordement",
        4: "Voie ferrée",
        5: "Carrefour aménagé",
        6: "Zone piétonne",
        7: "Zone de péage",
        8: "Chantier",
        9: "Autre"
    }

    nouveau_situ = {
        -1: np.nan,
        0: "Aucun",
        1: "Sur chaussée",
        2: "Sur bande d'arrêt d'urgence",
        3: "Sur accotement",
        4: "Sur trottoir",
        5: "Sur piste cyclable",
        6: "Sur autre voie spéciale",
        8: "Autre"
    }

    # vehicule
    catv_dict = {
        00: "Indéterminable",
        1: "Bicyclette",
        2: "Cyclomoteur",
        3: "Voiturette",
        4: "Scooter",
        5: "Motocyclette",
        6: "Side-car",
        7: "VL",
        8: "VL",
        9: "VL",
        10: "VU",
        11: "VU",
        12: "VU",
        13: "PL",
        14: "PL",
        15: "PL",
        16: "Tracteur routier",
        17: "Tracteur routier",
        18: "Transport en commun",
        19: "Tramway",
        20: "Engin spécial",
        21: "Tracteur agricole",
        30: "Scooter",
        31: "Motocyclette",
        32: "Scooter",
        33: "Motocyclette",
        34: "Scooter",
        35: "Quad",
        36: "Quad",
        37: "Autobus",
        38: "Autocar",
        39: "Train",
        40: "Tramway",
        41: "3RM",
        42: "3RM",
        43: "3RM",
        50: "EDP à moteur",
        60: "EDP sans moteur",
        80: "VAE",
        99: "Autre véhicule"
    }

    choc_dict = {
        -1: np.nan,
        0: "Aucun",
        1: "Avant",
        2: "Avant droit",
        3: "Avant gauche",
        4: "Arrière",
        5: "Arrière droit",
        6: "Arrière gauche",
        7: "Côté droit",
        8: "Côté gauche",
        9: "Chocs multiples (tonneaux)"
    }

    manv_dict = {
        -1: np.nan,
        0: "Inconnue",
        1: "Sans changement de direction",
        2: "Même sens, même file",
        3: "Entre 2 files",
        4: "En marche arrière",
        5: "A contresens",
        6: "En franchissant le terre-plein central",
        7: "Dans le couloir bus, dans le même sens",
        8: "Dans le couloir bus, dans le sens inverse",
        9: "En s’insérant",
        10: "En faisant demi-tour sur la chaussée",

        11: "Changeant  de file",
        12: "Changeant  de file",

        13: "Déporté",
        14: "Déporté",

        15: "Tournant",
        16: "Tournant",

        17: "Dépassant",
        18: "Dépassant",

        # Divers
        19: "Traversant la chaussée",
        20: "Manœuvre de stationnement",
        21: "Manœuvre d’évitement",
        22: "Ouverture de porte",
        23: "Arrêté (hors stationnement)",
        24: "En stationnement",
        25: "Circulant sur trottoir",
        26: "Autres manœuvres"

    }

    obs_dict = {
        -1: np.nan,
        0: "Sans objet",
        1: "Véhicule en stationnement",
        2: "Arbre",
        3: "Glissière métallique",
        4: "Glissière béton",
        5: "Autre glissière",
        6: "Bâtiment, mur, pile de pont",
        7: "Support de signalisation verticale ou poste d’appel d’urgence",
        8: "Poteau",
        9: "Mobilier urbain",
        10: "Parapet",
        11: "Ilot, refuge, borne haute",
        12: "Bordure de trottoir",
        13: "Fossé, talus, paroi rocheuse",
        14: "Autre obstacle fixe sur chaussée",
        15: "Autre obstacle fixe sur trottoir ou accotement",
        16: "Sortie de chaussée sans obstacle",
        17: "Buse – tête d’aqueduc"
    }

    obsm_dict = {
        -1: np.nan,
        0: "Aucun",
        1: "Piéton",
        2: "Véhicule",
        4: "Véhicule sur rail",
        5: "Animal domestique",
        6: "Animal sauvage",
        9: "Autre"
    }

    # usager
    catu_dict = {
        1: "Conducteur",
        2: "Passager",
        3: "Piéton"
    }

    grav_dict = {
        1: "Indemne",
        2: "Tué",
        3: "Blessé hospitalisé",
        4: "Blessé léger"
    }

    sexe_dict = {
        1: "Homme",
        2: "Femme"
    }

    trajet_dict = {
        -1: np.nan,
        0: np.nan,
        1: "Domicile - Travail",
        2: "Domicile - École",
        3: "Courses - achats",
        4: "Utilisation professionnelle",
        5: "Promenade - loisirs",
        9: "Autre"
    }

    secu_dict = {
        -1: np.nan,
        0: "Aucun équipement",
        1: "Ceinture",
        2: "Casque",
        3: "Dispositif enfants",
        4: "Gilet réfléchissant",
        5: "Airbag (2RM/3RM)",
        6: "Gants (2RM/3RM)",
        7: "Gants + Airbag (2RM/3RM)",
        8: "Non déterminable",
        9: "Autre"
    }

    return {
        "caract": {
            "mois": nouveau_mois,
            "lum": nouveau_lum,
            "agg": nouveau_agg,
            "int": nouveau_int,
            "atm": nouveau_atm,
            "col": nouveau_col
        },
        "lieux": {
            "catr": nouveau_catr,
            "circ": nouveau_circ,
            "vosp": nouveau_vosp,
            "prof": nouveau_prof,
            "plan": nouveau_plan,
            "surf": nouveau_surf,
            "infra": nouveau_infra,
            "situ": nouveau_situ
        },
        "vehicule": {
            "catv": catv_dict,
            "choc": choc_dict,
            "manv": manv_dict,
            "obs": obs_dict,
            "obsm": obsm_dict
        },
        "usager": {
            "catu": catu_dict,
            "grav": grav_dict,
            "sexe": sexe_dict,
            "trajet": trajet_dict,
            "secu1": secu_dict,
            "secu2": secu_dict,
            "secu3": secu_dict
        }
    }


# supprimer les colonnes non interressante pour notre problèmatique
def colonnes_a_supprimer():
    return {"com", "adr", "voie", "v1", "v2", "num_veh_x", "senc", "motor", "occutc", "num_veh_y",
            "place", "locp", "actp", "etatp", "vops", "pr", "pr1", "lartpc", "larrout", "secu2",
            "secu3"}


# transformation année de naissance en age
def création_age_usager(df):
    annee_actuel = date.today().year

    df["age"] = annee_actuel - df["an_nais"]
    df["age"] = df["age"].astype("Int64")
    df_new = df.drop(columns=["an_nais"])

    return df_new


# Jointure des 4 df
def jointure(df1, df2, df3, df4):
    df_final = (
        df1
        .merge(df2, on="Num_Acc", how="left")
        .merge(df3, on="Num_Acc", how="left")
        .merge(df4, on=["Num_Acc", "id_vehicule"], how="left")
    )
    df_final["Num_Acc"] = df_final["Num_Acc"].astype("Int64")

    return df_final


def rajout_colonnes(df):
    # colonne date
    df["date"] = pd.to_datetime(df[["an", "mois_num", "jour"]].rename(columns={
        "an": "year",
        "mois_num": "month",
        "jour": "day"
    }))

    jours_semaine = {
        "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
        "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi",
        "Sunday": "Dimanche"
    }

    # jour de la semaine
    df["jour_semaine"] = df["date"].dt.day_name().map(jours_semaine)

    # heure
    df["hr"] = df["hrmn"].str[0:2]

    return df
