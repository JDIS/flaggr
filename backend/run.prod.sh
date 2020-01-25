#!/bin/bash

sleep 10
source .env
flask db upgrade
flask seed
gunicorn --config=gunicorn_config.py jdisctf:app