# Copyright (C) 2022 Chintalagiri Shashank
#
# This file is part of Tendril API Server.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Server Configuration Options
============================
"""


from tendril.utils.config import ConfigOption

import logging
logger = logging.getLogger(__name__)

depends = ['tendril.config.core']


config_elements_server = [
    ConfigOption(
        'APISERVER_ENABLED', "True",
        "Whether the API server is to be started. Irrespective of "
        "this configuration option, the API server will still be "
        "constructed normally if the code path is triggered, but the "
        "final server.run() up will be skipped.",
        parser=bool
    ),
    ConfigOption(
        'APISERVER_BIND_IP', "'0.0.0.0'",
        "IP Address the server should bind to. See uvicorn.Server and uvicorn.Config."
    ),
    ConfigOption(
        'APISERVER_PORT', "8039",
        "Port the server should listen on.",
        parser=int
    ),
    ConfigOption(
        'APISERVER_PREFIX', "'/v1'",
        "API Prefix. Not presently used.",
    ),
    ConfigOption(
        'APISERVER_AUTO_RELOAD', "False",
        "Automatically reload the server on changes. This might actually "
        "not have any real effects and probably should be left alone in production.",
        parser=bool
    )
]


config_elements_server_ssl = [
    ConfigOption(
        'APISERVER_ENABLE_SSL', "True",
        "Whether to use TLS/SSL connections.",
        parser=bool
    ),
    ConfigOption(
        'APISERVER_SSL_KEYFILE', "''",
        "Path to the SSL Key to use."
    ),
    ConfigOption(
        'APISERVER_SSL_CERTFILE', "''",
        "Path to the SSL Certificate to use."
    )
]


config_elements_server_security = [
    ConfigOption(
        'APISERVER_CORS_ORIGINS', "['*']",
        "List of CORS Origins."
    ),
    ConfigOption(
        'APISERVER_CORS_METHODS', "['*']",
        "List of CORS Methods."
    ),
    ConfigOption(
        'APISERVER_CORS_HEADERS', "['*']",
        "List of CORS Headers."
    )
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_server,
                          doc="API Server Configuration")
    manager.load_elements(config_elements_server_ssl,
                          doc="API Server SSL Configuration")
    manager.load_elements(config_elements_server_security,
                          doc="API Server Security Configuration")
