import sqlite3


def createSchema():
    try:
        con = sqlite3.connect("toronto.db")
        cur = con.cursor()

        cur.executescript(
            """
            CREATE TABLE coop(
                id INTEGER PRIMARY KEY,
                name TEXT,
                availability INTEGER
            );

            CREATE TABLE statistics(
                id INTEGER PRIMARY KEY,
                totalCount INTEGER,
                weeklyCount INTEGER
            );
            """
        )
    except Exception as error:
        print(error)


if __name__ == "__main__":
    createSchema()