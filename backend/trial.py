import os
import re
import time
import json
import random
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
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
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
    print('found all img tags')
    for tag in imgTags:
        src = tag.get('src')
        if src == None:
            pass
        elif src.startswith(desiredPrefix) and '_SX' in src and '_SY' in src:
            imgUrl = src
            print('found desired src')
            break
    print('trying image request')
    imageResponse = requests.get(imgUrl)
    print('got image response')
    imgPath = os.path.join('static', 'images', title)
    print('got image path')
    with open(imgPath, 'wb') as file:
        print('opened attempting to write')
        file.write(imageResponse.content)
    
def addNewImage(url):
    try:
        soup = creatingSoup(url)
        print('got soup')
        imageLinkTitle = creatingImageLinkTitle(soup)
        print('got link title')
        gettingImage(soup, imageLinkTitle)
    except:
        print('Invalid Amazon URL Supplied')
  
urlList = [
    'https://www.amazon.com.au/Indiana-77015-Building-Interactive-Functions/dp/B0BV7CHRW2/ref=sr_1_1?crid=3LDFQ1V5Y1VMM&dib=eyJ2IjoiMSJ9.I0CdmC3RJbl4nm-3w0pJGeF8g04W5byw8yc29J0B3BOYUJ4memHVMSLVjGfv5mEvrstcULfzFXzQnDMHB-HCgFakpMnAL9akNp1seEXoR2KBaIMjfCvUM9_-scLAM1jLoQotQNqIV309qMF79xhuXT5n5iOhH38zRqHbLU2FPbbT2p_g3L_RRfqgjDWzZNx6gEJFRsWCKPqoJCdGxN3jg72h5nQMlOiJh8N6L4T4PGBZ2d1iD9XbnJcpJz26cMzZYestjx-A8MfW-Y6AS6fkS4THrPYFn0qCHk9llJVVbZ4.wUvtAuQ4gowE35bv8t5b1S_yhfFkF-onAOS-JS-vmLQ&dib_tag=se&keywords=lego+indiana+jones&qid=1721293127&sprefix=lego+indiana+jop%2Caps%2C290&sr=8-1',
    'https://www.amazon.com.au/LEGO-75357-Featuring-Brick-Built-Characters/dp/B0BV7FZH9C/ref=pd_sbs_d_sccl_2_4/356-9332776-0832204?pd_rd_w=qOOsQ&content-id=amzn1.sym.7f674399-a0fd-47af-a964-c980facc0dec&pf_rd_p=7f674399-a0fd-47af-a964-c980facc0dec&pf_rd_r=PH8N98HX43B0A4ME2SPY&pd_rd_wg=9uD1e&pd_rd_r=1cee9c0b-40d1-466e-976d-d4c5f66cba0d&pd_rd_i=B0BV7FZH9C&psc=1'
]

addNewImage(urlList[0])



# ghost and phantom
#indiana jones
