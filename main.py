from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from database import engine, get_db, Base
import crud
import fetcher

Base.metadata.create_all(bind=engine)

def scheduled_fetch():
    db = next(get_db())
    try:
        stations = fetcher.fetch_stations()
        crud.seed_stations(db, stations)
        records = fetcher.fetch_records()
        upsert_count = crud.upsert_records(db, records)
        print(f"Fetched and upserted {upsert_count} records")
    except Exception as e:
        print(f"Fetch failed: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_fetch, 'interval', minutes=60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduled_fetch()
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/records")
def get_all_records(db: Session = Depends(get_db)):
    return crud.get_all_records(db)

@app.get("/records/active")
def get_active_records(db: Session = Depends(get_db)):
    return crud.get_active_records(db)

@app.get("/records/{record_id}")
def get_record(record_id: str, db: Session = Depends(get_db)):
    return crud.get_record(db, record_id)

@app.get("/records/station/{station_name}")
def get_records_by_station(station_name: str, db: Session = Depends(get_db)):
    return crud.get_records_by_station(db, station_name)

@app.get("/closures")
def get_all_closures(db: Session = Depends(get_db)):
    return crud.get_all_closures(db)

@app.get("/closures/active")
def get_active_closures(db: Session = Depends(get_db)):
    return crud.get_active_closures(db)
