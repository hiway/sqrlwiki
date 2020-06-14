"""Console script for sqrlwiki."""
import sys
import click

from sqrlwiki.sqrlwiki import debug
from sqrlwiki.sqrlwiki import run

@click.group()
def main(args=None):
    pass


@main.command('run')
@click.option('--bind', default='127.0.0.1')
@click.option('--port', default=7000, type=int)
@click.option('--uvloop/--no-uvloop', default=True, is_flag=True)
def main_run(bind, port, uvloop):
    run(bind=bind, port=port, use_uvloop=uvloop)


@main.command('debug')
@click.option('--port', default=7000, type=int)
def main_debug(port):
    debug(port=port)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
