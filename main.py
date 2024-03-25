# p2app/engine/main.py
#
# ICS 33 Fall 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

import sqlite3
from p2app.events import database
from p2app.events import app

from p2app.events import continents
from p2app.engine import continentHandler
from p2app.events.continents import Continent

from p2app.events import countries
from p2app.engine import countryHandler
from p2app.events.countries import Country

from p2app.events import regions
from p2app.engine import regionHandler
from p2app.events.regions import Region

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.connection = None
        self.cursor = None

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if type(event) == database.OpenDatabaseEvent:
            pathStr = str(event.path())
            if not pathStr.endswith(".db"):
                yield database.DatabaseOpenFailedEvent("Path was not to a database")
            else:
                try:
                    self.connection = sqlite3.connect(event.path())
                    self.connection.execute("PRAGMA foreign_keys = ON;")
                    yield database.DatabaseOpenedEvent(event.path())
                except Exception as e:
                    yield database.DatabaseOpenFailedEvent("The file couldn't be opened")

        if isinstance(event, app.QuitInitiatedEvent):
            yield app.EndApplicationEvent()

        if isinstance(event, database.CloseDatabaseEvent):
            yield database.DatabaseClosedEvent()

        #CONTINENTS
        if isinstance(event, continents.StartContinentSearchEvent):
            cursor = self.connection.cursor()
            myContinentList = continentHandler.continent_search(cursor, event)
            print(type(myContinentList))
            if type(myContinentList) is list and len(myContinentList) > 0:
                for con in myContinentList:
                    yield continents.ContinentSearchResultEvent(con)

        if isinstance(event, continents.SaveNewContinentEvent):
            cursor = self.connection.cursor()
            cursor2 = self.connection.cursor()
            myContinent = continentHandler.load_new_continent(cursor, cursor2, event)
            if type(myContinent) == Continent:
                yield continents.ContinentSavedEvent(myContinent) #continent parameter
            else:
                yield continents.SaveContinentFailedEvent(myContinent) #string parameter

        if isinstance(event, continents.LoadContinentEvent):
            cursor = self.connection.cursor()
            myContinent = continentHandler.fetchContinent(cursor, event)
            yield continents.ContinentLoadedEvent(myContinent)

        if isinstance(event, continents.SaveContinentEvent):
            cursor = self.connection.cursor()
            cursor2 = self.connection.cursor()
            myContinent = continentHandler.saveContinent(cursor, cursor2, event)
            if type(myContinent) == Continent:
                yield continents.ContinentSavedEvent(myContinent) #continent parameter
            else:
                yield continents.SaveContinentFailedEvent(myContinent) #string parameter

    #COUNTRY
        if isinstance(event, countries.StartCountrySearchEvent):
            cursor = self.connection.cursor()
            myCountryList = countryHandler.country_search(cursor, event)
            if type(myCountryList) is list and len(myCountryList) > 0:
                for con in myCountryList:
                    yield countries.CountrySearchResultEvent(con)

        if isinstance(event, countries.SaveNewCountryEvent):
            cursor = self.connection.cursor()
            cursor2 = self.connection.cursor()
            myCountry = countryHandler.load_new_country(cursor, cursor2, event)
            if type(myCountry) == Country:
                yield countries.CountrySavedEvent(myCountry) #continent parameter
            else:
                yield countries.SaveCountryFailedEvent(myCountry) #string parameter

        if isinstance(event, countries.LoadCountryEvent):
            cursor = self.connection.cursor()
            myCountry = countryHandler.fetchCountry(cursor, event)
            yield countries.CountryLoadedEvent(myCountry)

        if isinstance(event, countries.SaveCountryEvent):
            cursor = self.connection.cursor()
            myCountry = countryHandler.saveCountry(cursor, event)
            if type(myCountry) == Country:
                yield countries.CountrySavedEvent(myCountry) #continent parameter
            else:
                yield countries.SaveCountryFailedEvent(myCountry) #string parameter
    #Region
        if isinstance(event, regions.StartRegionSearchEvent):
            cursor = self.connection.cursor()
            myRegionList = regionHandler.region_search(cursor, event)
            print(type(myRegionList))
            if type(myRegionList) is list and len(myRegionList) > 0:
                for con in myRegionList:
                    yield regions.RegionSearchResultEvent(con)

        if isinstance(event, regions.SaveNewRegionEvent):
            cursor = self.connection.cursor()
            cursor2 = self.connection.cursor()
            myRegion = regionHandler.load_new_region(cursor, cursor2, event)
            if type(myRegion) == Region:
                yield regions.RegionSavedEvent(myRegion) #continent parameter
            else:
                yield regions.SaveRegionFailedEvent(myRegion) #string parameter

        if isinstance(event, regions.LoadRegionEvent):
            cursor = self.connection.cursor()
            myRegion = regionHandler.fetchRegion(cursor, event)
            yield regions.RegionLoadedEvent(myRegion)

        if isinstance(event, regions.SaveRegionEvent):
            cursor = self.connection.cursor()
            myRegion = regionHandler.saveRegion(cursor, event)
            if type(myRegion) == Region:
                yield regions.RegionSavedEvent(myRegion) #continent parameter
            else:
                yield regions.SaveRegionFailedEvent(myRegion) #string parameter