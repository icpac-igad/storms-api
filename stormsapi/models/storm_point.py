from stormsapi import db
from geoalchemy2 import Geometry
from sqlalchemy import Index


class StormPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    storm_id = db.Column(db.String(256), db.ForeignKey('storm.id', ondelete="CASCADE"), nullable=False)
    storm_segment_id = db.Column(db.Integer(), db.ForeignKey('storm_segment.id', ondelete="CASCADE"), nullable=False)
    wind_speed = db.Column(db.Integer(), nullable=False)
    min_pressure = db.Column(db.Float(), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    geom = db.Column(Geometry('POINT', srid=4326, spatial_index=False), nullable=False)

    def __init__(self, storm_id, storm_segment_id, wind_speed, min_pressure, category, date, geom):
        self.storm_id = storm_id
        self.storm_segment_id = storm_segment_id
        self.wind_speed = wind_speed
        self.min_pressure = min_pressure
        self.category = category
        self.date = date
        self.geom = geom

    def __repr__(self):
        return '<StormPoint %r>' % self.id

    def serialize(self, include=None):
        """Return object data in easily serializable format"""

        include = include if include else []

        storm = {
            "id": self.id,
        }

        return storm


Index('idx_storm_point_geom', StormPoint.__table__.c.geom, postgresql_using='gist')
