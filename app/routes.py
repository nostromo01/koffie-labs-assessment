import pandas as pd
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.responses import Response, FileResponse

from app import utils
from app.models import Vehicle, get_vehicle, create_vehicle, drop_vehicle, get_vehicles


async def fetch_vehicle(db: Session, vehicle: Vehicle) -> JSONResponse:
    if cached_vehicle := get_vehicle(db, vehicle.vin):
        cached_vehicle.cached = True
        return cached_vehicle

    try:
        vehicle = utils.fetch_from_api(vehicle.vin)
    except ValueError as e:
        response = {"message": repr(e), "data": None}
        return JSONResponse(response, status_code=422)

    create_vehicle(db, vehicle)
    return JSONResponse(vehicle.dict())


async def remove_vehicle(db: Session, vehicle: Vehicle) -> JSONResponse:
    result = drop_vehicle(db, vehicle.vin)
    return JSONResponse({"deleted": result, "vin": vehicle.vin})


async def export_vehicles(db: Session) -> Response:
    file = 'vehicles.parquet'
    vehicles = get_vehicles(db)
    df = pd.DataFrame(
        {i: j.__dict__ for i, j in enumerate(vehicles)}
    ).T.drop(columns='_sa_instance_state')
    df.to_parquet(file, engine='fastparquet')
    return FileResponse(file, filename=file)
