import sqlite3

con = sqlite3.connect("toronto.db")
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE availability(
        id INTEGER PRIMARY KEY,
        status TEXT
    );
    """
)
cur.execute(
    """
     CREATE TABLE coop(
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        availability INTEGER,
        FOREIGN KEY (availability) REFERENCES availability(id) ON UPDATE CASCADE ON DELETE SET NULL
    );
    """
)
cur.execute(
    """
    CREATE TABLE coopAvailabilities(
        id INTEGER PRIMARY KEY,
        coopId INTEGER,
        startAvailability TEXT DEFAULT CURRENT_TIMESTAMP,
        endAvailability TEXT
    );
    """
)
cur.execute(
    """
    CREATE TABLE statistics(
        id INTEGER PRIMARY KEY,
        totalCount INTEGER,
        weeklyCount INTEGER
    );
    """
)