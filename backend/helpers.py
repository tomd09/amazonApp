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

def addNewItem(url, name, type):
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        response = session.get(url)
        htmlContent = response.text
        soup = BeautifulSoup(htmlContent, 'html.parser')
        priceDiv = soup.find('div', class_='a-section a-spacing-none aok-align-center aok-relative')
        price = None
        if priceDiv:
            price = float(priceDiv.text.strip().split(' ')[-1][1:])
        df = pd.DataFrame([[name, type, url, price, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]], columns=['Name', 'Type', 'Link', 'Price', 'Time'])
        engine = initialiseConnection()
        df.to_sql(name='amazonprices', con=engine, index=False, if_exists='append')
    except:
        print('Invalid Amazon URL Supplied')


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
    imgUrl = '' 
    desiredPrefix = 'https://m.media-amazon.com/images/I/'
    for tag in imgTags:
        src = tag.get('src')
        if src.startswith(desiredPrefix):
            imgUrl = src
            break
    imageResponse = requests.get(imgUrl)
    imgPath = os.path.join(imgsFolder, title)
    with open(imgPath, 'wb') as file:
        file.write(imageResponse.content)
    
def addNewItem(url, name, type):
    existingDf = retrieveTable('amazonprices')
    uniqueURLs = list(existingDf['Link'].unique())
    new = False
    #if url not in uniqueURLs:
        #new = True
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