from flask import Flask ,request,jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017')  
db = client['CDC']  
collection = db['Student_details'] 
  


if __name__ == '__main__':
    app.run(debug=True)