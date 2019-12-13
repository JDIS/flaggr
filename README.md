# Flaggr

## Qu'est-ce que Flaggr ?

Flaggr est une plateforme de gestion de compétitions informatiques de styles variés. Elle a été dévoloppée avec comme objectif de créer une plateforme qui pourrait répondre aux besoins du plus grand nombre de compétitions possible, tout en restant simple à utiliser et configurer.

## Pourquoi Flaggr ?

Flaggr a été créé à l'origine par un groupe d'étudiants en Sciences Informatique de l'Université de Sherbrooke. Tous avaient organisé et/ou participé à un certain nombres de compétitions informatiques par le passé et trouvaient que celles-ci présentaient certains défis récurrents, tant pour les organisateurs que pour les participants. Voici une liste des principaux irritants qu'ils ont identifié chez les différentes plateformes existantes :

* **Complexes à configurer**

    Plusieurs des plateformes existantes nécessitent une quantité non-négligeable de configuration avant même de pouvoir lancer la compétition. De plus, cette configuration se fait souvent via des fichiers texte, une interface en ligne de commande ou même directement les fichiers source sur le serveur par accès direct, par SSH ou autre.
    
    Nous pensons que cela apporte une complexité inutile qui pourrait être paliée par une **interface d'administration web** agréable et facile à utiliser.

* **Une plateforme, une compétition**

    En plus de la configuration longue et complexe, les autres plateformes ne supportent généralement qu'une seule compétition. Ceci signifie que tout le temps qui a été investi dans la mise en place et la configuration d'une compétition est généralement perdu une fois la compétition terminée et doit être investi de nouveau lors de la prochaine compétition.

    Nous pensons que cela représente une perte de temps énorme, surtout pour les groupes qui organisent plusieurs coméptitions par année, ou même par mois. C'est pourquoi nous avons créé une plateforme qui permet de **gérer autant de compétitions que vous le désirez** sans que cela n'ajoute de complexité supplémentaire pour les organisateurs.

* **Mauvaise gestion des permissions**

    La plupart des compétitions informatiques relèvent du travail commun d'un grand nombre d'individus. Ces différents individus doivent tous avoir accès à la plateforme de gestion, mais dans la plupart des cas, les autres plateformes ne font aucune distinction entre les différents individus qui y ont accès, qu'ils soient *challenge designers*, designers graphiques, ou simplement administrateurs. Ceci peut mener à beaucoup de problèmes et de frustrations quand un *challenge designer* de sécurité décide de corriger ce petit bug visuel sur la page d'acceuil qui traine depuis des semaines, mais finit plutôt par complètement démolir ladite page d'accueil par accident.

    C'est pourquoi Flaggr offre un système de **gestion des permissions par compétition**. Ainsi, les administrateurs principaux d'une compétition peuvent décider de façon granulaire quels organisateurs ont accès à quelle partie de la compétition, réduisant ainsi les risques de bris et de conflits.

* **Mauvaises interfaces**

    Dans bien des cas, les autres plateformes de compétition offrent des interfaces utilisateur qui semblent avoir porté peu de considération pour l'expérience utilisateur de l'application, que l'on parle d'ergonomie, de simplicité ou tout simplement d'attrait visuel. Ces interfaces mal adaptées causent une expérience peu agréable et parfois même ardue pour les participants de la compétition, laquelle sera malheureusement associée à la compétition elle-même et pourra en faire souffrir sa réputation.

    Flaggr propose plutôt une **interface web simple, moderne et réactive** qui vise à rendre l'utilisation de la plateforme la plus simple et la plus agréable possible.

## Déploiement

### Dépendances

La seule dépendance pour le déploienent de la plateforme est [Docker](https://www.docker.com/) (et [Docker-Compose](https://docs.docker.com/compose/), généralement inclut avec Docker).

Une fois Docker installé, il suffit d'exécuter les commandes suivantes :

```bash
git clone git@depot.dinf.usherbrooke.ca:projets/a19/eq17/jdis.git
cd jdis
docker-compose up
```

Si votre environnement de déploiement ne dispose pas de Git, il est possible d'installer la plateforme à l'aide des commandes suivantes:

```bash
wget "https://depot.dinf.usherbrooke.ca/projets/a19/eq17/jdis/-/archive/master/jdis-master.tar.gz"
tar xzf jdis-master.tar.gz
cd jdis-master
docker-compose up
```

Pour que les différents services qui composent l'application puissent être créés correctement, les ports 80 et 443 (serveur web nginx) devront être disponibles sur le serveur, de même que le port 5432 (PostgreSQL).

### Contributions

Les dépendances, procédures et normes de contribution au projet sont détaillées dans leurs fichiers respectifs :

* [Backend](backend/README.md)
* [Frontend](frontend/README.md)
