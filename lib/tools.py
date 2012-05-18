"""Tools using the parser."""
# Copyright (c) 2012 Andrew Dawson
#
# See the file license.txt for copying permission.


import urllib2
from contextlib import closing

from parser import PlanetRockRadioParser


# The URL of the played tracks list. This may change in the future.
PLANETROCK_RADIO_URL = "http://www.planetrock.com/played"


def recent_tracks(n=None):
    """The most recent tracks played on PlanetRock.
    
    Returns a tuple of tracks, the first is the most recent. Each track
    is a 3-tuple with entries:
        (title, artist, time)

    Only tracks played within the last hour are available.

    **Optional Argument:**

    *n*
        Maximum number of tracks to list.
        
    """
    with closing(urllib2.urlopen(PLANETROCK_RADIO_URL)) as f:
        s = f.read()
    with closing(PlanetRockRadioParser()) as parser:
        parser.feed(s)
        tracks = parser.tracks()
    tracks.reverse()
    return tracks[slice(0, n)]


if __name__ == "__main__":
    pass


