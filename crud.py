from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
from models import Record, Station
from datetime import datetime

def parse_date_from_string(date_string):
    if date_string is None:
        return date_string
    return datetime.strptime(date_string, "%Y-%m-%d").date()

def seed_stations(db: Session, stations: list):
    for station in stations:
        stmt = insert(Station).values(
            station_name = station
        ).on_conflict_do_nothing()
        db.execute(stmt)
    db.commit()

def upsert_records(db: Session, records: list):
    stations = [station.station_name for station in get_all_stations(db)]
    count = 0

    for record in records:
        if record.get('Station Name') not in stations:
            continue
        stmt = insert(Record).values(
            id=str(record['id']),
            description=record.get('Description'),
            station_description=record.get('StationDescription'),
            beach_name=record.get('Beach Name'),
            latitude=record.get('Latitude'),
            longitude=record.get('Longitude'),
            extent_start=record.get('Extent Start'),
            extent_start_type=record.get('Extent Start Type'),
            extent_end=record.get('Extent End'),
            extent_end_type=record.get('Extent End Type'),
            station_name=record.get('Station Name'),
            type=record.get('Type'),
            cause=record.get('Cause'),
            source=record.get('Source'),
            substance=record.get('Substance'),
            substance_volume=record.get('Substance Volume'),
            substance_unit=record.get('Substance Unit'),
            start_date=parse_date_from_string(record.get('Start Date')),
            start_time=record.get('Start Time'),
            end_date=parse_date_from_string(record.get('End Date')),
            end_time=record.get('End Time'),
            county=record.get('County'),
            comments=record.get('Comments'),
            enterococcus=record.get('Enterococcus'),
            fecal_coliforms=record.get('Fecal Coliforms'),
            total_coliforms=record.get('Total Coliforms'),
            area_description=record.get('Area Description'),
            active=record.get('End Date') is None
        ).on_conflict_do_update(
            index_elements=['id'],
            set_=dict(
                description=record.get('Description'),
                station_description=record.get('StationDescription'),
                beach_name=record.get('Beach Name'),
                latitude=record.get('Latitude'),
                longitude=record.get('Longitude'),
                extent_start=record.get('Extent Start'),
                extent_start_type=record.get('Extent Start Type'),
                extent_end=record.get('Extent End'),
                extent_end_type=record.get('Extent End Type'),
                station_name=record.get('Station Name'),
                type=record.get('Type'),
                cause=record.get('Cause'),
                source=record.get('Source'),
                substance=record.get('Substance'),
                substance_volume=record.get('Substance Volume'),
                substance_unit=record.get('Substance Unit'),
                start_date=parse_date_from_string(record.get('Start Date')),
                start_time=record.get('Start Time'),
                end_date=parse_date_from_string(record.get('End Date')),
                end_time=record.get('End Time'),
                county=record.get('County'),
                comments=record.get('Comments'),
                enterococcus=record.get('Enterococcus'),
                fecal_coliforms=record.get('Fecal Coliforms'),
                total_coliforms=record.get('Total Coliforms'),
                area_description=record.get('Area Description'),
                active=record.get('End Date') is None
            )
        )
        db.execute(stmt)
        count += 1

    db.commit()
    return count

def get_all_records(db: Session):
    return db.query(Record).all()

def get_record(db: Session, record_id: str):
    return db.query(Record).filter(Record.id == record_id).first()

def get_active_records(db: Session):
    return db.query(Record).filter(Record.active == True).all()

def get_records_by_station(db: Session, station_name: str):
    return db.query(Record).filter(Record.station_name == station_name).all()

def get_all_closures(db: Session):
    return db.query(Record).filter(Record.type == "Closure").all()

def get_active_closures(db: Session):
    return db.query(Record).filter(Record.active == True).filter(Record.type == "Closure").all()

def get_all_stations(db: Session):
    return db.query(Station).all()
