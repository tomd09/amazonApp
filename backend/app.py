import datetime
import json
import pandas as pd
from flask import Flask, request, jsonify
from helpers import retrieveTable, addNewItem

app = Flask(__name__)

@app.route('/selectionTypes')
def getSelectionTypes():
    df = retrieveTable('amazonprices')
    types = ['All'] + list(df['Type'].unique()) 
    print(jsonify(types))
    return jsonify(types)

@app.route('/data', methods=['GET'])
def getDbData():
    option = request.args.get('option')
    print(option)
    df = retrieveTable('amazonprices')
    if option != 'All':
        df = df[df['Type'] == option]
    df['Price'] = df['Price'].fillna(value='Not Available')
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