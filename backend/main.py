"""Flask app / WSGI entrypoint"""

from JDISCTF import create_app
from seeds import seed
import click

app = create_app()


@app.cli.command('seed')
@click.option('-v', '--verbose', is_flag=True)
def perform_seeding(verbose: bool):
    seed(verbose)
