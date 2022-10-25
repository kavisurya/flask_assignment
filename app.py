from flask import Flask, request, jsonify
from database_controller import db
import jwt

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return 'Home page'


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        req_data = request.get_json()

        user_found = False

        try:
             # Check 1st already the email exists
            res = db.get_by_user(req_data["email"])
            
            if res["email"] == req_data["email"]:
                return jsonify({"error":"This email is already exists"})
                user_found = True

        except  Exception as e:
            pass


        if user_found == False:
          # IF not exists create new user
            res = db.insert(req_data["fname"], req_data["lname"], req_data["email"], req_data["mobile"], req_data["password"], req_data["yog"], req_data["gender"])

            if res:
                return jsonify({"success":"User created success"})
            else:
                return jsonify({"error":"User creation error! Try after some time"})

        

@app.route("/login",methods=["POST"])
def login():
    if request.method == "POST":
        req_data = request.get_json()

        res = db.get_by_user(req_data["email"])

        try:
            if res["password"] == req_data["password"]:
                return jsonify({"success":"User successfully logged in"})

            else:
                return jsonify({"error":"Password is incorrect"})

        except Exception as e:
            return jsonify({"error":"user is not found"})



if __name__ == "__main__":
    app.run(debug=False)