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

        # Checking input's
        gender_ = 0

        if req_data["fname"] == "" or len(req_data["fname"]) < 4:
            return jsonify({"error":"Check the firstname,firstname chars should be 4"}), 421

        elif req_data["lname"] == "" or len(req_data["lname"]) < 3:
            return jsonify({"error":"Check the lastname, lastname chars should be 3"}), 421

        elif req_data["email"] == "" or len(req_data["email"]) < 5:
            return jsonify({"error":"Check the mail-id"}), 421

        elif len(req_data["mobile"]) != 10:
            return jsonify({"error":"Mobile number chars should be 10"}), 421


        elif len(req_data["yog"]) != 4:
            return jsonify({"error":"Mobile number chars should be 4"}), 421

        elif len(req_data["password"]) < 8:
            return jsonify({"error":"Password length should be 8"}), 421


        if req_data["gender"] != "female":
            gender_ += 1 

        elif req_data["gender"] != "male":
            gender_ += 1 

        if gender_ != 1:
            return jsonify({"error":"gender should be male or female"}), 421


        user_found = False

        try:
             # Check 1st already the email exists
            res = db.get_by_user(req_data["email"])
            
            if res["email"] == req_data["email"]:
                return jsonify({"error":"This email is already exists"}), 401
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
                return jsonify({"error":"Password is incorrect"}), 401

        except Exception as e:
            return jsonify({"error":"user is not found"}), 404



@app.route("/profile_update", methods=["PUT"])
def update_user():
    if request.method == "PUT":
        req_data = request.get_json()

        # Checking input's
        if req_data["fname"] == "" or len(req_data["fname"]) < 4:
            return jsonify({"error":"Check the firstname,firstname chars should be 4"}), 421

        elif req_data["lname"] == "" or len(req_data["lname"]) < 3:
            return jsonify({"error":"Check the lastname, lastname chars should be 3"}), 421

        elif req_data["email"] == "" or len(req_data["email"]) < 5:
            return jsonify({"error":"Check the mail-id"}), 421

        elif len(req_data["mobile"]) != 10:
            return jsonify({"error":"Mobile number chars should be 10"}), 421


        elif len(req_data["yog"]) != 4:
            return jsonify({"error":"Mobile number chars should be 4"}), 421


        elif req_data["gender"] != "male" or req_data["gender"] != "female":
            return jsonify({"error":"gender should be male or female"}), 421

        user_found = False

        try:
             # Check 1st already the email exists
            res = db.get_by_user(req_data["email"])
            
            if res["email"] != req_data["email"]:
                return jsonify({"error":"This email is not found"})
                user_found = True

        except  Exception as e:
            pass


        if user_found == False:
          # IF not exists create new user
            res = db.update(req_data["fname"], req_data["lname"], req_data["email"], req_data["mobile"], req_data["yog"], req_data["gender"])

            if res:
                return jsonify({"success":"User updated success"})
            else:
                return jsonify({"error":"User updation error! Try after some time"}), 421
    else:
        return jsonify({"error":"Only PUT method allowed"}), 421




@app.route("/profile_update/<email_id>", methods=["GET"])
def get_user_details(email_id):

    if request.method == "GET":

        # Checking input's
        if email_id == "" or len(email_id) < 5:
            return jsonify({"error":"Check the mail-id"}), 421

        user_found = False
        email = email_id
        result = ""

        try:
            # Check 1st already the email exists
            res = db.get_by_user(email_id)
            result = res
            if res["email"] != email_id:
                return jsonify({"error":"This email is not found"})
                user_found = True
        except  Exception as e:
            pass

        if user_found == False:
            if result:

                data = {
                        'id': str(result["_id"]), 
                        'fname': result["fname"], 
                        'lname': result["lname"], 
                        'email': result["email"], 
                        'mobile': result["mobile"], 
                        'yog': result["yog"], 
                        'gender': result["gender"]
                    }

                return jsonify({"success": data})
            else:
                return jsonify({"error":"User fetching error! Try after some time"}), 421
    
    else:
        return jsonify({"error":"Only GET method allowed"}), 421





@app.route("/delete_account/<email_id>", methods=["DELETE"])
def delete_account(email_id):
    if request.method == "DELETE":

        # Checking input's
        if email_id == "" or len(email_id) < 5:
            return jsonify({"error":"Check the mail-id"}), 421

        try:
             # Check 1st the email exists
            res = db.get_by_user(email_id)
            
            if res["email"] == email_id:
                
                # Delete the account
                result = db.delete(email_id)

                if result:
                    return jsonify({"success":"The account deleted successfully"})
                else:
                    return jsonify({"error":"Can't delete the account! please try after some time"})

            else:
                return jsonify({"error":"This email is not found"}), 404

        except  Exception as e:
            return jsonify({"error":"This email is not found"}), 404


    else:
        return jsonify({"error":"Only DELETE method allowed"}), 421




if __name__ == "__main__":
    app.run(debug=False)