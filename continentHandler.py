import sqlite3

from p2app.events.continents import Continent


def continent_search(myCursor, event): #Works perfectly
    """
    Search for continents in the database based on the given event attributes.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the query.
        event: An event object containing attributes for the search.

    Returns:
        list[Continent] or None: A list of Continent objects matching the search criteria, or None if no matches are found.
    """
    continent_code = event.continent_code()
    name = event.name()
    if continent_code and name:
        myCursor.execute("SELECT * FROM continent WHERE continent_code = ? and name = ?", (continent_code, name))
    elif continent_code:
        myCursor.execute("SELECT * FROM continent WHERE continent_code = ?", (continent_code,))
    elif name:
        myCursor.execute("SELECT * FROM continent WHERE name = ?", (name,))
    else:
        return None

    continent_list = []
    rows = myCursor.fetchall()
    if rows:
        for row in rows:
            continent = Continent(*row)
            continent_list.append(continent)
        return continent_list
    else:
        return

def load_new_continent(myCursor, myCursor2, event): #Perfect, Duplicate Continent Code, Empty fields dealt with
    """
    Load a new continent into the database, ensuring uniqueness of the continent_code.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor for inserting the new continent.
        myCursor2 (sqlite3.Cursor): The SQLite cursor for checking the existence of continent_code.
        event: An event object with continent information.

    Returns:
        Continent or str: The newly loaded Continent object or a message indicating if the continent_code already exists.
    """
    myCon = event.continent()
    continent_code = myCon.continent_code
    name = myCon.name

#cursor 2 checks if code exists
    myCursor2.execute(f'SELECT * FROM continent WHERE continent_code = "{continent_code}"')
    conCode = myCursor2.fetchone()

    # and continent_code and name
    if conCode is None:
        # Creates new row
        insert_query = "INSERT INTO continent (continent_code, name) VALUES (?, ?)"
        myCursor.execute(insert_query, (continent_code, name))

        myCursor.execute("SELECT * FROM continent WHERE continent_code = ? AND name = ?", (continent_code, name))
        myRow = myCursor.fetchone() #fetches the id of continent we want
        myCursor.connection.commit()  # Commit the changes to the database
        myContinent = Continent(continent_id = myRow[0], continent_code = continent_code, name = name)
        return myContinent
    else:
        return "Continent Code already exists"

def fetchContinent(myCursor,event): #Works perfectly
    """
    Fetch a Continent based on the continent_id.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the query.
        event: An event object with the continent_id.

    Returns:
        Continent: The Continent object.
    """
    myContinent_id = event.continent_id()
    myCursor.execute("SELECT * FROM continent WHERE continent_id = ?", (myContinent_id,))
    myContinent = Continent(*myCursor.fetchone())
    return myContinent

def saveContinent(myCursor, myCursor2, event):
    """
    Save changes to a Continent in the database, checks if continent code is unique.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the update.
        myCursor2 (sqlite3.Cursor): The SQLite cursor for checking the existence of continent_code.
        event: An event object with the Continent to save.

    Returns:
        Continent or str: The saved Continent object or a message indicating if the continent_code already exists.
    """
    myContinent = event.continent()
    myContinent_id = myContinent.continent_id

    try:
        myCursor.execute("UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?",(myContinent.continent_code, myContinent.name, myContinent_id))
        return myContinent
    except Exception:
        return "Make sure the continent code is unique"
