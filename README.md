# Current-Projects

Data Analyses, Data Engineering , Data science

All For One Scraper

Introduction
The All For One Scraper is a Python script that extracts workshop information from multiple pole dancing studio websites and saves it to a CSV file. The script uses web scraping techniques to collect workshop names, dates, prices, and other details from each studio's workshop page. The script is designed to automate the process of collecting workshop information from multiple studio websites, saving you time and effort.

Usage
To use the All For One Scraper script, follow these steps:

In the All_For_One file, edit the following codeline at the end of the script and replace the URL, or insert multiple URLs, seperated by commas:

# Get user input for a list of URLs

user_input = "https://www.eversports.de/sw/yoga-and-pole-art-by-selina, ".." "

The script will then automatically collect all the workshop links from each of these pages.

Run the One_For_All.py script by just running the script, or use your terminal. This script will collect all of the workshop details from each of the workshop pages previously collected.

The script will save the workshop information as a CSV file in the CSV directory. Each studio's workshops will be saved as a separate CSV file, named after the studio's name. The CSV file will contain the following columns:

workshop_name
date
time
price
duration
level
location
instructor

Additionally, if the script finds a 'Pole Studio Eversports Seite' column in the workshop information CSV files, it will automatically extract the pole studio overview information for each pole studio, including studio name, address, starting price, taster course price, ratings, and contact information. This information will be saved as a separate CSV file in the 'PoleStudio_CSV' directory.

Requirements
To use the One_For_All script, you will need the following:

Python 3
The following Python libraries:

os
re
glob
requests
BeautifulSoup
pandas
datetime

The Pole Studio Scraper script is intended for educational and research purposes only. The script should not be used for commercial purposes without the consent of the studio owners.

Conclusion
The Pole Studio Workshop Overview script is a powerful tool that can help you stay organized and informed about upcoming pole dancing workshops at various studios. With just a few clicks, you can scrape workshop information from multiple websites and save it to a CSV file for easy reference. Happy scraping!

PS: This was my first selv managed project and was much fun. I would lie, if I said, it was easy, but it was worth it. Learning by doing and trial & error taught me much more, than just "watching" or learning.

To create the One For All Scraper script took around 110h of learning, coding and debugging.
