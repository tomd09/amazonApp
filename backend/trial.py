import os
import re
import logging
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

def initialiseConnection():
    logging.disable(logging.WARNING)
    usr = 'root'
    pwd = 'Barney2015$$'
    host = 'localhost'
    port = 3306
    dbName = 'amazonscraping'
    engine = create_engine(f'mysql+mysqldb://{usr}:{pwd}@{host}:{port}/{dbName}', future=True)
    return engine

def retrieveTable(table):
    engine = initialiseConnection()
    with engine.connect() as conn:
        df = pd.read_sql(text(f'SELECT * FROM {table};'), conn)
    return df

uncannyUrl = 'https://www.amazon.com.au/UNCANNY-X-FORCE-REMENDER-OMNIBUS-PRINTING/dp/1302957732/ref=sr_1_2?crid=18Z2HWOAF2CRG&dib=eyJ2IjoiMSJ9.YOTNRks2nVm1tZp3ZXhRsEobHBCpOn2n2AUyU2-6lj3UrBjDv__BeQDzx1LIwu7NUNLmMYz4FOCrWU7gL_7T-Q3jfqj48sOrjUm9NY8Q-BCZSmgIev2sH7vaALE1HlQWUx9mzXVdBcx9xRVZI3dRgSnd5OlOSmgAryl1nrpHDBDW6u4q0BwibAfNfXOa39h6Q0NvWx_94lN7dpIBj5Dr2S62U3u1GMgiyC6dnfhtOPkZhnEERLg1iClY-hNr4-uv16m3esL0wzZ4Cbu4GW3DtRx0A2SBm-Sx-47xhNlIqSs.KpEzAxCepp6jYEcUP3aXvKNRAW_-UL4ITs21J13JdmA&dib_tag=se&keywords=uncanny+x+force+omnibus&qid=1722520554&sprefix=uncanny+x+forceomnibus%2Caps%2C361&sr=8-2'
thorUrl = 'https://www.amazon.com.au/THOR-JASON-AARON-OMNIBUS-VOL/dp/1302953850/ref=sr_1_4?crid=1IXBJCJ2AKVE&dib=eyJ2IjoiMSJ9.5hNV-NHa8Drws5xZfcO52jjYMLprxyTq9jKPMSM1BUw7pM8cQIaqofwp3nBnnXwEji6ftdE2cYriBBC0PO_p31DmVnRqd4qCeHbb7WiQdAlAaGlZrJoe7Oz-mBn-hkLkhOcwQRX4Og85jz97nOWoTO-qqzAPfzOxnoU1XJ-ianxxPQkLvuK4jJj1wJ-oBZ0MF8vu2-oy9UUwqgUhP7wbZvFVb6thC9uBtkReCmCLTaMusbFkblImiiiz8eXfkBY2v9cisvRHvX4iinFPgqI32stPr0fTsI8qsEKZQR35i6U.FJdm1xW8HRBN8HITZSA1y4fQEr3M3QOAysnQS6AaiSI&dib_tag=se&keywords=thor+omnibus&qid=1722575851&sprefix=thor+omnibu%2Caps%2C314&sr=8-4'

def creatingSoup(url):
    #beautifulsoup to scrape amazon url with session to stop blockers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    })
    response = session.get(url)
    htmlContent = response.text
    soup = BeautifulSoup(htmlContent, 'html.parser')
    return soup

def creatingImageLinkTitle(soup):
    titles = soup.find_all('h1')
    for title in titles:
        span = title.find('span', id='productTitle')
        if span:
            span = span.text.strip().replace(' ', '-')
            title = re.sub(r'[^\w\-]', '', span)
            title = re.sub(r'-+', '-', title)
            title = f'IMAGE-{title}.jpg'
            return title
    return 'No Title Found'

def gettingImage(soup, title):
    currentDir = os.path.dirname(__name__)
    imgsFolder = os.path.join(currentDir, 'images')
    os.makedirs(imgsFolder, exist_ok=True) 
    imgTags = soup.find_all('img')
    imgUrl = imgTags[6].get('src') 
    imageResponse = requests.get(imgUrl)
    imgPath = os.path.join(imgsFolder, title)
    with open(imgPath, 'wb') as file:
        file.write(imageResponse.content)
    
def addNewItem(url, name, type):
    existingDf = retrieveTable('amazonprices')
    uniqueURLs = list(existingDf['Link'].unique())
    new = False
    if url not in uniqueURLs:
        new = True
    try:
        soup = creatingSoup(url)
        imageLinkTitle = creatingImageLinkTitle(soup)
        if new == True: #only save image if the url is fresh
            gettingImage(soup, imageLinkTitle)
        priceDiv = soup.find('div', class_='a-section a-spacing-none aok-align-center aok-relative')
        price = None
        if priceDiv:
            price = float(priceDiv.text.strip().split(' ')[-1][1:])
        df = pd.DataFrame([[name, type, url, price, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), imageLinkTitle]], columns=['Name', 'Type', 'Link', 'Price', 'Time', 'Image Link'])
        engine = initialiseConnection()
        df.to_sql(name='amazonprices', con=engine, index=False, if_exists='append')
    except:
        print('Invalid Amazon URL Supplied')
    

addNewItem(uncannyUrl, 'Uncanny X-Force Omnibus', 'Omnibus')
        
