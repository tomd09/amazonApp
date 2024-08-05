import datetime
import json
import pandas as pd
from flask import Flask, request, jsonify
from helpers import retrieveTable, addNewItem

app = Flask(__name__)

@app.route('/data')
def getDbData():
    df = retrieveTable('amazonprices')
    df['Price'] = df['Price'].fillna(value='Not Available')
    print(df.columns)
    records = df.to_dict(orient='records')
    jsonData = json.dumps(records, indent=4)
    return jsonData

@app.route('/addItem', methods=['POST'])
def addNewItemsToDB():
    data = request.get_json()
    itemUrl = data.get('itemUrl')
    itemName = data.get('itemName')
    itemType = data.get('itemType')
    addNewItem(itemUrl, itemName, itemType)
    return data

if __name__ == '__main__':
    app.run(debug=True)