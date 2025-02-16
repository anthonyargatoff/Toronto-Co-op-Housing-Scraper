import sqlite3


def createSchema():
    try:
        con = sqlite3.connect("toronto.db")
        cur = con.cursor()

        cur.executescript(
            """
            CREATE TABLE availability(
                id INTEGER PRIMARY KEY,
                status TEXT
            );

            CREATE TABLE coop(
                id INTEGER PRIMARY KEY,
                name TEXT,
                availability INTEGER,
                FOREIGN KEY (availability) REFERENCES availability(id) ON UPDATE CASCADE ON DELETE SET NULL
            );

            CREATE TABLE coopAvailabilities(
                id INTEGER PRIMARY KEY,
                coopId INTEGER,
                startAvailability TEXT DEFAULT CURRENT_TIMESTAMP,
                endAvailability TEXT
            );

            CREATE TABLE statistics(
                id INTEGER PRIMARY KEY,
                totalCount INTEGER,
                weeklyCount INTEGER
            );

            INSERT INTO availability(status) VALUES('vacancies', 'waiting_list', 'no_vacancies');
            """
        )
    except Exception as error:
        print(error)


if __name__ == "__main__":
    createSchema()
