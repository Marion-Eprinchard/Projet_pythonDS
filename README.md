# Projet Python pour la Data Science | Analyse et prédiction de la gravité des accidents corporels de la circulation routière

## Présentation

Nous avons cherché à répondre aux problématiques suivantes : *Quels facteurs influencent la gravité ? Peut-on prédire cette dernière en tenant compte des caractéristiques environnementales, géographiques, routières et circonstancielles de l'accident ?*

Vous trouverez dans le fichier principal :
- Un traitement des données, qui a permis de réunir les observations dans une même base en les recodant pour une meilleure lisibilité.
- Une analyse descriptive, qui donne un aperçu du nombre d'accidents et de l'état des usagers impliqués.
- Une modélisation visant à prédire la gravité des accidents.

Cet objectif de prédiction nous a en effet amené à entraîner un modèle de forêt aléatoire (*random forest*) avec les variables pertinentes à notre disposition.

Plusieurs types de facteurs sont entrés en compte dans l'analyse et la prédiction.
- Environnement de conduite : luminosité, conditions atmosphériques, condition de la surface (pouvant relever de paramètres météorologiques comme les précipitations).
- Conditions routières : catégorie de route, type d'intersection, sens de circulation.
- Caractéristiques de l'accident : collision, obstacle heurté. 

Ce projet utilise les bases de données annuelles des accidents corporels de la circulation routière (BAAC) pour les années 2022 à 2024, publiées par le ministère de l'Intérieur sur le site data.gouv.fr : https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024

## Données

La base de données finale comportait 

## Fichiers

## Guide d'utilisation

Les packages utilisés et leurs versions respectives sont listées dans le fichier `requirements.txt` et peuvent être directement installés en exécutant la commande suivante dans le terminal :

`pip install -r requirements.txt`

Attention, l'exécution d'une telle commande risque de modifier votre environnement.

Une fois les packages installés, vous pouvez exécuter le fichier `main.ipynb`. 