# Toronto Housing Co-op Web Scraper

This program checks the availability of available co-ops [here](https://co-ophousingtoronto.coop/resources/find-a-coop/?region=all&vacancies=both) and will send email notifications to the recipients when a housing unit has an availability. It by default runs every 10 minutes, but can be edited in the code (main.py).

## How to use

1. Clone the repository onto your machine.
1. Create a `.env` file based on the `.example.env`
1. Create a virtual env with `python -m venv <venv>` where _<venv>_ is the name of the virtual environment.
1. Install requirements with `pip install -r requirements.txt`.
1. Run `db.py` to initialize the database
1. Run the program with `python3 ./main.py`

## No hup -- Run in background
1. To run as background process, use `nohup /<path>/<to>/<dir>/.venv/bin/python3 -u /<path>/<to>/<dir>/main.py > /<path>/<to>/<dir>/Toronto-Co-op-Housing-Scraper/log.txt 2>&1 &`