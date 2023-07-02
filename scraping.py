from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

request = Request(url="https://co-ophousingtoronto.coop/resources/find-a-coop/",
                  headers={"User-Agent": "Mozilla/5.0"}
                  )

# opens the url
page = urlopen(request)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')
print(soup)
