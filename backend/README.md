
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

    export FLASK_APP=main.py
    export FLASK_ENV=development
    export POSTGRES_URL="127.0.0.1:5432"
    export POSTGRES_USER="jdisctf"
    export POSTGRES_PW="jdisctf"
    export POSTGRES_DB="jdisctf_db"
    flask run
