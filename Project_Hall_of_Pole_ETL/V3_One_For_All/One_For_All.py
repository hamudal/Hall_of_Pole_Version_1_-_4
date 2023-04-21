import os
import re
import glob
import requests
from bs4 import BeautifulSoup
import pandas as pd

import datetime
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
    if not os.path.exists("Workshop_List_CSV"):
        os.makedirs("Workshop_List_CSV")

    # save the CSV file in the "CSV" directory
    # poleworkshop_list_df.to_csv(
    #     f"Workshop_List_CSV/{polestudio_name_cl}.csv", index=False)

    return poleworkshop_list_df


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

    # Loop through each element in the container
    for item in starting_price_:
        # Starting Price
        starting_price = item.find(
            'p', class_='MuiTypography-root MuiTypography-body1 css-13ps6ou').text

        # Taster Course Price
        taster_course_price = item.find(
            'p', class_="MuiTypography-root MuiTypography-body1 css-13ps6ou").text

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
        'Schnupperkurspreis': taster_course_price,
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

    # create pandas dataframe
    pole_studio_overview_df = pd.DataFrame([pole_studio_overview])

    # Make a datastamp
    pole_studio_overview_df['Version'] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")

    # Drop Rating Fact
    # pole_studio_overview_df = pole_studio_overview_df.drop(["Rating Faktoren"], axis=1)


    # create the "CSV" directory if it does not exist
    if not os.path.exists("PoleStudio_CSV"):
        os.makedirs("PoleStudio_CSV")

    # save the CSV file in the "CSV" directory
    # pole_studio_overview_df.to_csv(
    #     f"PoleStudio_CSV/{pole_studio_name}.csv", index=False)

    return pole_studio_overview_df


def super_function(urls):
    # Workshop List Function
    url_list = urls
    workshop_list_dfs = []

    for url in url_list:
        workshop_list_df = workshop_list(url)
        workshop_list_dfs.append(workshop_list_df)

    # Concatenate all workshop_list_dfs into one DataFrame
    all_workshops_didi_df = pd.concat(workshop_list_dfs, ignore_index=True)

    # Timestamp for the CSV file name
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')

    # Save the CSV file in the "CSV" directory with timestamp
    all_workshops_didi_df.to_csv(
        f"Workshop_List_CSV/1_Workshops_List_Didi_Ws_{timestamp}.csv", index=False)

    # Workshop Overview
    url_list = all_workshops_didi_df["Workshop Seite Eversports"].to_list()
    workshop_overview_dfs = []

    for url in url_list:
        workshop_overview_df = workshop_overview(url)
        workshop_overview_dfs.append(workshop_overview_df)

    # Concatenate all workshop_overview_dfs into one DataFrame
    all_workshops_overview_didi_df = pd.concat(
        workshop_overview_dfs, ignore_index=True)

    # Replace underscores with whitespaces in the 'Workshop Name' column
    all_workshops_overview_didi_df['Workshop Name'] = all_workshops_overview_didi_df['Workshop Name'].apply(
        lambda x: x.replace('_', ' '))

    # Save the CSV file in the "CSV" directory with timestamp
    all_workshops_overview_didi_df.to_csv(
        f"Workshop_CSV/1_Workshop_Overview_Didi_e_{timestamp}.csv", index=False)

    # Pole Studios Overview
    url_list = all_workshops_overview_didi_df['PoleStudio Eversports Seite'].tolist(
    )
    url_list = list(set(url_list))
    polestudio_overview_dfs = []

    for url in url_list:
        polestudio_overview_df = pole_overview(url)
        polestudio_overview_dfs.append(polestudio_overview_df)

    # Concatenate all polestudio_overview_dfs into one DataFrame
    all_polestudios_overview_didi_df = pd.concat(
        polestudio_overview_dfs, ignore_index=True)

    # Save the CSV file in the "CSV" directory with timestamp
    all_polestudios_overview_didi_df.to_csv(
        f"PoleStudio_CSV/1_PoleStudio_Overview_Didi_{timestamp}.csv", index=False)

    return all_workshops_didi_df, all_workshops_overview_didi_df, all_polestudios_overview_didi_df


# Get user input for a list of URLs
user_input = "https://www.eversports.de/sw/yoga-and-pole-art-by-selina"

# user_input = input("Enter URLs separated by commas: ")

# Split the input string into a list of URLs
url_list = [url.strip() for url in user_input.split(',')]

# Call the super_function with the list of URLs
workshops_df, workshops_overview_df, polestudios_overview_df = super_function(url_list)

# Display the DataFrames
print(workshops_df)
print(workshops_overview_df)
print(polestudios_overview_df)

if __name__ == "__main__":
    all_workshops_didi_df, all_workshops_overview_didi_df, all_pole_studio_overview_didi_df = super_function(user_input)

    print("Workshops List DataFrame")
    print(all_workshops_didi_df.head())

    print("Workshops Overview DataFrame")
    print(all_workshops_overview_didi_df.head())

    print("Pole Studio Overview DataFrame")
    print(all_pole_studio_overview_didi_df.head())

