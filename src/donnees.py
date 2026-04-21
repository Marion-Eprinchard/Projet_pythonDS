import pandas as pd


def lecture(nom_fichier_csv):
    """
    Lecture des fichiers de données en dataframe
    """
    df = pd.read_csv(nom_fichier_csv, sep=';', encoding='UTF-8')
    return df


def import_donnees():
    """
    Importation des fichiers de données

    Retour : dictionnaire des données des 4 fichiers
    """
    urls = {
        "caract": {
            24: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2024/20251021-115900/"
                 "caract-2024.csv"),
            23: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2023/20241028-103125/"
                 "caract-2023.csv"),
            22: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20231005-093927/"
                 "carcteristiques-2022.csv")
        },
        "lieux": {
            24: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2024/20251021-115812/"
                 "lieux-2024.csv"),
            23: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2023/20241023-153219/"
                 "lieux-2023.csv"),
            22: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20231005-094112/"
                 "lieux-2022.csv")
        },
        "vehicule": {
            24: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2024/20251107-100240/"
                 "vehicules-2024.csv"),
            23: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2023/20241023-153253/"
                 "vehicules-2023.csv"),
            22: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20231005-094147/"
                 "vehicules-2022.csv")
        },
        "usager": {
            24: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2024/20251021-115506/"
                 "usagers-2024.csv"),
            23: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2023/20241023-153328/"
                 "usagers-2023.csv"),
            22: ("https://static.data.gouv.fr/resources/bases-de-donnees-annuelles-des-accidents-"
                 "corporels-de-la-circulation-routiere-annees-de-2005-a-2021/20231005-094229/"
                 "usagers-2022.csv")
        }
    }

    donnees_completes = {}

    # Transformation de chaque url de données
    for table, annees in urls.items():
        donnees_completes[table] = {}
        for annee, url in annees.items():
            donnees_completes[table][annee] = lecture(url)

    return donnees_completes


def renomer_cle_jointure(nom_table, nouveau_nom, ancien_nom):
    """
    Renommer la clé de jointure
    """
    df = nom_table.rename(columns={ancien_nom: nouveau_nom})
    return df


def concatenation_annees(donnees, table, annees=[24, 23, 22]):
    """
    Concaténation des 3 années 2022, 2023 et 2024

    donnees : dictionnaire
    table : nom du fichier (caract, lieux, vehicule, usager)
    """
    return pd.concat([donnees[table.lower()][a] for a in annees], ignore_index=True)
