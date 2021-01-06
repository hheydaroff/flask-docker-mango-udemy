"""
Title: Database as a Service

Ideas: 
-Registration of a user with 0 tokens
-Each user gets 10 tokens
-Store a sentence on the DB for 1 token
-Retrieve his stored sentence on the database for 1 token
"""



from flask import Flask
from flask import request, jsonify

from flask_restful import Api, Resource

from pymongo import MongoClient

import bcrypt



app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017") #the path should be exactly as it is in docker-compose.yaml service name
db = client.SentencesDatabase
users = db["Users"] # Sentences will be a document within the collection of Users


class Register(Resource):
    def post(self):
        #Step 1: get posted data by the user
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]


        #Step 2: Hash the pass
        hashed_pass = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


        #Step 3: Store the username and pass into DB
        tokens = 6
        users.insert({
            "username" : username,
            "password" : hashed_pass,
            "sentence" : " ",
            "tokens" : tokens
        })

        retJson = {
            "status" : 200,
            "message" : f"You have successfully registered for the API with the username {username} and you have {tokens} tokens"
        }
        return retJson




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


class Store(Resource):
    def post(self):
        #Step 1: Get the posted data
        postedData = request.get_json()


        #Step 2: Read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Step 3: Verify username pass match
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status" : 302,
                "message" : "wrong login credentials"
            }

            return retJson

        #Step 4: Verify user has enough tokens
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            retJson = { 
                "status" : 301,
                "message" : "You are out of tokens"
            }
            return retJson


        #Step 5: Store the sentence
        users.update({
            "username" : username
            },
            {
                "$set":{
                    "sentence" : sentence,
                    "tokens" : num_tokens - 1
                }
            })
        
        retJson = {
            "status" : 200,
            "message" : "Your sentence is successfully saved"
        }

        return retJson


class Retrieve(Resource):
    def post(self):
        #Step 1: Get the posted data
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]


        #Step 2: Verify username pass match
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status" : 302,
                "message" : "wrong login credentials"
            }

            return retJson


        #Step 3: Verify user has enough tokens
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            retJson = { 
                "status" : 301,
                "message" : "You are out of tokens"
            }
            return retJson


        #Step 4: Give user the sentence
        sentence = users.find({
            "username" : username,
        })[0]["sentence"]

        #also take one token off
        users.update({
            "username" : username
            },
            {"$set": {
                "tokens" : num_tokens - 1
            }
        )

        retJson = { 
            "status" : 200,
            "sentence" : sentence,
            "message": f"You have successfully retrieved your sentence. We took a token off from you, now you have left {num_tokens-1} tokens."
        }

        return retJson




api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Retrieve, "/retrieve")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)  