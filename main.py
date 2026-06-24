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
        advisories = fetcher.fetch_advisories()
        stations_count = crud.upsert_stations(db, stations)
        advisories_count = crud.upsert_advisories(db, advisories)
        print(f"Fetched and upserted {advisories_count} advisories and {stations_count} stations")
    except Exception as e:
        print(f"Fetch failed: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_fetch, 'interval', minutes=15)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduled_fetch()
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/advisories")
def get_all_advisories(db: Session = Depends(get_db)):
    return crud.get_all_advisories(db)

@app.get("/advisories/active")
def get_active_advisories(db: Session = Depends(get_db)):
    return crud.get_active_advisories(db)

@app.get("/advisories/{advisory_id}")
def get_advisory(advisory_id: str, db: Session = Depends(get_db)):
    return crud.get_advisory(db, advisory_id)

@app.get("/advisories/station/{station_name}")
def get_advisories_by_station(station_name: str, db: Session = Depends(get_db)):
    return crud.get_advisories_by_station(db, station_name)

@app.get("/closures")
def get_all_closures(db: Session = Depends(get_db)):
    return crud.get_all_closures(db)

@app.get("/closures/active")
def get_active_closures(db: Session = Depends(get_db)):
    return crud.get_active_closures(db)

@app.get("/stations")
def get_all_stations(db: Session = Depends(get_db)):
    return crud.get_all_stations(db)

@app.get("/beach_status")
def get_all_beach_statuses(db: Session = Depends(get_db)):
    return crud.get_all_beach_statuses(db)
