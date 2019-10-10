"""Flask app / WSGI entrypoint"""

from JDISCTF import create_app
from seeds import seed

app = create_app()


@app.cli.command('seed')
def perform_seeding():
    seed()
