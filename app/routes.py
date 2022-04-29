import pandas as pd
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from app import utils, constants
from app.models import Vehicle, get_vehicle, create_vehicle, drop_vehicle, get_vehicles


async def fetch_vehicle(db: Session, vehicle: Vehicle) -> JSONResponse:
    """
    Fetches a vehicle.
        - First, checks the cache to see if it exists, returning cached value if found
        - Otherwise, fetches Vehicle information from API, saves it to the database and returns it in response

    :param db: Database session
    :param vehicle: Vehicle object
    :return: JSON Response based on success or failure state
    """
    if cached_vehicle := get_vehicle(db, vehicle.vin):
        cached_vehicle.cached = True
        return cached_vehicle

    try:
        vehicle = utils.fetch_from_api(vehicle.vin)
        create_vehicle(db, vehicle)
        return JSONResponse(vehicle.dict())
    except ValueError as e:
        response = {"message": repr(e), "data": None}
        return JSONResponse(response, status_code=422)
    except Exception as e:
        response = {"message": repr(e), "data": None}
        return JSONResponse(response, status_code=408)


async def remove_vehicle(db: Session, vehicle: Vehicle) -> JSONResponse:
    """
    Removes a vehicle from the cache, if one exists
        - If no vehicle found in cache, 'deleted' key will be false. Otherwise, it is true.

    :param db: Database session
    :param vehicle: Vehicle object
    :return: JSON Response based on success or failure state
    """
    result = drop_vehicle(db, vehicle.vin)
    return JSONResponse({"deleted": result, "vin": vehicle.vin})


async def export_vehicles(db: Session) -> FileResponse:
    """
    Exports all database entries to binary parquet file for download

    :param db: Database session
    :return: FileResponse to allow client to download exported database
    """
    vehicles = get_vehicles(db)
    df = pd.DataFrame(
        {i: j.__dict__ for i, j in enumerate(vehicles)}
    ).T.drop(columns='_sa_instance_state')
    df.to_parquet(constants.EXPORT_FILENAME, engine='fastparquet')
    return FileResponse(constants.EXPORT_FILENAME, filename=constants.EXPORT_FILENAME)
