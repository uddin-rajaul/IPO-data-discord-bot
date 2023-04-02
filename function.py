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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                    options=chrome_options)
    return driver



if __name__ == "__main__":
    print("creating driver....")
    driver = get_driver()
    print('success')
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
    lastClosing_date = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[8]')
    issue_manager = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[10]')
    status = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr/td[11]')

    table_data = []
    df = pd.DataFrame(
        columns=['SN', 'Symbol', 'Units', 'Price', 'Opening Date', 'Closing Date', 'Last Closing Date', 'Issue Manager',
                 'Status'])

    for i in range(len(row[:10])):
        df = {
            'SN': sn[i].text,
            'Symbol': symbol[i].text,
            'Units': units[i].text,
            'Price': price[i].text,
            'Opening Date': opening_date[i].text,
            'Closing Date': closing_date[i].text,
            'Last Closing Date': lastClosing_date[i].text,
            'Issue Manager': issue_manager[i].text,
            'Status': status[i].text
        }
        table_data.append(df)
    df_data = pd.DataFrame(table_data)
    print(df_data)
    filtered_data = df_data[(df_data['Status'] == 'Open') | (df_data['Status'] == 'Coming Soon')]
    print(filtered_data)

