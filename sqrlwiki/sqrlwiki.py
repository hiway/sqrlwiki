import asyncio
import logging
import os
from asyncio.locks import Event
from pathlib import Path
from signal import SIGHUP
from signal import SIGINT
from signal import SIGTERM
from typing import Optional
from uuid import uuid4

import uvloop
from hypercorn.asyncio import serve as hypercorn_serve
from hypercorn.config import Config as HypercornConfig
from quart import Quart
from quart import redirect
from quart import render_template
from quart import url_for


logger = logging.getLogger(__name__)

app = Quart(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid4().hex)
app.template_folder = Path(__file__).parent.joinpath('templates')
app.static_folder = Path(__file__).parent.joinpath('static')


@app.route('/')
async def index():
    return await render_template('index.html')


def run(bind,
        port,
        shutdown_trigger: Optional[Event] = None,
        use_uvloop: bool = True):
    if use_uvloop:
        logger.debug('Using uvloop')
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    shutdown_trigger = shutdown_trigger or asyncio.Event()

    def _signal_handler(*_):
        print('')
        logger.warning('Shutting down web server')
        shutdown_trigger.set()

    for signal in (SIGHUP, SIGTERM, SIGINT):
        loop.add_signal_handler(signal, _signal_handler)

    hyper_config = HypercornConfig()
    hyper_config.bind = [f'{bind}:{port}']

    logger.info('Starting web server')
    loop.run_until_complete(hypercorn_serve(
        app, hyper_config, shutdown_trigger=shutdown_trigger.wait))


def debug(port):
    app.run(debug=True, port=port)
