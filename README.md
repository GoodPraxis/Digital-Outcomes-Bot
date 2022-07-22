Digital Outcomes Bot
====================

Sends a message to Google Chat when a new opportunity on [Digital Outcomes](https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities) appears.

The script will create a temporary file to store the latest ID of the opportunity to keep track of which opportunities are new and which have been seen already.

## Configuration
Set bot webhook URL in `config.ini`.

## Installation
Create a virtual environment and run `pip install`:

    pip install -r requirements.txt

## Usage
Simply run the script to scrape the page and send a message. We recommend setting up a cron job to schedule the task.

    python scraper.py

## License
AGPL Version 3, 19 November 2007 (see [LICENSE](LICENSE))
