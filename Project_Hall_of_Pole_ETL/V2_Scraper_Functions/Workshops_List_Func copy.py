import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

import re
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import text


def workshop_list(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract workshops dates
    list_1 = soup.find_all('div', class_='marketplace-tile__date')
    workshops_dates = [item.text for item in list_1]

    # Extract workshop names
    workshop_names = []
    workshops = soup.find_all(
        'div', class_='discover-results marketplace-tile-container')
    try:
        for item in workshops:
            h4_tags = item.find_all('h4')
            for tag in h4_tags:
                workshop_names.append(tag.text)
    except AttributeError:
        print(f"No workshops found on {url}")

    # Extract pole studio name
    name_soup = soup.find_all('div', class_='container discover-container')
    polestudio_name = "0"
    try:
        for item in name_soup:
            h1_tag = item.find_all('h1')
            for h1 in h1_tag:
                polestudio_name = h1.text
        polestudio_name_cl = polestudio_name.split(" ")[0]
    except AttributeError:
        print(f"No pole studio name found on {url}")
        polestudio_name_cl = 0

    # Extract price information
    price_elements = soup.find_all('div', class_='marketplace-tile__price')
    prices = []
    try:
        for item in price_elements:
            if item.find('span'):
                prices.append(item.find('span').text)
            else:
                prices.append('')
    except AttributeError:
        print(f"No price information found on {url}")

    # Create a dictionary of the extracted information
    workshop_dict = {'polestudio_name': polestudio_name_cl, 'workshop_name': workshop_names, 'date': workshops_dates,
                     'price': prices}

    # Convert the dictionary to a Pandas DataFrame and return it
    return pd.DataFrame(workshop_dict)

    # Assign a default value to polestudio_name
    polestudio_name = "0"

    for item in name_soup:
        h1_tag = item.find_all("h1")
        for h1 in h1_tag:
            try:
                polestudio_name_cl = polestudio_name.split(" ")[0]
            except UnboundLocalError:
                polestudio_name_cl = "Not Found"

    # Extract all div elements with class "marketplace-tile__price"
    price_elements = soup.find_all('div', class_='marketplace-tile__price')

    # Extract the text content of each price element
    workshop_prices = [price.text.strip() for price in price_elements]

    # find all links inside the container and create a list

    links = [a['href'] for a in soup.find(
        'div', class_='discover-results marketplace-tile-container').find_all('a')]

    workshop_page_eversports = []
    base_url = "https://www.eversports.de"

    workshop_page_eversports = [base_url + link for link in links]
    workshop_page_eversports

    # create a dictionary from the given lists
    poleworkshop_list_df = {
        'Workshop Name': workshop_names,
        'PoleStudio': polestudio_name_cl,
        # 'Workshop Datum': workshops_dates,
        # 'Workshop Preis': workshop_prices,
        'Workshop Seite Eversports': workshop_page_eversports,

    }

    # create pandas dataframe
    poleworkshop_list_df = pd.DataFrame.from_dict(poleworkshop_list_df)

    # Add a new column to the DataFrame with the current date and time
    poleworkshop_list_df['Version'] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")

    # create the directory if it doesn't exist
    # if not os.path.exists("Workshop_List_CSV"):
    # os.makedirs("Workshop_List_CSV")

    # save the CSV file in the "CSV" directory
    # poleworkshop_list_df.to_csv(
    #     f"Workshop_List_CSV/{polestudio_name_cl}.csv", index=False)

    return poleworkshop_list_df
