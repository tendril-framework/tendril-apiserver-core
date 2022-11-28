import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from tendril.authn import authn_dependency
from tendril.authn import AuthUserModel
from tendril.authn import auth_spec

from tendril.config import AUTH0_DOMAIN, AUTH0_USER_MANAGEMENT_API_CLIENTID, AUTH0_USER_MANAGEMENT_API_CLIENTSECRET

from auth0.v3.management import Auth0
from auth0.v3.authentication import GetToken

from tendril.utils import log

logger = log.get_logger(__name__, log.DEBUG)

file_management = APIRouter(prefix='/file-management',
                            tags=["File Management"])


class UserID(BaseModel):
    user_id: str


@file_management.post("/user-info")
async def user_info(user_id: UserID):
    domain = AUTH0_DOMAIN
    non_interactive_client_id = AUTH0_USER_MANAGEMENT_API_CLIENTID
    non_interactive_client_secret = AUTH0_USER_MANAGEMENT_API_CLIENTSECRET

    try:
        logger.debug("Attempting to get the management API token using:")
        logger.debug("Domain: {}".format(domain))
        logger.debug("Client ID: {}".format(non_interactive_client_id))
        logger.debug("Client Secret ending in {}".format(non_interactive_client_secret[-5:]))
        get_token = GetToken(domain)
        token = get_token.client_credentials(non_interactive_client_id,
                                             non_interactive_client_secret, 'https://{}/api/v2/'.format(domain))
        mgmt_api_token = token['access_token']
        logger.debug("Successfully received Management API token ending in {}".format(mgmt_api_token[-5:]))

    except Exception as exception:
        logger.error(exception)
        logger.error("Could not fetch M2M token for Auth0 Management API, please check the credentials and "
                     "permissions before trying again.")
        raise HTTPException(status_code=500)

    try:
        logger.debug("Attempting to fetch user information from the Management API")
        auth0 = Auth0(domain, mgmt_api_token)
        user_details = auth0.users.get(user_id.user_id)
        logger.debug("Successfully fetched user details from the Management API\n" + json.dumps(user_details, indent=2))
        return {"message": user_details}

    except Exception as exception:
        logger.error(exception)
        logger.error("Could not fetch user information for user_id \"{}\"."
                     "Check the details and try again.".format(user_id.user_id))
        raise HTTPException(status_code=500)

routers = [
    file_management
]
