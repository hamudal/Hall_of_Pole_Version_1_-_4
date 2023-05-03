import re
import pandas as pd
from PoleStudio_Overview_Func import pole_overview
from Workshops_List_Func_V2 import workshop_list
from Workshop_Overview_Func import workshop_overview

import datetime


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
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')

    # Save the CSV file in the "CSV" directory with timestamp
    all_workshops_didi_df.to_csv(
        f"1_Workshops_List_Didi_Ws_{timestamp}.csv", index=False)

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
        f"1_Workshop_Overview_Didi_e_{timestamp}.csv", index=False)

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
        f"1_PoleStudio_Overview_Didi_{timestamp}.csv", index=False)

    return all_workshops_didi_df, all_workshops_overview_didi_df, all_polestudios_overview_didi_df
