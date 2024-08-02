import os
import re
import logging
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from sqlalchemy import create_engine, text

uncannyUrl = 'https://www.amazon.com.au/UNCANNY-X-FORCE-REMENDER-OMNIBUS-PRINTING/dp/1302957732/ref=sr_1_2?crid=18Z2HWOAF2CRG&dib=eyJ2IjoiMSJ9.YOTNRks2nVm1tZp3ZXhRsEobHBCpOn2n2AUyU2-6lj3UrBjDv__BeQDzx1LIwu7NUNLmMYz4FOCrWU7gL_7T-Q3jfqj48sOrjUm9NY8Q-BCZSmgIev2sH7vaALE1HlQWUx9mzXVdBcx9xRVZI3dRgSnd5OlOSmgAryl1nrpHDBDW6u4q0BwibAfNfXOa39h6Q0NvWx_94lN7dpIBj5Dr2S62U3u1GMgiyC6dnfhtOPkZhnEERLg1iClY-hNr4-uv16m3esL0wzZ4Cbu4GW3DtRx0A2SBm-Sx-47xhNlIqSs.KpEzAxCepp6jYEcUP3aXvKNRAW_-UL4ITs21J13JdmA&dib_tag=se&keywords=uncanny+x+force+omnibus&qid=1722520554&sprefix=uncanny+x+forceomnibus%2Caps%2C361&sr=8-2'
thorUrl = 'https://www.amazon.com.au/THOR-JASON-AARON-OMNIBUS-VOL/dp/1302953850/ref=sr_1_4?crid=1IXBJCJ2AKVE&dib=eyJ2IjoiMSJ9.5hNV-NHa8Drws5xZfcO52jjYMLprxyTq9jKPMSM1BUw7pM8cQIaqofwp3nBnnXwEji6ftdE2cYriBBC0PO_p31DmVnRqd4qCeHbb7WiQdAlAaGlZrJoe7Oz-mBn-hkLkhOcwQRX4Og85jz97nOWoTO-qqzAPfzOxnoU1XJ-ianxxPQkLvuK4jJj1wJ-oBZ0MF8vu2-oy9UUwqgUhP7wbZvFVb6thC9uBtkReCmCLTaMusbFkblImiiiz8eXfkBY2v9cisvRHvX4iinFPgqI32stPr0fTsI8qsEKZQR35i6U.FJdm1xW8HRBN8HITZSA1y4fQEr3M3QOAysnQS6AaiSI&dib_tag=se&keywords=thor+omnibus&qid=1722575851&sprefix=thor+omnibu%2Caps%2C314&sr=8-4'


def gettingImage(url):
    #beautifulsoup to scrape amazon url with session to stop blockers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })
    response = session.get(url)
    htmlContent = response.text
    soup = BeautifulSoup(htmlContent, 'html.parser')

    #getting product name
    title = soup.find_all('h1')[1].find_all('span')[0].text.strip().replace(' ', '-')
    title = re.sub(r'[^\w\-]', '', title)
    
    #finding relative file paths and constructing path to images folder
    currentDir = os.path.dirname(__name__)
    imgsFolder = os.path.join(currentDir, 'images')
    os.makedirs(imgsFolder, exist_ok=True) #creates folder if it doesn't exist

    #getting image data to write to file
    imgTags = soup.find_all('img')
    imgUrl = imgTags[6].get('src') #getting url of product image
    imageResponse = requests.get(imgUrl)
    imageName = f'IMAGE-{title}.jpg'
    imgPath = os.path.join(imgsFolder, imageName)
    with open(imgPath, 'wb') as file:
        file.write(imageResponse.content)
    return imageName
    
    
    
    
        

gettingImage(uncannyUrl)
gettingImage(thorUrl)