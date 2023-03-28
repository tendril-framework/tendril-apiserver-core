

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


from tendril import config
from tendril.utils.versions import get_versions


@system_monitoring.get("/versions")
async def versions():
    return {k: v for (k, v) in get_versions('tendril')}


@system_monitoring.get("/config")
async def tendril_config():
    return config.json_render()


routers = [
    system_monitoring,
    system_administration
]
