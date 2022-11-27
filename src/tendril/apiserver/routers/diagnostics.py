

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from tendril.authn import authn_dependency
from tendril.authn import AuthUserModel
from tendril.authn import auth_spec


connection_diagnostics = APIRouter(prefix='/diagnostics',
                                   tags=["Connection Diagnostics"])


class GenericMessage(BaseModel):
    message: str


@connection_diagnostics.post("/echo")
async def echo(message: GenericMessage):
    return {'message': message.message}


@connection_diagnostics.post("/echo-login", dependencies=[Depends(authn_dependency)])
async def echo_login(message: GenericMessage,
                     user: AuthUserModel = auth_spec()):
    return {'message': message.message}


@connection_diagnostics.post("/echo-scope", dependencies=[Depends(authn_dependency)])
async def echo_scoped(message: GenericMessage,
                      user: AuthUserModel = auth_spec(scopes=['system:administration'])):
    return {'message': message.message}


routers = [
    connection_diagnostics
]
