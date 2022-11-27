

import os
import importlib

from uvicorn import Config, Server
from fastapi.middleware.cors import CORSMiddleware

from tendril.config import INSTANCE_ROOT
from tendril.apiserver.core import apiserver
from tendril.utils.versions import get_namespace_package_names

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


core_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)


def server_basic_options():
    from tendril.config import APISERVER_BIND_IP
    from tendril.config import APISERVER_PORT
    from tendril.config import APISERVER_AUTO_RELOAD

    return {
        "host": APISERVER_BIND_IP,
        "port": APISERVER_PORT,
        "reload": APISERVER_AUTO_RELOAD,
    }


def _default_certificates():
    return {
        'ssl_keyfile': os.path.join(core_dir, 'resources', 'test_key.pem'),
        'ssl_certfile': os.path.join(core_dir, 'resources', 'test_certificate.pem'),
    }


def server_ssl_options():
    from tendril.config import APISERVER_ENABLE_SSL
    if not APISERVER_ENABLE_SSL:
        return {}

    from tendril.config import APISERVER_SSL_KEYFILE
    from tendril.config import APISERVER_SSL_CERTFILE

    if not APISERVER_SSL_KEYFILE or not APISERVER_SSL_CERTFILE:
        logger.warning("APISERVER_ENABLE_SSL is True but APISERVER_SSL_KEYFILE and/or "
                       "APISERVER_SSL_CERTFILE not set. Falling back to built-in test certificates.")
        return _default_certificates()

    if not os.path.isabs(APISERVER_SSL_KEYFILE):
        APISERVER_SSL_KEYFILE = os.path.join(INSTANCE_ROOT, APISERVER_SSL_KEYFILE)
    if not os.path.isabs(APISERVER_SSL_CERTFILE):
        APISERVER_SSL_CERTFILE = os.path.join(INSTANCE_ROOT, APISERVER_SSL_CERTFILE)

    if not os.path.exists(APISERVER_SSL_KEYFILE) or not os.path.exists(APISERVER_SSL_CERTFILE):
        logger.warning("Configured APISERVER_SSL_KEYFILE and/or APISERVER_SSL_CERTFILE not found. "
                       "Falling back to built-in test certificates.")
        return _default_certificates()

    return {
        'ssl_keyfile': APISERVER_SSL_KEYFILE,
        'ssl_certfile': APISERVER_SSL_CERTFILE
    }


def prepare_app():
    from tendril.config import APISERVER_CORS_ORIGINS
    from tendril.config import APISERVER_CORS_METHODS
    from tendril.config import APISERVER_CORS_HEADERS

    apiserver.add_middleware(
        CORSMiddleware,
        allow_origins=APISERVER_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=APISERVER_CORS_METHODS,
        allow_headers=APISERVER_CORS_HEADERS
    )


def install_routers():
    for p in get_namespace_package_names('tendril.apiserver.routers'):
        try:
            m = importlib.import_module(p)
            for router in m.routers:
                logger.info("Loading API router on {0} from {1}".format(router.prefix, p))
                apiserver.include_router(router)
        except ImportError:
            raise


def run_server():
    server_opts = server_basic_options()
    server_opts.update(server_ssl_options())

    prepare_app()
    install_routers()

    server = Server(
        Config(
            apiserver,
            **server_opts
        ),
    )
    server.run()
