import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def scrape_data():
    driver = get_driver()
    url = 'https://www.sharesansar.com/existing-issues#'
    driver.get(url)
    driver.maximize_window()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # to calculate no. of row in table
    row = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr[@class="odd" or @class="even"]')

    # extracting row information
    sn = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[1]')
    symbol = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[2]/a')
    company = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[3]/a')
    units = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[4]')
    price = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[5]')
    opening_date = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[6]')
    closing_date = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[7]')
    last_closing_date = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[8]')
    issue_manager = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[10]')
    status = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[11]')

    table_data = []
    df = pd.DataFrame(
        columns=['SN', 'Symbol', 'Units', 'Price', 'Opening Date', 'Closing Date', 'Last Closing Date', 'Issue Manager',
                 'Status'])

    for i in range(len(row)):
        df = {
            'SN': sn[i].text,
            'Symbol': symbol[i].text,
            'Company': company[i].text,
            'Units': units[i].text,
            'Price': price[i].text,
            'Opening Date': opening_date[i].text,
            'Closing Date': closing_date[i].text,
            'Last Closing Date': last_closing_date[i].text,
            'Issue Manager': issue_manager[i].text,
            'Status': status[i].text
        }
        table_data.append(df)
    df_data = pd.DataFrame(table_data)
    return df_data


def get_data_by_status(status):
    df = scrape_data()

    # Filter data by status
    filtered_df = df[df['Status'] == status]

    # Convert filtered data to list of dictionaries
    data = filtered_df.to_dict('records')

    return data