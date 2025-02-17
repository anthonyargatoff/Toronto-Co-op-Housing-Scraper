import os
import schedule
from dotenv import load_dotenv
from scraping import *
from compareVacancies import compareVacancies

schedule.every(1).minutes.do(compareVacancies())
schedule.every().sunday.at("8:00").do() # TODO: send admin email update