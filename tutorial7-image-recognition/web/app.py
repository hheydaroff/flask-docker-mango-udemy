from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json


app =Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017/")
db = client.ImageRecognition
users = db["users"]


def UserExists(username):
    if users.count({"username" : username}) != 0:
        return True
    else:
        return False

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if UserExists(username):
            return({
                "status" : 301,
                "message" : "Username already exists"
            })

        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

        TOKENS = 4
        users.insert({
            "username" : username,
            "password" : hashed_pw,
            "tokens" : TOKENS
        })

        return({
            "status" : 200,
            "message" : f"You signed up. You have {TOKENS} amount of tokens."
        })




def verify_pw(username, password):
    if not UserExists(username):
        return False
    
    hashed_pw = users.find({
        "username" : username
    })[0]["password"]

    if bcrypt.hashpw(password.encode("utf8"), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def generateReturnDictionary(status, msg):
    retJson ={
        "status" : status,
        "msg" : msg
    }

    return retJson


def verifyCredentials(username, password):
    if not UserExists(username):
        return generateReturnDictionary(301, "Invalid Username"), True
    
    correct_pw = verify_pw(username, password)
    if not correct_pw:
        return generateReturnDictionary(302, "Invalid Password"), True
    
    return None, False





class Classify(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]


        retJson, error = verifyCredentials(username, password)
        if error:
            return retJson
        
        tokens = users.find({"username" : username})[0]["tokens"]
        if tokens <= 0:
            return(generateReturnDictionary(303, "Not enough Tokens!"))

        r = requests.get(url)
        retJson = {}
        with open("temp.jpg", "wb") as f:
            f.write(r.content)
            process = subprocess.Popen("python3 classify_image.py --model_dir=. --image_file=./temp.jpg", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            process.communicate()[0]
            process.wait()
            with open("text.txt") as f:
                retJson = json.load(f)

            
            users.update({
                "username" : username
            },
            {
                "$set" : {"tokens" :tokens - 1}
            })
            return retJson


class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["refill_amount"]

        if not UserExists:
            return generateReturnDictionary(301, "Invalid Username")

        correct_pw = "abc123"
        if password != correct_pw:
            return generateReturnDictionary(302, "Invalid Password")

        users.update({"username" : username},
        {
            "$set" : {"tokens" : refill_amount}
        })

        return generateReturnDictionary(200, f"You refilled {refill_amount} tokens.")


api.add_resource(Register, "/register")
api.add_resource(Classify, "/classify")
api.add_resource(Refill, "/refill")


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)