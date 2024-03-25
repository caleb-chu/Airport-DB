import sqlite3

from p2app.events.regions import Region


def region_search(myCursor, event):
    """
    Search for regions in the database based on the given event attributes.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the query.
        event: An event object containing attributes for the search.

    Returns:
        list[Region] or None: A list of Region objects matching the search criteria, or None if no matches are found.
    """
    region_code = event.region_code()
    local_code = event.local_code()
    name = event.name()

    if region_code and local_code and name: #6 possible combinations, 3 available
        myCursor.execute("SELECT * FROM region WHERE region_code = ? and local_code = ? and name = ?", (region_code, local_code, name))
    elif region_code and local_code: #2 available
        myCursor.execute("SELECT * FROM region WHERE region_code = ? and local_code = ?", (region_code, local_code))
    elif region_code and name:
        myCursor.execute("SELECT * FROM region WHERE region_code = ? and name = ?", (region_code, name))
    elif local_code and name:
        myCursor.execute("SELECT * FROM region WHERE local_code = ? and name = ?", (local_code, name))
    elif region_code: #1 available
        myCursor.execute("SELECT * FROM region WHERE region_code = ?", (region_code,))
    elif local_code:
        myCursor.execute("SELECT * FROM region WHERE local_code = ?", (local_code,))
    elif name:
        myCursor.execute("SELECT * FROM region WHERE name = ?", (name,))
    else:
        return None

    region_list = []
    rows = myCursor.fetchall()
    if rows:
        for row in rows:
            region = Region(*row)
            region_list.append(region)
        return region_list
    else:
        return

def load_new_region(myCursor, myCursor2, event):  # Perfect, Duplicate region Code, Empty fields dealt with
    """
    Load a new region into the database, ensuring uniqueness of the region_code.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor for inserting the new region.
        myCursor2 (sqlite3.Cursor): The SQLite cursor for checking the existence of region_code.
        event: An event object with region information.

    Returns:
        region or str: The newly loaded region object or a message indicating if the region_code already exists.
    """
    #['region_id', 'region_code', 'local_code', 'name','continent_id', 'country_id', 'wikipedia_link', 'keywords'])
    myRegion = event.region()
    region_code = myRegion.region_code
    local_code = myRegion.local_code
    name = myRegion.name
    continent_id = myRegion.continent_id
    country_id = myRegion.country_id
    wikipedia_link = myRegion.wikipedia_link
    keywords = myRegion.keywords

    # cursor 2 checks if code exists
    myCursor2.execute(f'SELECT * FROM region WHERE region_code = "{region_code}"')
    conCode = myCursor2.fetchone()

    if conCode is None and keywords:
        print("Started if statement")

        # Creates new row
        insert_query = "INSERT INTO region (region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?)"
        try:
            myCursor.execute(insert_query, (region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords))
        except Exception:
            return "Please enter valid continent id and country_id"
        myCursor.execute("SELECT * FROM region WHERE region_code = ? AND name = ?", (region_code, name))
        myRow = myCursor.fetchone() #gets the id of the new one
        myCursor.connection.commit()  # Commit the changes to the database
        myRegion = Region(region_id = myRow[0], region_code = region_code, local_code = local_code, name = name, continent_id = continent_id, country_id = country_id, wikipedia_link = wikipedia_link, keywords = keywords)
        return myRegion
    else:
        return "region Code already exists"


def fetchRegion(myCursor, event):  # Works perfectly
    """
    Fetch a region based on the region_id.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the query.
        event: An event object with the region_id.

    Returns:
        region: The region object.
    """
    myRegion_id = event.region_id()
    myCursor.execute("SELECT * FROM region WHERE region_id = ?", (myRegion_id,))
    myRegion = Region(*myCursor.fetchone())
    return myRegion

def saveRegion(myCursor, event):
    """
    Save changes to a region in the database, checks if region code is unique.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the update.
        myCursor2 (sqlite3.Cursor): The SQLite cursor for checking the existence of region_code.
        event: An event object with the region to save.

    Returns:
        region or str: The saved region object or a message indicating if the region_code already exists.
    """
    myRegion = event.region()
    myRegion_id = myRegion.region_id
    myKeywords = myRegion.keywords

    print(myRegion)

    if myKeywords:
        try:
            myCursor.execute("UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?",
                             (myRegion.region_code, myRegion.local_code, myRegion.name, myRegion.continent_id, myRegion.country_id, myRegion.wikipedia_link, myRegion.keywords, myRegion.region_id))
            return myRegion
        except sqlite3.Error as e:
            return str(e)
    else:
        return "Enter a keyword"

