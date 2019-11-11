#!/bin/sh

export FLASK_APP=main.py
export FLASK_ENV=development
export POSTGRES_URL="127.0.0.1:5432"
export POSTGRES_USER="jdisctf"
export POSTGRES_PW="jdisctf"
export POSTGRES_DB="jdisctf_db"
flask seed