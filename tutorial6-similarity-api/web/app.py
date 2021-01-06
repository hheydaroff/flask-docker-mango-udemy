from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient

import bcrypt

import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["users"]

def UsernameExists(username):
    if users.count({"username" : username}) != 0:
        return True
    else:
        return False



class Register(Resource):
    def post(self):
        #Step 1: Read the posted data
        postedData = request.get_json()

        #Step 2: Get the elements from poste data
        username = postedData["username"]
        password = postedData["password"]

        #Step 3: Check if the username exists or is new
        username_exists = UsernameExists(username)


        if username_exists == True:
            return( {
                "status" : 301,
                'message' : 'username already exists'
            })
        

        #Step 4: Hash the pass
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    

        #Step 5: add the registration details to the db
        token_amount = 6
        users.insert({
            "username" : username,
            "password" : hashed_pw,
            "tokens" : token_amount
        })

        return({
            'status' : 200,
            'message' : "you have successfully signed up"
        })



def verifyPw(username, password):
    hashed_pw = users.find({
        "username" : username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "username" : username
    })[0]["tokens"]
    return tokens

class Detect(Resource):
    def post(self):
        #Step 1: Get the posted data
        postedData = request.get_json()

        #Step 2: Get the data from posted data
        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        # Step 3: Check if the values exist
        if UsernameExists(username) == False:
            return({
                "status" : 301,
                "msg" : "Invalid Username"
            })

        if not verifyPw(username, password):
            return({
                "status" : 302,
                "msg" : "Invalid Pass"
            })

        if countTokens(username) <=0:
            return({ 
                "status" : 303,
                "msg" : "you are out of tokens. please refill."
            })

        #Step 4: Calculate the similarity
        nlp = spacy.load('en_core_web_sm')
        text1_nlp = nlp(text1)
        text2_nlp = nlp(text2)
        
        ratio = text1_nlp.similarity(text2_nlp)

        #Step 5: Get one token
        current_tokens = countTokens(username)

        users.update({
            "username" : username}, {
                "$set" : {"tokens" : current_tokens - 1}
            }
        )

        return({ 
            "status" : 200,
            "similarity" : ratio,
            "tokens left" : current_tokens - 1,
            "msg" : "The similarity score is successfully created."
        })




class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        refill_amount = postedData["refill"]


        if not UsernameExists(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(retJson)

        correct_pw = "admin_pass"
        if not password == correct_pw:
            retJson = {
                "status":304,
                "msg": "Invalid Admin Password"
            }
            return jsonify(retJson)

        #Deposit Tokens to users account
        users.update({
            "username":username
        }, {
            "$set":{
                "tokens":refill_amount
                }
        })

        return({
            "status":200,
            "msg": "Refilled successfully"
        })




api.add_resource(Register, "/register")
api.add_resource(Detect, "/detect")
api.add_resource(Refill, "/refill")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)   