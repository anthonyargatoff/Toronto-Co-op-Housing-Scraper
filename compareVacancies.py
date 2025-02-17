import sqlite3
from dotenv import load_dotenv
from scraping import *
from send_email import *

con = sqlite3.connect("toronto.db")
cur = con.cursor()


def compareVacancies():
    try:
        print("Searching...")
        incomingVacancies = get_vacancies()
        
        # Set statistics
        cur.execute("UPDATE statistics SET totalCount = totalCount + 1 WHERE id = 1;")
        con.execute()

        # Update all entries that were previously true if they don't appear in the fetch
        query = cur.execute("SELECT id FROM coop WHERE availability = '1';")
        result = query.fetchone()
        if not result and not incomingVacancies:
            return
        elif result and not incomingVacancies:
            cur.execute("UPDATE coop SET availability = 0")
            con.commit()
            return
        else:
            vacanciesToUpdate = [
                incomingVacancy["name"] for incomingVacancy in incomingVacancies
            ]
            placeholders = ", ".join("?" for _ in vacanciesToUpdate)
            sql = f"UPDATE coop SET availability = 0 WHERE name NOT IN ({placeholders})"
            cur.execute(sql, vacanciesToUpdate)
            con.commit()

        newVacancies = []

        # Check if new vacancy notification has already been sent
        for incomingVacancy in incomingVacancies:
            query = cur.execute(
                "SELECT * FROM coop WHERE name = ?;", [incomingVacancy["name"]]
            )
            result = query.fetchone()

            if not result:  # add to database. Will be available at this point
                print("adding to db")
                cur.execute(
                    "INSERT INTO coop(name, availability) VALUES(?, 1);",
                    [incomingVacancy["name"]],
                )
                con.commit()
                newVacancies.append(incomingVacancy)

            else:  # Coop name is already in database. Check if already vacant
                if not result[2]:  # Newly vacant, add to list
                    print("updating db")
                    cur.execute(
                        "UPDATE coop SET availability = 1 WHERE id = ?;", [result[0]]
                    )
                    con.commit()
                    newVacancies.append(incomingVacancy)

        # TODO: Send emails with newVacancies lists
        if len(newVacancies):
            print("Sending Emails")
            send_email(
                subject="New co-op found",
                body=""
            )
            print(newVacancies)
            
    except Exception as error:
        raise (error)
