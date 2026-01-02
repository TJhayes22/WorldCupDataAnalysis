from selenium import webdriver
import time
import pandas as pd
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Build path to data/raw folder (one level up from src, then into data/raw)
output_path = os.path.join(script_dir, "..", "data", "raw", "fifa_worldcup_missing_data.csv")

driver = webdriver.Chrome()

def get_missing_data(year):
    # Author: thepycoach
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

    driver.get(web)
    matches = driver.find_elements(by='xpath', value='//td[@align="right"]/.. | //td[@style="text-align:right;"]/..')
    # matches = driver.find_elements(by='xpath', value='//tr[@style="font-size:90%"]')

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find_element(by='xpath', value='./td[1]').text)
        score.append(match.find_element(by='xpath', value='./td[2]').text)
        away.append(match.find_element(by='xpath', value='./td[3]').text)

    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    time.sleep(2)
    return df_football


years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
            1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
            2018]

fifa = [get_missing_data(year) for year in years]
driver.quit()
df_fifa = pd.concat(fifa, ignore_index=True)
df_fifa.to_csv(output_path, index=False)