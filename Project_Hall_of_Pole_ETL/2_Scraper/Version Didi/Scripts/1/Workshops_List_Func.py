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
    # url = 'https://www.eversports.de/sw/schoenheitstanz-studio'
    response = requests.get(url)

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Container Workshops
    list_1 = soup.find_all(
        'div', class_="discover-results marketplace-tile-container")

    # Assuming you have already fetched the HTML content and parsed it using BeautifulSoup
    list_1 = soup.find_all('div', class_='marketplace-tile__date')

    workshops_dates = []

    # Loop through each div element and extract its text content
    for item in list_1:
        workshops_dates.append(item.text)

    # Create list of names of the workshops
    workshop_names = []

    workshops = soup.find_all(
        'div', class_="discover-results marketplace-tile-container")

    for item in workshops:
        h4_tags = item.find_all('h4')
        for tag in h4_tags:
            workshop_names.append(tag.text)

    name_soup = soup.find_all("div", class_="container discover-container")
    name_soup

    for item in name_soup:
        h1_tag = item.find_all("h1")
        for h1 in h1_tag:
            polestudio_name = h1.text

    polestudio_name_cl = polestudio_name.split(" ")[0]

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
