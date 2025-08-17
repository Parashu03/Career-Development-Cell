from flask import Flask ,request,jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017')  
db = client['CDC']  
collection = db['Student_details'] 
  
@app.route("/user/<username>")
def user_profile(username):
    user = db.collection.find_one_or_404({"_id": username})
    return render_template("student_dashboard.html",user=user)

if __name__ == '__main__':
    app.run(debug=True)