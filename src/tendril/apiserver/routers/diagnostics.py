

from fastapi import APIRouter
from pydantic import BaseModel

# import os
# from fastapi_auth0 import Auth0, Auth0User
# auth0_domain = os.getenv("AUTH0_DOMAIN")
# auth0_api_audience = os.getenv("AUTH0_AUDIENCE")
# auth = Auth0(domain=auth0_domain,
#              api_audience=auth0_api_audience,
#              scopes={
#                  "upload": "Permission to upload media",
#                  "approve": "Permission to approve media",
#                  "remove": "Permission to remove media",
#                  "delete": "Permission to delete media",
#                  "list": "Permission to list media",
#                  "find": "Permission to find media"
#              })


connection_diagnostics = APIRouter(prefix='diagnostics',
                                   tags="Connection Diagnostics")


class GenericMessage(BaseModel):
    message: str


@connection_diagnostics.post("/echo")
async def echo(message: GenericMessage):
    return {'message': message.message}


@connection_diagnostics.post("/echo-login")
async def echo_login(message: GenericMessage):
    return {'message': message.message}


@connection_diagnostics.post("/echo-scope")
async def echo(message: GenericMessage):
    return {'message': message.message}


routers = [
    connection_diagnostics
]
