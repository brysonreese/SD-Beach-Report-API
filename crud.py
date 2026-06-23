from sqlalchemy.orm import Session
from sqlalchemy import desc, update
from sqlalchemy.dialects.sqlite import insert
from models import Advisory, Station
from datetime import datetime

def parse_date_from_string(date_string):
    if date_string is None:
        return date_string
    return datetime.strptime(date_string, "%Y-%m-%d").date()

def get_all_advisories(db: Session):
    return db.query(Advisory).all()

def get_advisory(db: Session, advisory_id: str):
    return db.query(Advisory).filter(Advisory.id == advisory_id).first()

def get_active_advisories(db: Session):
    return db.query(Advisory).filter(Advisory.active == True).all()

def get_advisories_by_station(db: Session, station_name: str):
    return db.query(Advisory).filter(Advisory.station_name == station_name).all()

def get_latest_advisory_by_station(db: Session, station_name: str):
    return db.query(Advisory).filter(Advisory.station_name == station_name).order_by(desc(Advisory.start_date)).first()

def get_all_closures(db: Session):
    return db.query(Advisory).filter(Advisory.type == "Closure").all()

def get_active_closures(db: Session):
    return db.query(Advisory).filter(Advisory.active == True).filter(Advisory.type == "Closure").all()

def get_all_stations(db: Session):
    return db.query(Station).all()

def upsert_advisories(db: Session, advisories: list):
    count = 0
    
    for advisory in advisories:
        stmt = insert(Advisory).values(
            id=str(advisory['id']),
            description=advisory.get('Description'),
            station_description=advisory.get('StationDescription'),
            beach_name=advisory.get('Beach Name'),
            latitude=advisory.get('Latitude'),
            longitude=advisory.get('Longitude'),
            extent_start=advisory.get('Extent Start'),
            extent_start_type=advisory.get('Extent Start Type'),
            extent_end=advisory.get('Extent End'),
            extent_end_type=advisory.get('Extent End Type'),
            station_name=advisory.get('Station Name'),
            type=advisory.get('Type'),
            cause=advisory.get('Cause'),
            source=advisory.get('Source'),
            substance=advisory.get('Substance'),
            substance_volume=advisory.get('Substance Volume'),
            substance_unit=advisory.get('Substance Unit'),
            start_date=parse_date_from_string(advisory.get('Start Date')),
            start_time=advisory.get('Start Time'),
            end_date=parse_date_from_string(advisory.get('End Date')),
            end_time=advisory.get('End Time'),
            county=advisory.get('County'),
            comments=advisory.get('Comments'),
            enterococcus=advisory.get('Enterococcus'),
            fecal_coliforms=advisory.get('Fecal Coliforms'),
            total_coliforms=advisory.get('Total Coliforms'),
            area_description=advisory.get('Area Description'),
            active=advisory.get('End Date') is None
        ).on_conflict_do_update(
            index_elements=['id'],
            set_=dict(
                description=advisory.get('Description'),
                station_description=advisory.get('StationDescription'),
                beach_name=advisory.get('Beach Name'),
                latitude=advisory.get('Latitude'),
                longitude=advisory.get('Longitude'),
                extent_start=advisory.get('Extent Start'),
                extent_start_type=advisory.get('Extent Start Type'),
                extent_end=advisory.get('Extent End'),
                extent_end_type=advisory.get('Extent End Type'),
                station_name=advisory.get('Station Name'),
                type=advisory.get('Type'),
                cause=advisory.get('Cause'),
                source=advisory.get('Source'),
                substance=advisory.get('Substance'),
                substance_volume=advisory.get('Substance Volume'),
                substance_unit=advisory.get('Substance Unit'),
                start_date=parse_date_from_string(advisory.get('Start Date')),
                start_time=advisory.get('Start Time'),
                end_date=parse_date_from_string(advisory.get('End Date')),
                end_time=advisory.get('End Time'),
                county=advisory.get('County'),
                comments=advisory.get('Comments'),
                enterococcus=advisory.get('Enterococcus'),
                fecal_coliforms=advisory.get('Fecal Coliforms'),
                total_coliforms=advisory.get('Total Coliforms'),
                area_description=advisory.get('Area Description'),
                active=advisory.get('End Date') is None
            )
        )
        db.execute(stmt)
        count += 1

    db.commit()
    return count

def upsert_stations(db: Session, stations: list):
    for station in stations:
        stmt = insert(Station).values(
            station_name = station
        ).on_conflict_do_nothing()
        db.execute(stmt)
    
        advisory = get_latest_advisory_by_station(db, station)
        if advisory is None:
            continue

        stmt = update(Station).where(Station.station_name == station).values(
            beach_name = advisory.beach_name,
            station_description = advisory.station_description,
            latitude = advisory.latitude,
            longitude = advisory.longitude,
            area_description = advisory.area_description,
            county = advisory.county
        )

        db.execute(stmt)
    db.commit()
