import requests
from bs4 import BeautifulSoup

def get_test_results():
    """
    Gets the test results of the web scrapper as to ensure smooth operation.

    Returns:
        String: A string containing a table of all the residences and their vacancy status, as well as the number of each.
    """
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
    
    test_results_string = ""
    for name, vacant in combined.items():
        test_results_string += name + ": " + vacant + "\n"
        
    test_results_string += "Number of co-ops: {}. Number of Vacancies: {}.".format(len(coop_names), len(vacancies))
    
    return test_results_string
    

def get_vacancies():
    """
    Determines if there are any vacant co-op houses.

    Returns:
        Boolean: True if there are houses, false if not.
        String: If true, returns a list of available co-ops.
        
    """    
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
