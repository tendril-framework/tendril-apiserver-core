

from fastapi import APIRouter
from fastapi import Depends

from tendril.authn.users import authn_dependency
from tendril.authn.users import AuthUserModel
from tendril.authn.users import auth_spec


system_monitoring = APIRouter(prefix='/system',
                              tags=["System Monitoring"],
                              dependencies=[Depends(authn_dependency),
                                            auth_spec(scopes=['system:monitoring'])])

system_administration = APIRouter(prefix='/system',
                                  tags=["System Administration"],
                                  dependencies=[Depends(authn_dependency),
                                                auth_spec(scopes=['system:administration'])])


from tendril.utils.versions import get_versions


@system_monitoring.get("/versions", tags=["System Monitoring"])
async def versions(user: AuthUserModel = auth_spec()):
    return {k: v for (k, v) in get_versions('tendril')}


routers = [
    system_monitoring,
    system_administration
]
