"""Parsing support."""
# Copyright (c) 2012 Andrew Dawson
#
# See the file license.txt for copying permission.


try:
    # Python 3
    from html.parser import HTMLParser
except:
    from HTMLParser import HTMLParser


class PlanetRockRadioParser(HTMLParser):
    """Parse the PlanetRock played tracks webpage."""

    def __init__(self):
        HTMLParser.__init__(self)
        # Define the state of the parser.
        self._state = dict(intrack=False, nextistitle=False,
                nextisartist=False, nextistime=False)
        # Storage for track details.
        self._data = dict(artist=list(), title=list(), time=list())
        # HTML tag handlers.
        self._starthandlers = dict(p=self._handle_startp,
                span=self._handle_startspan, li=self._handle_startli)

    def tracks(self):
        """Return the tracks.

        Returns a tuple of tracks. Each track is a 3-tuple with entries:
            (title, artist, time)

        """
        return zip(self._data["title"], self._data["artist"], 
                self._data["time"])

    def handle_starttag(self, tag, attrs):
        try:
            # Run the appropriate handler for the current tag and create
            # storage for the tag data.
            self._starthandlers[tag](attrs)
            self._entities = list()
        except KeyError:
            # If no handler is specified don't do anything.
            pass

    def handle_endtag(self, tag):
        # Retrieve the list (artist, title, or time) that data should be
        # appended to.
        datalist = self._get_datalist()
        try:
            # If a valid list was returned combine the current data entities
            # into a string and add them to the list.
            datalist.append("".join(self._entities).strip())
        except AttributeError:
            pass

    def handle_data(self, data):
        if self._state["intrack"]:
            # Append to the data entities list if currently in a track.
            self._entities.append(data)

    def _handle_startli(self, attrs):
        for name, value in attrs:
            if name == "class":
                if value.startswith("playedTrack"):
                    self._state["intrack"] = True

    def _handle_startp(self, attrs):
        for name, value in attrs:
            if name == "class":
                if value == "trackTime":
                    self._state["nextistime"] = True

    def _handle_startspan(self, attrs):
        if self._state["intrack"]:
            for name, value in attrs:
                if name == "class":
                    if value == "trackTitle":
                        self._state["nextistitle"] = True
                    elif value == "trackArtist":
                        self._state["nextisartist"] = True

    def _get_datalist(self):
        """
        Return the appropriate list given the current state of the
        parser. Also adjust the state.

        """
        if self._state["intrack"]:
            if self._state["nextistime"]:
                self._state["nextistime"] = False
                return self._data["time"]
            if self._state["nextistitle"]:
                self._state["nextistitle"] = False
                return self._data["title"]
            if self._state["nextisartist"]:
                self._state["nextisartist"] = False
                self._state["intrack"] = False
                return self._data["artist"]
        return None


if __name__ == "__main__":
    pass

