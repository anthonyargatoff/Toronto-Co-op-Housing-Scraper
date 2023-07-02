import requests
from bs4 import BeautifulSoup


def get_vacancies():
    URL = "https://co-ophousingtoronto.coop/resources/find-a-coop/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    coop_table = soup.find("div", class_="coop-table")
    vacancies = coop_table.find_all("div", class_="coop-field vacancies")
    vacancies_text = []
    coop_names_text = []

    for vacancy in vacancies:
        vacancies_text.append(vacancy.text)

    coop_names = coop_table.find_all("div", class_="coop-field name")
    for coop_name in coop_names:
        coop_names_text.append(coop_name.text)

    combined = {coop_names_text[i]: vacancies_text[i]
                for i in range(len(coop_names_text))}

    available_coops = {}
    for name, vacants in combined.items():
        if vacants != "No vacancies":
            available_coops.update({name: vacants})

    available_coops_string = ""
    for name, vacant in available_coops.items():
        available_coops_string += name + ": " + vacant + "\n"

    if (available_coops):
        return True, available_coops_string
    else:
        return False, None
