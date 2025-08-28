from flask import Flask, request, jsonify, render_template ,redirect,url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/college"
mongo = PyMongo(app).db
students_collection = mongo['students']

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = {
        'name': request.form['name'],
        'usn': request.form['usn'],
        'mobile': request.form['mobile'],
        'email': request.form['email'],
        'gender': request.form['gender'],
        'password': request.form['password']  # Note: In production, hash the password
    }
    if students_collection.find_one({'usn': data['usn']}):
        return "USN already exists!", 400
    students_collection.insert_one(data)
    return redirect(url_for('landing'))

@app.route('/login', methods=['POST'])
def login():
    usn = request.form['usn']
    password = request.form['password']
    user = students_collection.find_one({'usn': usn, 'password': password})
    if user:
        return redirect(url_for('user'), usn=usn)
    return "Invalid USN or password!", 401


@app.route("/user")
def user():
    return render_template("user_dash.html")

@app.route("/admin")
def admin():
    return render_template("admin_dashboard2.html")


app.run(debug=True, port=50001)
