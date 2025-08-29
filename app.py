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
        return redirect(url_for('user_dashboard', usn=usn))
    return "Invalid USN or password!", 401

@app.route('/user_dashboard/<usn>')
def user_dashboard(usn):
    user = students_collection.find_one({'usn': usn})
    if not user:
        return "User not found!", 404
    return render_template('user_dash.html', user=user)

@app.route('/save_profile/<usn>', methods=['POST'])
def save_profile(usn):
    user = students_collection.find_one({'usn': usn})
    if not user:
        return "User not found!", 404

    # Collect form data
    profile_data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'location': request.form.get('location'),
        'linkedin': request.form.get('linkedin'),
        'github': request.form.get('github'),
        'summary': request.form.get('summary'),
        'skills': request.form.get('skills').split(',') if request.form.get('skills') else [],
        'education': [
            {
                'degree': request.form.getlist('education_degree[]')[i],
                'institution': request.form.getlist('education_institution[]')[i],
                'year': request.form.getlist('education_year[]')[i],
                'gpa': request.form.getlist('education_gpa[]')[i]
            } for i in range(len(request.form.getlist('education_degree[]')))
        ] if request.form.getlist('education_degree[]') else [],
        'projects': [
            {
                'title': request.form.getlist('project_title[]')[i],
                'desc': request.form.getlist('project_desc[]')[i],
                'tech': request.form.getlist('project_tech[]')[i]
            } for i in range(len(request.form.getlist('project_title[]')))
        ] if request.form.getlist('project_title[]') else [],
        'achievements': [
            {
                'title': request.form.getlist('achievement_title[]')[i],
                'desc': request.form.getlist('achievement_desc[]')[i]
            } for i in range(len(request.form.getlist('achievement_title[]')))
        ] if request.form.getlist('achievement_title[]') else [],
        'experience': [
            {
                'title': request.form.getlist('exp_title[]')[i],
                'company': request.form.getlist('exp_company[]')[i],
                'duration': request.form.getlist('exp_duration[]')[i],
                'desc': request.form.getlist('exp_desc[]')[i]
            } for i in range(len(request.form.getlist('exp_title[]')))
        ] if request.form.getlist('exp_title[]') else [],
        'certifications': [
            {
                'name': request.form.getlist('cert_name[]')[i],
                'org': request.form.getlist('cert_org[]')[i],
                'date': request.form.getlist('cert_date[]')[i]
            } for i in range(len(request.form.getlist('cert_name[]')))
        ] if request.form.getlist('cert_name[]') else []
    }

    # Handle photo upload
    if 'photo' in request.files:
        file = request.files['photo']
        if file.filename:
            filename = secure_filename(f"{usn}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_data['photo'] = filename

    # Update user profile
    students_collection.update_one({'usn': usn}, {'$set': {'profile': profile_data}})
    return redirect(url_for('user_dashboard', usn=usn))


@app.route("/admin")
def admin():
    return render_template("admin_dashboard2.html")


app.run(debug=True, port=50001)
