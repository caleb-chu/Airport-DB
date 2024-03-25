# Airport-DB
**FUNCTIONALITY**
Search for continents in the database, given either a continent code, a name, or both, displaying all of the continents that exactly match the given characteristics.
Add a new continent to the database, by specifying the various data points that describe them (except their primary key).
Update an existing continent in the database, changing any of the various data points that describe them (except their primary key).
Search for a country in the database, given either its country code, its name, or both, displaying all of the countries that exactly match the given characteristics.
Add a new country to the database, by specifying the various data points that describe them (except their primary key).
Update an existing country in the database, changing any of the various data points that describe them (except their primary key).
Search for a region (a part of a country) in the database, given either its region code, its local code, its name, or some combination of them, displaying all of the regions that exactly match the given characteristics..
Add a new region to the database, by specifying the various data points that describe them (except their primary key).
Update an existing region in the database, changing any of the various data points that describe them (except their primary key).
Notably, not all of the tables in the provided database are represented in the user interface, nor are they required to be, but the three tables that are represented should be sufficient to gain the necessary experience with how you can approach problems like this.

**COMPONENTS**

A package named p2app.views, which defines a tkinter-based graphical user interface giving a user the ability to view and edit the information in the airport.db database. All of the necessary functionality is already in place, so you will not need to make any modifications to this package.
A package named p2app.engine, in which you'll write the part of the program necessary to communicate with the airport.db, so that the provided graphical user interface can obtain and modify the information in that database. Almost all of the necessary code is missing from this package, so this is where you'll be working.
A package named p2app.events, which provides the tools necessary to allow the p2app.views package to communicate with the p2app.engine package. When the user interface needs to engine to perform some operation, it uses events to do it; when the engine needs to communicate its results back to the user interface, it uses events to do it. All of the necessary functionality is already in place, so you will not need to make any modifications to this package.
A "main" module named project2.py that initializes the necessary parts of the program, then launches the user interface. You will not need to make any modifications to this module.
How the user interface communicates with the engine

When the user interface needs something done, p2app.views sends out an event. Subsequently, p2app.engine receives that event and processes it, then sends out one or more events indicating what the results are. Those events are, in turn, received by p2app.views and cause the user interface to change in some way.

When p2app.views sends out an event, the Engine.process_event method is called, and its event parameter will be the event that was sent. In return, Engine.process_event generates any resulting events, which are received by the user interface again. So, ultimately, the entire interaction between the two packages boils down to a sequence of calls to a generator function: the user interface calling it with an event, and the engine yielding its results (if any).


Situation	Event sent by p2app.views	Event(s) sent back by p2app.engine
Application-level events
User quits the application	QuitInitiatedEvent	EndApplicationEvent
User opens a database file	OpenDatabaseEvent	
DatabaseOpenedEvent, when the database was opened successfully
DatabaseOpenFailedEvent, when opening the database failed, with a user-friendly error message
User closes the currently-open database file	CloseDatabaseEvent	DatabaseClosedEvent
Continent-related events
User initiates a search for continents	StartContinentSearchEvent	
One ContinentSearchResultEvent for each continent found in the search.
If no continents were found, no events are returned.
User loads a continent from the database to edit it	LoadContinentEvent	ContinentLoadedEvent, containing the loaded information about the continent
User saves a new continent into the database	SaveNewContinentEvent	
If saving the continent succeeded, ContinentSavedEvent, containing the complete information about the saved continent
If saving the continent failed, SaveContinentFailedEvent with a user-friendly error message.
User saves a modified continent into the database	SaveContinentEvent	
If saving the continent succeeded, ContinentSavedEvent, containing the complete information about the saved continent
If saving the continent failed, SaveContinentFailedEvent with a user-friendly error message.
Country-related events
User initiates a search for countries	StartCountrySearchEvent	
One CountrySearchResultEvent for each country found in the search.
If no countries were found, no events are returned.
User loads a country from the database to edit it	LoadCountryEvent	CountryLoadedEvent, containing the loaded information about the country
User saves a new country into the database	SaveNewCountryEvent	
If saving the country succeeded, CountrySavedEvent, containing the complete information about the saved country
If saving the country failed, SaveCountryFailedEvent with a user-friendly error message.
User saves a modified country into the database	SaveCountryEvent	
If saving the country succeeded, CountrySavedEvent, containing the complete information about the saved country
If saving the country failed, SaveCountryFailedEvent with a user-friendly error message.
Region-related events
User initiates a search for regions	StartRegionSearchEvent	
One RegionSearchResultEvent for each region found in the search.
If no regions were found, no events are returned.
User loads a region from the database to edit it	LoadRegionEvent	RegionLoadedEvent, containing the loaded information about the region
User saves a new region into the database	SaveNewRegionEvent	
If saving the region succeeded, RegionSavedEvent, containing the complete information about the saved region
If saving the region failed, SaveRegionFailedEvent with a user-friendly error message.
User saves a modified region into the database	SaveRegionEvent	
If saving the region succeeded, RegionSavedEvent, containing the complete information about the saved region
If saving the region failed, SaveRegionFailedEvent with a user-friendly error message.
In cases in which errors occur and there is no event specifically defined for it (e.g., when loading a continent fails), the engine should yield one ErrorEvent.

The various event types listed here are defined in the p2events package; refer to the Python modules in that package for details like the names and types of their attributes.

Debugging the events being sent and received

When the Show Events feature is enabled, all of the events sent from p2app.views and p2app.engine and sent back from p2app.engine to p2app.views are logged to the standard output. While your program is running, you'll find them in the Run area in PyCharm, where any other standard output would normally appear.

project2.py provides a way to execute your program in whole; executing project2.py executes the program. 
