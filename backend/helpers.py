import os
import re
import logging
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

currentTable = 'historicaldata'

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
    datetimeColumns = df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns
    for column in datetimeColumns:
        df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

def retrieveItemList(table):
    engine = initialiseConnection()
    with engine.connect() as conn:
        df = pd.read_sql(text(f'SELECT * FROM {table};'), conn)
    df = df.sort_values(by='Time', ascending=False).drop_duplicates(subset='Link', keep='first')
    datetimeColumns = df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns
    for column in datetimeColumns:
        df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df
    

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
            spanText = re.sub(r'[^\w\-]', '', span)
            spanText = re.sub(r'-+', '-', spanText)
            segments = spanText.split('-')[:12]
            limitedTitle = '-'.join(segments)
            title = f'IMAGE-{limitedTitle}.jpg'
            return title
    return 'No Title Found'

def gettingImage(soup, title):
    imgTags = soup.find_all('img')
    imgUrl = '' 
    desiredPrefix = 'https://m.media-amazon.com/images/I/'
    for tag in imgTags:
        src = tag.get('src')
        if src.startswith(desiredPrefix):
            imgUrl = src
            break
    imageResponse = requests.get(imgUrl)
    imgPath = os.path.join('static', 'images', title)
    os.makedirs(os.path.dirname(imgPath), exist_ok=True)
    with open(imgPath, 'wb') as file:
        file.write(imageResponse.content)
    
def addNewItem(url, name, type):
    existingDf = retrieveTable(currentTable)
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
        df.to_sql(name=currentTable, con=engine, index=False, if_exists='append')
    except:
        print('Invalid Amazon URL Supplied')