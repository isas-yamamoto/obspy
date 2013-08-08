#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Header files for the FDSN webservice.

:copyright:
    The ObsPy Development Team (devs@obspy.org)
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
from obspy import __version__, UTCDateTime

import platform

URL_MAPPINGS = {"IRIS": "http://service.iris.edu",
                "USGS": "http://comcat.cr.usgs.gov",
                "RESIF": "http://ws.resif.fr",
                "NCEDC": "http://service.ncedc.org"
                }

# The default User Agent that will be sent with every request.
DEFAULT_USER_AGENT = "ObsPy %s (%s, Python %s)" % (__version__,
                                                   platform.platform(),
                                                   platform.python_version())


# The default parameters. Different services can choose to add more. It always
# contains the long name first and the short name second. If it has no short
# name, it is simply a tuple with only one entry.
DEFAULT_DATASELECT_PARAMETERS = [
    ("starttime", "start"), ("endtime", "end"), ("network", "net"),
    ("station", "sta"), ("location", "loc"), ("channel", "cha"), ("quality", ),
    ("minimumlength", ), ("longestonly", )]

DEFAULT_STATION_PARAMETERS = [
    ("starttime", "start"), ("endtime", "end"), ("startbefore", ),
    ("startafter", ), ("endbefore", ), ("endafter", ), ("network", "net"),
    ("station", "sta"), ("location", "loc"), ("channel", "cha"),
    ("minlatitude", "minlat"), ("maxlatitude", "maxlat"),
    ("minlongitude", "minlon"), ("maxlongitude", "maxlon"),
    ("latitude", "lat"), ("longitude", "lon"), ("minradius", ),
    ("maxradius",), ("level", ), ("includerestricted", ),
    ("includeavailability", ), ("updatedafter", )]

DEFAULT_EVENT_PARAMETERS = [
    ("starttime", "start"), ("endtime", "end"), ("minlatitude", "minlat"),
    ("maxlatitude", "maxlat"), ("minlongitude", "minlon"),
    ("maxlongitude", "maxlon"), ("latitude", "lat"), ("longitude", "lon"),
    ("minradius", ), ("maxradius", ), ("mindepth", ), ("maxdepth", ),
    ("minmagnitude", "minmag"), ("maxmagnitude", "maxmag"),
    ("magnitudetype", "magtype"), ("includeallorigins", ),
    ("includeallmagnitudes", ), ("includearrivals", ), ("eventid", ),
    ("limit",), ("offset", ), ("orderby", ), ("catalog", ), ("contributor", ),
    ("updatedafter", )]


# The default types if none are given. If the parameter can not be found in
# here and has no specified type, the type will be assumed to be a string.
DEFAULT_TYPES = {
    "starttime": UTCDateTime,
    "endtime": UTCDateTime,
    "network": str,
    "station": str,
    "location": str,
    "channel": str,
    "quality": str,
    "minimumlength": float,
    "longestonly": bool,
    "startbefore": UTCDateTime,
    "startafter": UTCDateTime,
    "endbefore": UTCDateTime,
    "endafter": UTCDateTime,
    "maxlongitude": float,
    "minlongitude": float,
    "longitude": float,
    "maxlatitude": float,
    "minlatitude": float,
    "latitude": float,
    "maxdepth": float,
    "mindepth": float,
    "maxmagnitude": float,
    "minmagnitude": float,
    "magnitudetype": str,
    "maxradius": float,
    "minradius": float,
    "level": str,
    "includerestricted": bool,
    "includeavailability": bool,
    "includeallorigins": bool,
    "includeallmagnitudes": bool,
    "includearrivals": bool,
    "eventid": int,
    "limit": int,
    "offset": int,
    "orderby": str,
    "catalog": str,
    "contributor": str,
    "updatedafter": UTCDateTime}

# This list collects WADL parameters that will not be parsed because they are
# not useful for the ObsPy client.
# Current the nodata parameter used by IRIS is part of that list. The ObsPy
# client relies on the HTTP codes.
# Furthermore the format parameter is part of that list. ObsPy relies on the
# default format.
WADL_PARAMETERS_NOT_TO_BE_PARSED = ["nodata", "format"]
