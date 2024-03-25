from p2app.events.countries import Country


def country_search(myCursor, event): #Works perfectly
    """
    Search for countries in the database based on the given event attributes.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the query.
        event: An event object containing attributes for the search.

    Returns:
        list[Country] or None: A list of Country objects matching the search criteria, or None if no matches are found.
    """
    country_code = event.country_code()
    name = event.name()
    if country_code and name:
        myCursor.execute("SELECT * FROM country WHERE country_code = ? and name = ?", (country_code, name))
    elif country_code:
        myCursor.execute("SELECT * FROM country WHERE country_code = ?", (country_code,))
    elif name:
        myCursor.execute("SELECT * FROM country WHERE name = ?", (name,))
    else:
        return None

    country_list = []
    rows = myCursor.fetchall()
    if rows:
        for row in rows:
            country = Country(*row)
            country_list.append(country)
        return country_list
    else:
        return

def load_new_country(myCursor, myCursor2, event):  # Perfect, Duplicate country Code, Empty fields dealt with
    #'country_code', 'name', 'continent_id', 'wikipedia_link', 'keywords'])
    """
    Load a new country into the database, ensuring uniqueness of the country_code.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor for inserting the new continent.
        myCursor2 (sqlite3.Cursor): The SQLite cursor for checking the existence of continent_code.
        event: An event object with continent information.

    Returns:
        Country or str: The newly loaded Country object or a message indicating if the country_code already exists.
    """
    myCon = event.country()
    country_code = myCon.country_code
    name = myCon.name
    continent_id = myCon.continent_id
    wikipedia_link = myCon.wikipedia_link
    keywords = myCon.keywords

    # cursor 2 checks if code exists
    myCursor2.execute(f'SELECT * FROM country WHERE country_code = "{country_code}"')
    conCode = myCursor2.fetchone()

    if conCode is None and keywords:
        print("Started if statement")

        # Creates new row
        insert_query = "INSERT INTO country (country_code, name, continent_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?)"
        try:
            myCursor.execute(insert_query, (country_code, name, continent_id, wikipedia_link, keywords))
        except Exception:
            return "Please enter valid continent id"

        myCursor.execute("SELECT * FROM country WHERE country_code = ? AND name = ?",(country_code,name))
        myRow = myCursor.fetchone() #gets the id of the new one
        myCursor.connection.commit()  # Commit the changes to the database
        myCountry = Country(country_id = myRow[0], country_code = country_code,name = name, continent_id = continent_id, wikipedia_link = wikipedia_link, keywords = keywords)
        return myCountry
    else:
        return "Country Code already exists"

def fetchCountry(myCursor, event):  # Works perfectly
    """
    Fetch a country based on the country_id.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the query.
        event: An event object with the country_id.

    Returns:
        country: The country object.
    """
    myCountry_id = event.country_id()
    myCursor.execute("SELECT * FROM country WHERE country_id = ?", (myCountry_id,))
    myCountry = Country(*myCursor.fetchone())
    return myCountry

def saveCountry(myCursor, event): #Duplicate country code will not work
    """
    Save changes to a country in the database, checks if country code is unique.

    Args:
        myCursor (sqlite3.Cursor): The SQLite cursor to execute the update.
        myCursor2 (sqlite3.Cursor): The SQLite cursor for checking the existence of country_code.
        event: An event object with the country to save.

    Returns:
        country or str: The saved country object or a message indicating if the country_code already exists.
    """
    myCountry = event.country()
    myCountry_id = myCountry.country_id
    myKeywords = myCountry.keywords
    if myKeywords:
        try:
            myCursor.execute(f"UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = {myCountry_id}",(myCountry.country_code, myCountry.name, myCountry.continent_id, myCountry.wikipedia_link, myCountry.keywords))
            return myCountry
        except Exception:
            return "Make sure the country code is unique"
    else:
        return "Please enter a keyword"
