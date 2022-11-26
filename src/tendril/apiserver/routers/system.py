


from fastapi import APIRouter


system_monitoring = APIRouter(prefix='system',
                              tags="System Monitoring")

system_administration = APIRouter(prefix='system',
                                  tags="System Administration")


from tendril.utils.versions import get_versions


@system_monitoring.get("/versions", tags=["System Monitoring"])
async def versions():
    return {k: v for (k, v) in get_versions('tendril')}


routers = [
    system_monitoring,
    system_administration
]
