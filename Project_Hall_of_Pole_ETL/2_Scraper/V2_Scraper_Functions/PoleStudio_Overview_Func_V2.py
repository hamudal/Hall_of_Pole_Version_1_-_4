import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import text


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

    try:
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

    # Create a DataFrame for the contact information
    contact_df = pd.DataFrame(contact_info, columns=["E-Mail", "Homepage", "Telefon"])

    # Concatenate the contact_df with pole_studio_overview_df
    pole_studio_overview_df = pd.concat([pole_studio_overview_df, contact_df], axis=1)

