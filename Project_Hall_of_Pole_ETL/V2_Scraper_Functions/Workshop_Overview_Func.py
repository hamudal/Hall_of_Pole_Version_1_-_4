import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import text


def workshop_overview(url):

    # Send a GET request to the webpage
    response = requests.get(url)
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    response

    # extract workshop name
    workshop_name = soup.find(
        'div', class_='header-holder').find('h3').text.strip()

    workshop_beschreibung = ''.join([p.text.strip() for p in soup.find(
        'div', class_='marketplace-truncated-text-block js_truncate-block').find_all('p')])

    # extract pole studio name
    pole_studio = soup.find(
        'a', class_='venue-name action-link-default').text.strip()

    # extract pole studio address
    try:
        stadt = soup.find('div', class_='venue-location').text.strip()
    except AttributeError:
        stadt = 0

    # extract pole studio street address
    try:
        strasse = soup.find('div', class_='venue-location').text.strip()
    except AttributeError:
        strasse = 0

    # extract date
    datum = soup.find('div', class_='date-holder').text.strip()

    # extract time
    uhrzeit = soup.find('div', class_='date-holder').text.strip()

    # extract duration
    dauer = soup.find('div', class_='date-holder').text.strip()

    # extract level
    try:
        level = soup.find('div', class_='event-level').text.strip()
    except AttributeError:
        level = 0

    # extract trainer
    try:
        trainer = soup.find('div', class_='trainer-name').text.strip()
    except AttributeError:
        trainer = 0

    # extract trainer description
    try:
        trainer_beschreibung = soup.find(
            'div', class_='about-teacher text').text.strip()
    except:
        trainer_beschreibung = 0

    # extract price
    preis = soup.find('div', class_='event-detail-price__price').text.strip()

    # Reconstruct Eversports Pole Studio Webpage
    a_tag = soup.find('a', {'class': 'venue-name'})

    link_p2 = a_tag['href']
    link_p1 = "https://www.eversports.de"
    polestudio_eversports_seite = link_p1 + link_p2

    # Regex names
    workshop_name = re.sub(r'\W+', '_', workshop_name)

    # create pandas DataFrame
    workshop_overview_df = pd.DataFrame({
        'Workshop Name': [workshop_name],
        'Workshop Beschreibung': [workshop_beschreibung],
        'PoleStudio': [pole_studio],
        'Stadt': [stadt],
        'Straße': [strasse],
        'Datum': [datum],
        'Uhrzeit': [uhrzeit],
        'Dauer': [dauer],
        'Level': [level],
        'Trainer': [trainer],
        'Trainer Beschreibung': [trainer_beschreibung],
        'Preis': [preis],
        'Workshop Everest Seite': url,
        'PoleStudio Eversports Seite': polestudio_eversports_seite
    })

    workshop_overview_df['Version'] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")

    # Splitt the string to get the town
    try:
        workshop_overview_df["Stadt"] = stadt.split(",")[1].split(" ")[2]
    except:
        workshop_overview_df["Stadt"] = 0

    # Splitt the string to get the street
    try:
        workshop_overview_df["Straße"] = strasse[5:-7]
    except:
        workshop_overview_df["Straße"] = 0

    #
    workshop_overview_df["Datum"] = datum[3:13]
    #
    workshop_overview_df["Uhrzeit"] = uhrzeit[14:29]

    #
    try:
        workshop_overview_df["Dauer"] = dauer[-7:-1]
    except:
        workshop_overview_df["Dauer"] = 0
    #
    try:
        workshop_overview_df["Level"] = level[5:]
    except:
        workshop_overview_df["Level"] = 0

    # create the "CSV" directory if it does not exist
    if not os.path.exists("Workshop_CSV"):
        os.makedirs("Workshop_CSV")

    # save the CSV file in the "CSV" directory
    # workshop_overview_df.to_csv(
    #     f"Workshop_CSV/{pole_studio}_{workshop_name}.csv", index=False)

    return workshop_overview_df
