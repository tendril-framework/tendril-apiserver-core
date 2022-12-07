

import json

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from tendril.authn.users import authn_dependency
from tendril.authn.users import AuthUserModel
from tendril.authn.users import auth_spec
from tendril.authn.users import get_user_profile

from tendril.utils import log
logger = log.get_logger(__name__, log.DEBUG)

connection_diagnostics = APIRouter(prefix='/diagnostics',
                                   tags=["Connection Diagnostics"])


class GenericMessage(BaseModel):
    message: str


@connection_diagnostics.post("/echo")
async def echo(message: GenericMessage):
    logger.debug("Got Incoming Test Message : {}".format(message))
    return {'message': message.message}


@connection_diagnostics.post("/echo-login", dependencies=[Depends(authn_dependency)])
async def echo_login(message: GenericMessage,
                     user: AuthUserModel = auth_spec()):
    user_profile = get_user_profile(user)
    logger.debug("Got Incoming Test Message : {}".format(message))
    logger.debug("      from logged in user : {}".format(user.id))
    logger.debug("               with email : {}".format(user.email))
    logger.debug(json.dumps(user_profile, indent=2))
    return {
        'user-profile': user_profile,
        'message': message.message
    }


@connection_diagnostics.post("/echo-scope", dependencies=[Depends(authn_dependency)])
async def echo_scoped(message: GenericMessage,
                      user: AuthUserModel = auth_spec(scopes=['system:administration'])):
    user_profile = get_user_profile(user)
    logger.debug("Got Incoming Test Message : {}".format(message))
    logger.debug("      from logged in User : {}".format(user.id))
    logger.debug("               with email : {}".format(user.email))
    logger.debug("              with scopes : {}".format(user.permissions))
    logger.debug(json.dumps(user_profile, indent=2))
    return {
        'user-profile': user_profile,
        'message': message.message
    }


routers = [
    connection_diagnostics
]
