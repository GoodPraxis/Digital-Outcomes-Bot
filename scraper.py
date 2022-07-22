import requests, configparser, time
from bs4 import BeautifulSoup

URL = "https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities?statusOpenClosed=open&lot=digital-outcomes"
# Load bot url from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
BOT_URL = config['BOT']['url']


def get_opportunities():
    """
    Get all the opportunities from the Digital Marketplace
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    opportunity_items = soup.find_all('li', class_='app-search-result')
    opportunities = [process_opportunity(opportunity) for opportunity in opportunity_items]
    opportunities = sorted(opportunities, key=lambda k: k['id'])
    return opportunities

def process_opportunity(opportunity):
    """
    Find .govuk-link in the opportunity and return the url and text
    """
    link = opportunity.find('a', class_='govuk-link')
    url = link['href']
    # Get id from url
    try:
        id = int(url.split('/')[-1])
    except ValueError:
        id = 0
    text = link.text
    return {'id': id, 'url': url, 'text': text}

def save_id_in_file(id):
    """
    Overwrite the id in a file
    """
    with open('id.txt', 'w') as f:
        f.write(str(id))

def read_id_from_file():
    """
    Read the id from a file as integer
    """
    with open('id.txt', 'r') as f:
        id = f.read()
    return int(id)

def scrape():
    """
    Scrape the Digital Marketplace, go through all opportunities
    """
    id = 0
    try:
        id = read_id_from_file()
    except FileNotFoundError:
        pass
    print("Getting opportunities")
    opportunities = get_opportunities()
    most_recent_id = 0
    for opportunity in opportunities:
        if opportunity['id'] > id:
            text = opportunity['text']
            url = opportunity['url']
            most_recent_id = opportunity['id']
            send_message(f'New opportunity: {text}\nhttps://www.digitalmarketplace.service.gov.uk/{url}')

    if most_recent_id > id:
        save_id_in_file(most_recent_id)

def send_message(message):
    """
    Send a message to the Google Chat
    """
    print(message, BOT_URL)
    data = {
        "text": message
    }
    try:
        requests.post(BOT_URL, json=data)
    except requests.exceptions.RequestException as e:
        print(e)

if __name__ == "__main__":
    scrape()
