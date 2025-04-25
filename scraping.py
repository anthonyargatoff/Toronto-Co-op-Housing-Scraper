from requests_html import HTMLSession
from bs4 import BeautifulSoup

def get_vacancies():
    """
    Determines if there are any vacant co-op houses.

    Returns: Dictionary of co-op names and vacancy status.
    { 
        "name": name,
        "vacancy": vacancy 
    }

    """
    try:
        URL = "https://co-ophousingtoronto.coop/resources/find-a-coop/?region=all&vacancies=both"
        session = HTMLSession() # Create an HTMLSession object
        page = session.get(URL) # Get the raw HTML from the website using htmlsession
        soup = BeautifulSoup(page.content, 'html.parser') # Create bs4 object so we can parse the data
        
        coopTable = soup.find("div", class_="coop-table")
        vacanciesObject = []
        
        coops = coopTable.find_all("div", class_="coop-tile")
        for coop in coops:
            name = coop.find("div", class_="coop-field name").text
            vacancy = coop.find("div", class_="coop-field vacancies").text
            vacanciesObject.append({
                "name": name,
                "vacancy": vacancy,
            })
        return vacanciesObject
    
    except Exception as error:
        print(error)
        return None


if __name__ == "__main__":
    print(get_vacancies())