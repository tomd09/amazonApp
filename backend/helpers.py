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