#!/usr/bin/env python3
import argparse
import logging
import os
from datetime import datetime

import pytz
import toml
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse

import eurlex_api.lib_misc as lm

from .lib_cfg import config
from .utilities import logger

# ################################################### SETUP AND ARGUMENT PARSING
# ##############################################################################
dir_path = os.path.dirname(os.path.realpath(__file__))

VERSION = 10
START_TIME = datetime.now(pytz.utc)

tags_metadata = [
    {
        "name": "search",
        "description": "Search operations",
    }
]

app = FastAPI(root_path=config.key('proxy_prefix'), openapi_tags=tags_metadata)

favicon_path = './static/favicon.ico'


# ############################################################### SERVER ROUTES
# #############################################################################


@app.get("/")
def root():
    return lm.status_get(START_TIME, VERSION)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


# ##################################################################### STARTUP
# #############################################################################
def main():
    parser = argparse.ArgumentParser(description='Matching server process')
    parser.add_argument('--config', dest='config', help='config file', default=None)
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='Debug mode')
    args = parser.parse_args()

    # XXX: Lambda is a hack : toml expects a callable
    if args.config:
        t_config = toml.load(['config_default.toml', args.config])
    else:
        t_config = toml.load('config_default.toml')

    config.merge(t_config)

    if args.debug:
        logger.setLevel(logging.getLevelName('DEBUG'))
        logger.debug('Debug activated')
        config.set('log_level', 'debug')
        config.set(['server', 'log_level'], 'debug')
        logger.debug('Arguments: %s', args)
        config.dump(logger)
        logger.debug('config: %s', toml.dumps(config._config))

        uvicorn.run(
            "eurlex_api.main:app",
            reload=True,
            **config.key('server')
        )
    uvicorn.run(
        app,
        **config.key('server')
    )


if __name__ == "__main__":
    main()
