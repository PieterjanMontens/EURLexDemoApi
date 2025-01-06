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

from .routers import search, navlist, notice

description = """
The EUR-Lex DEMO API is a testing ground made to explore, understand
 and test up-to-date and state-of-thearet webservice API features and
 methods of content delivery.

- Execute search operations wich reproduce and improve the legacy webservice
- Navigate through document collections
- Configuration of output format
"""

# ################################################### SETUP AND ARGUMENT PARSING
# ##############################################################################
dir_path = os.path.dirname(os.path.realpath(__file__))

VERSION = 10
START_TIME = datetime.now(pytz.utc)

tags_metadata = [
    {
        "name": "search",
        "description": "Query the EUR-Lex search index",
    },
    {
        "name": "list",
        "description": "List contents from various collections or content groups"
    },
    {
        "name": "notice",
        "description": "Resource metadata notice"
    }
]

app = FastAPI(
    title="EUR-Lex REST API",
    description=description,
    root_path=config.key('proxy_prefix'),
    openapi_tags=tags_metadata
)
app.include_router(search.router)
app.include_router(navlist.router)
app.include_router(notice.router)

favicon_path = './static/favicon.ico'


# ############################################################### SERVER ROUTES
# #############################################################################


@app.get("/", include_in_schema=False)
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
    else:
        uvicorn.run(
            app,
            **config.key('server')
        )


if __name__ == "__main__":
    main()
