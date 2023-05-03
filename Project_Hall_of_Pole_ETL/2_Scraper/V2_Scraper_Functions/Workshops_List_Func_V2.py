import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

import re
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import text

def workshop_list(url):
    """
    Returns a pandas DataFrame with a list of workshops and their details from the given Eversports URL.

    Args:
        url (str): The URL of the Eversports page to scrape.

    Returns:
        pandas.DataFrame: A DataFrame with the following columns:
            - Workshop Name
            - PoleStudio
            - Workshop Seite Eversports
            - Version
    """

    try:
        # Send a GET request to the webpage
        response = requests.get(url)

        # Raise an exception for unsuccessful status codes
        response.raise_for_status()

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the name of the pole studio
        polestudio_name_tag = soup.find('h1')
        if polestudio_name_tag is not None:
            polestudio_name = polestudio_name_tag.text.split(" ")[0]
        else:
            polestudio_name = "No Pole Studio Name Found"

        # Extract all workshop containers
        workshop_containers = soup.find_all('div', class_="discover-results marketplace-tile-container")

        # Extract the names and Eversports page URLs of the workshops
        workshop_names = [tag.text for container in workshop_containers for tag in container.find_all('h4')]
        workshop_page_eversports = ["https://www.eversports.de" + link['href'] for container in workshop_containers for link in container.find_all('a')]

        # Create a dictionary from the given lists
        poleworkshop_list_df = {
            'Workshop Name': workshop_names,
            'PoleStudio': polestudio_name,
            'Workshop Seite Eversports': workshop_page_eversports,
        }

        # Create pandas dataframe
        poleworkshop_list_df = pd.DataFrame.from_dict(poleworkshop_list_df)

        # Add a new column to the DataFrame with the current date and time
        poleworkshop_list_df['Version'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return poleworkshop_list_df

    except requests.exceptions.RequestException as e:
        print(f"Error while checking URL '{url}': {e}")
        return pd.DataFrame()
