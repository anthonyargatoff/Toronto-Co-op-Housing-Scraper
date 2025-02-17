#! /usr/bin/env python3

import os
import time
import sqlite3
from dotenv import load_dotenv
from scraping import *
from send_email import *

load_dotenv()
con = sqlite3.connect("toronto.db")
cur = con.cursor()

print(
    "Server is running with frequency of {0} minutes.".format(
        os.getenv("FETCH_FREQUENCY")
    )
)

while True:
    try:
        print("New iteration")
        # incomingVacancies = get_vacancies()
        incomingVacancies = [
            # {"name": "test home", "vacancy": "Vacant"},
            # {"name": "test2", "vacancy": "Vacant"},
            # {"name": "t4", "vacancy": "Waiting List"}
        ]

        # Check for removed entries

        # Update all entries that were previously true if they don't appear in the fetch
        query = cur.execute("SELECT id FROM coop WHERE availability = '1';")
        result = query.fetchone()
        if not result and not incomingVacancies:
            time.sleep(10)
            continue
        elif result and not incomingVacancies:
            cur.execute("UPDATE coop SET availability = 0")
            con.commit()
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
        print("Sending Emails")
        print(newVacancies)

        time.sleep(10)

    except Exception as error:
        raise (error)
