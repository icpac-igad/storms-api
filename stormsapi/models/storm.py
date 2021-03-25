from stormsapi import db


class Storm(db.Model):
    id = db.Column(db.String(256), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    max_wind_speed = db.Column(db.Integer(), nullable=False)
    min_pressure = db.Column(db.Float(), nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    end_date = db.Column(db.DateTime(), nullable=False)
    segments = db.relationship('StormSegment', backref='storm', passive_deletes=True)
    points = db.relationship('StormPoint', backref='storm', passive_deletes=True)

    def __init__(self, id, name, category, max_wind_speed, min_pressure, start_date, end_date):
        self.id = id
        self.name = name
        self.category = category
        self.max_wind_speed = max_wind_speed
        self.min_pressure = min_pressure
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return '<Segment %r>' % self.name

    def serialize(self, include=None):
        """Return object data in easily serializable format"""

        include = include if include else []

        storm = {
            "id": self.id,
        }

        return storm
