from stormsapi import db
from geoalchemy2 import Geometry
from sqlalchemy import Index


class StormSegment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    storm_id = db.Column(db.String(256), db.ForeignKey('storm.id', ondelete="CASCADE"), nullable=False)
    geom = db.Column(Geometry('LINESTRING', srid=4326, spatial_index=False), nullable=False)
    ss_scale = db.Column(db.String(256), nullable=True)

    def __init__(self, storm_id, geom, ss_scale=None):
        self.storm_id = storm_id
        self.geom = geom
        self.ss_scale = ss_scale

    def __repr__(self):
        return f"<StormSegment {self.id} - {self.storm_id}>"

    def serialize(self, include=None):
        """Return object data in easily serializable format"""

        include = include if include else []

        segment = {
            "id": self.id,
        }

        return segment


Index('idx_storm_segment_geom', StormSegment.__table__.c.geom, postgresql_using='gist')
