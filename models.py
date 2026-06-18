from sqlalchemy import Column, String, Float, Boolean, Date
from database import Base

class Record(Base):
    __tablename__ = "records"

    id = Column(String, primary_key=True)
    description = Column(String, nullable=True)
    station_description = Column(String, nullable=True)
    beach_name = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    extent_start = Column(String, nullable=True)
    extent_start_type = Column(String, nullable=True)
    extent_end = Column(String, nullable=True)
    extent_end_type = Column(String, nullable=True)
    station_name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    cause = Column(String, nullable=True)
    source = Column(String, nullable=True)
    substance = Column(String, nullable=True)
    substance_volume = Column(Float, nullable=True)
    substance_unit = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    start_time = Column(String, nullable=True)
    end_date = Column(Date, nullable=True)
    end_time = Column(String, nullable=True)
    county = Column(String, nullable=True)
    comments = Column(String, nullable=True)
    enterococcus = Column(Float, nullable=True)
    fecal_coliforms = Column(Float, nullable=True)
    total_coliforms = Column(Float, nullable=True)
    area_description = Column(String, nullable=True)
    active = Column(Boolean, default=True)


class Station(Base):
    __tablename__ = "stations"

    station_name = Column(String, primary_key=True)
    beach_name = Column(String, nullable=True)
    station_description = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    area_description = Column(String, nullable=True)
    county = Column(String, nullable=True)
