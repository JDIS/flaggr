#!/bin/bash

sleep 10
flask db upgrade
flask seed
gunicorn --config=gunicorn_config.py jdisctf:app