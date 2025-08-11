from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from .deps import get_db
import httpx

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])

@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    results = []
    async with httpx.AsyncClient() as client:
        for city in cities:
            temperature = 20.5
            temp_record = crud.add_temperature(db, city.id, temperature)
            results.append(temp_record)
    return results

@router.get("/", response_model=list[schemas.TemperatureRead])
def get_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id)
