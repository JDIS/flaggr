
# Le nom du projet!


## Dev notes - Backend

### postgres

    sudo apt-get install postgresql postgresql-contrib
    sudo su - postgres
    psql -c "CREATE USER jdisctf WITH PASSWORD 'jdisctf'"
    createdb -O jdisctf jdisctf_db

Quand le projet sera dockerized, les valeurs suivantes devront être dans le Dockerfile

    export POSTGRES_URL="127.0.0.1:5432"
    export POSTGRES_USER="jdisctf"
    export POSTGRES_PW="jdisctf"
    export POSTGRES_DB="jdisctf_db"

### venv

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate

### Setup flask (sera automatisé plus tard)

Dans le venv:

    pip install -r requirements.txt

    ./run.sh

### Migration

Pour faire une migration

    flask db migrate -m "Nom de la migration"

Pour appliquer la migration

    flask db upgrade

### Seeding

Pour seeder la database de développement

    flask seed [-v/--verbose]