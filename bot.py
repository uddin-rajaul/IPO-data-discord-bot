
# # bot.py
import os
import discord
import asyncio
import requests
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()


client = discord.Client(intents=intents)
url = 'https://www.sharesansar.com/existing-issues#'

TOKEN = os.getenv('TOKEN')

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


async def scrape_data():
    driver = get_driver()
    url = 'https://www.sharesansar.com/existing-issues#'
    driver.get(url)
    driver.maximize_window()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    row = driver.find_elements(By.XPATH, '//*[@id="myTableEip"]/tbody/tr[@class="odd" or @class="even"]')
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
    return df_data


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')


@client.event
async def on_message(message):
    if message.content.startswith('$scrape'):
        await message.channel.send("Scraping data...")

        today = pd.to_datetime('today').strftime('%Y-%m-%d')
        if os.path.isfile(f'sharesansar_data_{today}.csv'):
            # File exists, read from it
            # df = pd.read_csv(f'sharesansar_data_{today}.csv')
            df_data = pd.read_csv(f'sharesansar_data_{today}.csv')
            open_data = df_data[df_data['Status'] == 'Open']
            coming_soon_data = df_data[df_data['Status'] == 'Coming Soon']
            channel = client.get_channel(947753526761758771)  # Replace channel_id with your channel id
            if not open_data.empty:
                message = "**Open IPOs**\n\n"
                for index, row in open_data.iterrows():
                    message += f"**{row['Symbol']}**\nUnits: {row['Units']}\nPrice: {row['Price']}\nOpening Date: {row['Opening Date']}\nClosing Date: {row['Closing Date']}\nIssue Manager: {row['Issue Manager']}\n\n"
                await channel.send(message)

            if not coming_soon_data.empty:
                message = "\n\n**Upcoming IPOs**\n\n"
                for index, row in coming_soon_data.iterrows():
                    message += f"**{row['Symbol']}**\nUnits: {row['Units']}\nPrice: {row['Price']}\nOpening Date: {row['Opening Date']}\nClosing Date: {row['Closing Date']}\nIssue Manager: {row['Issue Manager']}\n\n"
                await channel.send(message)
        else:
            data = await scrape_data()
            df = pd.DataFrame(data)
            df.to_csv(f'sharesansar_data_{today}.csv')
            df_data = pd.read_csv(f'sharesansar_data_{today}.csv')
            open_data = df_data[df_data['Status'] == 'Open']
            coming_soon_data = df_data[df_data['Status'] == 'Coming Soon']
            channel = client.get_channel(947753526761758771)  # Replace channel_id with your channel id
            if not open_data.empty:
                message = "**Open IPOs**\n\n"
                for index, row in open_data.iterrows():
                    message += f"**{row['Symbol']}**\nUnits: {row['Units']}\nPrice: {row['Price']}\nOpening Date: {row['Opening Date']}\nClosing Date: {row['Closing Date']}\nIssue Manager: {row['Issue Manager']}\n\n"
                await channel.send(message)

            if not coming_soon_data.empty:
                message = "\n\n**Upcoming IPOs**\n\n"
                for index, row in coming_soon_data.iterrows():
                    message += f"**{row['Symbol']}**\nUnits: {row['Units']}\nPrice: {row['Price']}\nOpening Date: {row['Opening Date']}\nClosing Date: {row['Closing Date']}\nIssue Manager: {row['Issue Manager']}\n\n"
                await channel.send(message)


client.run(TOKEN)
