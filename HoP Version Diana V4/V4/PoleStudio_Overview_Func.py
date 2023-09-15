import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import text


def pole_overview(url):

    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Container Overview
    overview_description = soup.find_all('div', class_="css-ptk251")

    # Loop through each element in the container
    for item in overview_description:
        # Pole Studio Name
        pole_studio_name = item.find(
            'p', class_='MuiTypography-root MuiTypography-body1 css-1yc2rip').text

        # Address
        location = item.find(
            'p', class_="MuiTypography-root MuiTypography-body1 css-e8od91").text

    # Container Description Pole Studio
    description = soup.find_all('div', class_="css-1821gv5")

    # Loop through each element in the container
    for item in description:
        # Pole Describtion Name
        pole_studio_description = item.find(
            'p', class_='MuiTypography-root MuiTypography-body1 css-pxnkv9').text

        if pole_studio_description.strip():
            pole_studio_description = pole_studio_description.strip()
            break

    # Container Prices
    starting_price_ = soup.find_all('div', class_="css-1vt08d7")
    list_5 = soup.find_all('div', class_="css-sge262")

    starting_price = 0

    try:
        # Starting Price
        starting_price = item.find(
            'p', class_='MuiTypography-root MuiTypography-body1 css-13ps6ou').text
    except AttributeError:
        starting_price = 0

    # Rating
    div_container = soup.find('div', class_='css-1oqii6')
    div_container.find_all('p')
    p_elements = div_container.find_all('p')

    # Find the container for the rating information
    rating_container = soup.find('div', class_='css-1oqii6')
    ratingscore = div_container.find_all('p')[0].text
    ratingcount = div_container.find_all('p')[1].text
    #
    ratingfactors = [div_container.find_all('p')[2].text + ' ' + div_container.find_all('p')[3].text,
                     div_container.find_all(
                         'p')[4].text + ' ' + div_container.find_all('p')[5].text,
                     div_container.find_all(
                         'p')[6].text + ' ' + div_container.find_all('p')[7].text,
                     div_container.find_all(
                         'p')[8].text + ' ' + div_container.find_all('p')[9].text,
                     div_container.find_all(
                         'p')[10].text + ' ' + div_container.find_all('p')[11].text
                     ]

    # Contact Info: Homepage, Telephone, E-Mail
    pole_info = (soup.find_all('div', class_='css-1x2phcg'))

    contact_info = []
    for div in pole_info:
        a_tags = div.find_all('a')
        contact_row = {"E-Mail": 0, "Homepage": 0, "Telefon": 0}
        for a in a_tags:
            href = a.get('href')
            try:
                if 'mailto:' in href:
                    email = href.replace('mailto:', '')
                    contact_row["E-Mail"] = email
            except:
                pass
            try:
                if 'http' in href:
                    homepage = href
                    contact_row["Homepage"] = homepage
            except:
                pass
            try:
                if 'tel:' in href:
                    phone = href.replace('tel:', '')
                    contact_row["Telefon"] = phone
            except:
                pass
        contact_info.append(contact_row)

    # Prepare Strings
    location.split(',')
    address = location.split(',')[1]
    town = location.split(',')[0]
    plz = location.split(',')[1].split(' ')[1]

    # create a dictionary from the given lists
    pole_studio_overview = {
        'PoleStudio': pole_studio_name,
        'PLZ': plz,
        'Stadt': town,
        'Adresse': address,
        'Pole Studio Beschreibung': pole_studio_description,
        'Start Preis': starting_price,
        'Ratingscore': ratingscore,
        'Reviewanzahl': ratingcount,
        # 'Rating Faktoren': [ratingfactors],
        'E-Mail': contact_row['E-Mail'],
        'Homepage': contact_row['Homepage'],
        'Telefon': contact_row['Telefon'],
        'Eversports Pole Studio Seite': url
    }

    # create pandas dataframe
    pole_studio_overview_df = pd.DataFrame([pole_studio_overview])

    # Make a datastamp
    pole_studio_overview_df['Version'] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")

    # Drop Rating Fact
    # pole_studio_overview_df = pole_studio_overview_df.drop(["Rating Faktoren"], axis=1)

    # pole_studio_overview_df.to_csv('pole_studio_overview.csv', index=False)

    # create the "CSV" directory if it does not exist
    # if not os.path.exists("PoleStudio_CSV"):
    # os.makedirs("PoleStudio_CSV")

    # save the CSV file in the "CSV" directory
    # pole_studio_overview_df.to_csv(
    #     f"PoleStudio_CSV/{pole_studio_name}.csv", index=False)

    return pole_studio_overview_df
