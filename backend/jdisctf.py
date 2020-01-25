"""Flask app / WSGI entrypoint"""
import click

from JDISCTF import create_app
from seeds.seed import Seeder

app = create_app()


@app.cli.command('seed')
@click.option('-v', '--verbose', is_flag=True)
def perform_seeding(verbose: bool):
    Seeder(verbose).seed()
    exit(0)


if __name__ == "__main__":
    app.run()
