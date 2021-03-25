import logging

from stormsapi import db
from stormsapi.models import Storm, StormSegment, StormPoint
from shapely import geometry
from datetime import datetime


class StormService(object):

    @staticmethod
    def create_storm(storm_data, commit=True):

        storm = Storm(**storm_data)

        try:
            logging.info('[DB]: ADD')
            db.session.add(storm)

            if commit:
                db.session.commit()
        except Exception as e:
            raise e
        return storm

    @staticmethod
    def create_storm_from_json(storm_data):
        logging.info('[SERVICE]: Adding storm')

        storm_dict = {
            "id": storm_data.get("id"),
            "name": storm_data.get("name"),
            "category": storm_data.get("category"),
            "max_wind_speed": storm_data.get("max_wind_speed"),
            "min_pressure": storm_data.get("min_pressure"),
            "start_date": storm_data.get("start_date"),
            "end_date": storm_data.get("end_date"),
        }

        try:
            storm = StormService.create_storm(storm_dict, commit=True)

            points = storm_data.get("points")

            # sort the points by time
            points.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'))

            segment = StormService.create_storm_segment(storm, points=points, commit=True)

            for point in points:
                StormService.create_storm_point(storm_id=storm.id, storm_segment_id=segment.id, point=point)

        except Exception as e:
            raise e
        return storm

    @staticmethod
    def create_storm_segment(storm, points, commit=False):

        line = geometry.LineString([geometry.Point(point['coordinates']) for point in points])

        ewkt_line = f'SRID=4326;{line.wkt}'

        segment = StormSegment(storm_id=storm.id, geom=ewkt_line)

        try:
            logging.info('[DB]: ADD')
            db.session.add(segment)
            if commit:
                db.session.commit()
        except Exception as e:
            raise e
        return segment

    @staticmethod
    def create_storm_point(storm_id, storm_segment_id, point, commit=True):

        point_geom = geometry.Point(point['coordinates'])

        ewkt_line = f'SRID=4326;{point_geom.wkt}'

        storm_point_data = {
            "storm_id": storm_id,
            "storm_segment_id": storm_segment_id,
            "geom": ewkt_line,
            "wind_speed": point.get("wind_speed"),
            "min_pressure": point.get("wind_speed"),
            "category": point.get("category"),
            "date": point.get("date"),
        }

        point = StormPoint(**storm_point_data)

        try:
            logging.info('[DB]: ADD')
            db.session.add(point)
            if commit:
                db.session.commit()
        except Exception as e:
            raise e
        return point
