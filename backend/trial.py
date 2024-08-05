import os
import re
import json
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
    imgTags = soup.find_all('img')
    imgUrl = '' 
    desiredPrefix = 'https://m.media-amazon.com/images/I/'
    for tag in imgTags:
        src = tag.get('src')
        if src.startswith(desiredPrefix):
            imgUrl = src
            break
    imageResponse = requests.get(imgUrl)
    imgPath = os.path.join('backend\\static\\images', title)
    print('got img path')
    print(imgPath)
    with open(imgPath, 'wb') as file:
        file.write(imageResponse.content)
    
def addNewItem(url, name, type):
    try:
        soup = creatingSoup(url)
        imageLinkTitle = creatingImageLinkTitle(soup)
        gettingImage(soup, imageLinkTitle)
    except:
        print('Invalid Amazon URL Supplied')


jldURL = 'https://www.amazon.com.au/Justice-League-Dark-Rebirth-Omnibus/dp/1779525885/ref=sr_1_3?crid=1JXYVU16IOZZ3&dib=eyJ2IjoiMSJ9.F0TWsb6NJaFu73K2-I3FtNokGrRt4LYZTd65VKmSXIsmAD5bxOtYSISgo1k7B3oFazPhG7pj4fx2W7MdYwfNekx9ysiPOD3Yk-D9fKJ1erAlf14W8NAt1Zto9XzQ0vQgym0QiBGK-HxY2fTkBv9W1WIbI23gPv7iCEjsY1ndCduWAgzzdXiP6vgjRlgmKC095XXinHvLGDQPZ11c2WRtswgaf7I5cRiUVxEqn7YmOSGlvUWa4iXk-csMtKYV-ha3i6YwAbDVIigHrdV1qQfZ-upe9-g10i2nnuaXxD-mcUU.S5xZx7ZtdOl7oxy8wBLp7OFZF0qZdTvoC4_08ogSqoQ&dib_tag=se&keywords=justice+league+dark+omnibus&qid=1722865065&sprefix=justice+league+dark+omnibu%2Caps%2C337&sr=8-3'

addNewItem(jldURL, 'Justice League Dark Rebirth', 'Omnibus')