import sqlite3
import os
from dotenv import load_dotenv
from scraping import get_vacancies
from send_email import *



def compareVacancies():
    con = sqlite3.connect("toronto.db")
    cur = con.cursor()
    
    try:
        print("Searching...")
        incomingVacancies = get_vacancies()

        # Set statistics
        cur.execute("UPDATE statistics SET totalCount = totalCount + 1, weeklyCount = weeklyCount + 1 WHERE id = 1;")
        con.commit()

        # Update all entries that were previously true if they don't appear in the fetch
        query = cur.execute("SELECT id FROM coop WHERE availability = '1';")
        result = query.fetchone()
        if not result and not incomingVacancies:
            print("No availability")
            return
        elif result and not incomingVacancies:
            cur.execute("UPDATE coop SET availability = 0")
            con.commit()
            print("No availability")
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

        # Send emails with newVacancies lists
        if len(newVacancies):
            load_dotenv(override=True)
            print("Sending Emails")
            print(newVacancies)

            # Format vacancies string
            vacanciesString = ""
            for newVacancy in newVacancies:
                vacanciesString += "Name: {0}. Availability: {1}\n".format(
                    newVacancies["name"], newVacancies["vacancy"]
                )

            recipientList = os.getenv("EMAIL_ADDRESSES").split(",")

            send_email(
                subject="New co-op found",
                body="New co-ops have been found:\n\n" + vacanciesString,
                recipients=recipientList,
                email_account=os.getenv("SENDER_EMAIL"),
                email_password=os.getenv("SENDER_PASSWORD"),
                email_server=os.getenv("SENDER_SERVER"),
                email_server_port_number=os.getenv("SENDER_PORT"),
            )

    except Exception as error:
        adminList = os.getenv("ADMIN_EMAIL_ADDRESSES").split(",")
        send_email(
            subject="Co-op error",
            body="Error:\n\n {}".format(error),
            recipients=adminList,
            email_account=os.getenv("SENDER_EMAIL"),
            email_password=os.getenv("SENDER_PASSWORD"),
            email_server=os.getenv("SENDER_SERVER"),
            email_server_port_number=os.getenv("SENDER_PORT"),
        )
        
    con.close()


if __name__ == "__main__":
    compareVacancies()