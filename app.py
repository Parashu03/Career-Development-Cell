from flask import Flask, request, jsonify
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/college"
mongo = PyMongo(app).db

@app.route("/")
def hello_world():
    mongo.student.insert_one({"a":2})
   
    return"<p> Hello,wolrd! </p>"


app.run(debug=True, port=50001)
