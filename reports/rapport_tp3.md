# TP3 – Introduction à Feast et au Feature Store pour StreamFlow

## Contexte
La table labels permet de savoir quels clients sont partis et lesquels sont restés. (churn True ou False)
Le payments_agg_90d indique si des paiements ont été refusé lors des 90 derniers jours.
La table subscriptions permet de connaître les détails de paiement des abonnés (comme leur montant, la régularité de paiement ou même le service souscrit)
La table support_agg_90d permet de connaître le nombre de ticket et la durée de résolution reçu sur le service apporté aux clients sur les 90 derniers jours.
La table usage_agg_30d indique l'utilisation que fait le client de son abonnement.
Users contient des informations spécifique au client (Sexe, Age...)

Cet ensemble de table nous l'avons sous deux versions. Une image à la date du 2024-01-31 la deuxième à la date du 2024-02-29.
Elles sont stockées sur un conteneur docker postgresql et ingérées grâce au conteneur prefect, leur "propreté" est supervisé grâce à l'utilisation de Great Expectations.

L'objectif de ce tp est de transformer ces données brutes mais propres en features que nous pourrons utiliser lors de l'entraînement de note modèle. Ces features seront accessibles à travers le Feature Store de deux manières, en offline et online. Le premier matérialisera les données historiques pour l'entraînement pour ne pas produire de data leakage. Le deuxième servira les données en temps réel pour les prédictions en temps réel.

## Mise en place de Feast

docker compose up -d --build
Cette commande permet de lancer nos services contenus dans notre docker-compose. Le -d permet de le faire en mode detached qui n'affichera pas les logs des conteneurs. --build permet de forcer la reconstruction complète de l'image.

Puisqu'on a monté notre dossier repo qui contient la configuration du feature store dans le fichier /repo du conteneur, nous allons retrouver le fichier de configuration du feature store dans le fichier feature_store.yaml dans le dossier /repo du conteneur.

Grâce à la configuration et aux scripts python le  docker compose exec feast va pouvoir lancer les commandes feast apply et materialize à l'intérieur du docker pour accéder aux données et effectuer les transformations pour obtenir nos features.

## Définition du Feature Store

Une Entity dans Feast permet d'indiquer les métadonnées relatifs à une feature que nous allons utiliser ensuite dans les feature views.
User_id est pertinent comme clef de jointure dans streamflow car c'est la clef qui est récurrente entre les tables de notre base de données.

Dans la table usage_agg_30d_snapshots, nous pouvons retrouver les données suivantes : watch_hours_30d (nombre d'heures de visionnage), avg_session_mins_7d(la durée moyenne de chaque session sur les 7 derniers jours), unique_devices_30d (le nombre d'appareils différents utilisant le compte), skips_7d, rebuffer_events_7d 

Grâce à feast apply, nous définission la structure des features que nous souhaitons ainsi que leur aggrégation (par table).


## Récupération offline & online

Tout d'abord, j'ai relancé le build pour être sûr d'être àjour sur le conteneur : docker compose up -d --build
Puis, j'ai lancé la commande d'exécution du fichier python : docker compose exec prefect python build_training_dataset.py

Nous récupérons dans le fichier training_df les données suivantes : 
![alt text](image.png)

Nous garantissant le point in time correctness grâce à la variable AS_OF = 2024-01-31 qui donne l'image des données/features que nous souhaitons avoir. A travers une requête SQL : 
SELECT user_id, as_of
    FROM subscriptions_profile_snapshots
    WHERE as_of = %(as_of)s

Celle-ci récupère seulement les données datées du 2024-01-31 avec le WHERE.

Online features for user: 7590-VHVEG
{'user_id': ['7590-VHVEG'], 'monthly_fee': [29.850000381469727], 'paperless_billing': [True], 'months_active': [1]}
Si le user_id n'est pas existant, les valeurs renvoyées seront null comme ici : 
Online features for user: 0001
{'user_id': ['0001'], 'paperless_billing': [None], 'months_active': [None], 'monthly_fee': [None]}


## Réflexion offline & online

{"user_id":"7590-VHVEG","features":{"user_id":"7590-VHVEG","months_active":1,"monthly_fee":29.850000381469727,"paperless_billing":true}}
Cet api nous permet de réduire le training-serving skew étant donné que nous passons par la même transformation des données, ainsi que l'historisation de celles-ci pour de futurs entraînement. Ce qui a pour effet de stabiliser la méthode d'input des données, avoir des features similaires et des prédictions convaincantes.