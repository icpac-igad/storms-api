from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


from stormsapi.models.storm import Storm
from stormsapi.models.storm_point import StormPoint
from stormsapi.models.storm_segment import StormSegment
