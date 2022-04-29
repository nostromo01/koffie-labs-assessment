import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
import json


from app import routes
from app.models import Vehicle, get_db

app = FastAPI()


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(_, exc):
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}

    for error in exc_json:
        response['message'].append(error['loc'][-1] + f": {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.get('/lookup/{vin}', response_class=JSONResponse)
async def lookup(db: Session = Depends(get_db), vehicle: Vehicle = Depends(Vehicle)):
    return await routes.fetch_vehicle(db, vehicle)


@app.get('/remove/{vin}', response_class=JSONResponse)
async def remove(db: Session = Depends(get_db), vehicle: Vehicle = Depends(Vehicle)):
    return await routes.remove_vehicle(db, vehicle)


@app.get('/export', response_class=FileResponse)
async def export(db: Session = Depends(get_db)):
    return await routes.export_vehicles(db)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
