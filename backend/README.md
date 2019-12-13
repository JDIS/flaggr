
# Flaggr - Backend

Le backend de Flaggr consiste en un API REST développé en Python 3.7.5 avec Flask 1.1.1.

## Dépendances

La liste complète des dépendances est disponible dans le fichier [requirements.txt](requirements.txt), mais voici un résumé des dépendances principales :

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Flask-rebar](https://flask-rebar.readthedocs.io/en/latest/) : Un plugin Flask qui gère l'intégration avec [Swagger](https://swagger.io/) et [Marshmallow](https://marshmallow.readthedocs.io/en/stable/).
* [Flask-migrate](https://flask-migrate.readthedocs.io/en/latest/) : Un plugin Flask qui gère les migrations de base de données à l'aide de SQLAlchemy et [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Pytest](https://docs.pytest.org/en/latest/)

Pour installer automatiquement l'ensemble des dépendances, exécutez la commande suivante:
```bash
pip install -r requirements.txt
```

## Variables d'environnement

Voice la liste des différentes variables d'environnement dont l'API a besoin pour fonctionner :

* **FLASK_APP**: Le nom de l'application Flask. Doit être `main.py`.
* **FLASK_ENV**: Le type d'environnement dans lequel l'API s'exécute. `development` pour le développement, `production` pour le déploiement en production.
* **POSTGRES_URL**: L'url de connexion à la base de données. Généralement `127.0.0.1:5432` pour le développement.
* **POSTGRES_USER**: Le nom de l'utilisateur que le serveur utilisera pour se connecter à la base de données. Ex: `jdisctf`
* **POSTGRES_PW**: Le mot de passe que le serveur utilisera pour se connecter à la base de données. Ex: `jdisctf`
* **POSTGRES_DB**: Le nom de la base de données à laquelle se connecter. Ex: `jdisctf_db`

## Base de données

La base de données utilisée par le projet est PostgreSQL 10.10. Elle peut être hébergée soit localement ou soit via un conteneur Docker, mais elle doit absolument être accessible avec les paramètres décrits dans les [variables d'environnement](#variables-denvironnement).

## Migrations

Les migrations de la base de données sont situées dans le dossier [migrations/versions](migrations/versions). Elles sont générées automatiquement par Alembic et ne devraient généralement pas être mises à jour manuellement, mais il est possible de le faire si absolument nécessaire.

### Appliquer les migrations

Pour appliquer les migrations existantes, il suffit d'exécuter la commande suivante :
```bash
flask db upgrade
```

Cette commande va automatiquement appliquer toutes les migrations manquantes à la base de données.

### Annuler une migration

Pour annuler une migration, exécutez la commande suivante :
```bash
flask db downgrade
```

Cette commande ne va annuler qu'**une seule migration** à la fois. Pour annuler plusieurs migrations, il est nécessaire d'exécuter la commande plusieurs fois.

### Créer une nouvelle migration

Pour créer une nouvelle migration, exécutez la commande suivante :
```bash
flask db migrate -n "nom de la migration"
```

Cette commande va automatiquement comparer les modèles définis dans le code source avec l'état actuel de la base de données, puis générer une migration pour appliquer les modifications nécessaires. Il est donc important de s'assurer que la base de données soit à jour avant de créer une migration pour éviter d'appliquer certaines modifications en double.

## Populer la base de données

Pour populer la base de données avec des données de test, il suffit d'exécuter la commande suivante :
```
flask seed
```

Il est également possible d'ajouter l'option `-v` ou `--verbose` pour obtenir les détails des opérations effectuées par la commande.

## Démarrer le serveur

Pour démarrer le serveur, il suffit d'exécuter la commande suivante :
```
flask run
```

Cette variable assume que les [variables d'environnement](#variables-denvironnement) sont définies dans votre système. Si vous désirez exécuter le serveur sans enregistrer les variables d'environnement de façon permanente, vous pouvez utiliser le script `run.sh`, qui va automatiquement assigner les variables nécessaires pour le temps de l'exécution.

## Exécuter les tests

Pour exécuter les tests, il suffit d'exécuter la commande suivante:
```bash
pytest
```

La commande va automatiquement détecter et exécuter tous les tests de l'application. Pour n'exécuter qu'une seule partie des tests, il suffit d'ajouter le dossier ou le fichier que vous désirez tester comme argument à la commande. Il est également possible de fournir plusieurs suites de tests à exécuter dans la même commande. Ex:
```bash
pytest JDISCTF/test/unit_tests/api/admin JDISCTF/test/unit_tests/api/test_auth.py
```

## Valider le style

Le style du code n'est validé que dans les dossiers `JDISCTF` et `seeds`. Pour effectuer la validation, il suffit d'exécuter la commande suivante:
```bash
pylint JDISCTF seeds
```

Les paramètres de validation sont définis dans le fichier [pylintrc](./pylintrc)
