#!/bin/sh
sleep 10
source .env
flask db upgrade
flask seed
flask run --host=0.0.0.0 --port=8080