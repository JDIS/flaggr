import gunicorn

workers = 4
threads = 4
bind = "0.0.0.0:8080"
accesslog = "-"
gunicorn.SERVER_SOFTWARE = "None"
