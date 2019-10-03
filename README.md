# dev.docker-compose.yml
Contient un service pour la db et un service pour faire les migrations

Pour démarrer les services
```
docker-compose -f dev.docker-compose.yml up
```

Pour appliquer une nouvelle migration
```
docker-compose -f dev.docker-compose.yml up --build
```