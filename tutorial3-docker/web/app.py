from flask import Flask
from flask import request, jsonify

from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def checkPostedData(postedData, functionName):
    if functionName in ["add", "subtract", "multiply"]: 
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200

    if (functionName in ["divide"]): 
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif  int(postedData["y"]) == 0:
            return 302
        else:
            return 200




class Add(Resource):
    def post(self):
        #If I am here, then the resource Add as requested using the method POST

        #STEP 1: Get posted data
        postedData = request.get_json()

        #STEP 1b: Verify the validity of the posted data
        status_code = checkPostedData(postedData, "add")

        if status_code != 200:
            retJson = {
                "Message": "Missing Data. Check the body again.",
                "Status Code" : status_code
            }
            return retJson


        x = postedData["x"]
        y = postedData["y"]

        #STEP 2: Do the processing
        added  = int(x) + int(y)

        #STEP 3: Return the output in JSON
        addedMap = {
            "Message":added,
            "Status Code" : 200
        }

        return addedMap

    def get(self):
        # This will do a get request on the Resource Add.
        pass

class Subtract(Resource):
    def post(self):
        #If I am here, then the resource subtract as requested using the method POST

        #STEP 1: Get posted data
        postedData = request.get_json()

        #STEP 1b: Verify the validity of the posted data
        status_code = checkPostedData(postedData, "subtract")

        if status_code != 200:
            retJson = {
                "Message": "Missing Data. Check the body again.",
                "Status Code" : status_code
            }
            return retJson


        x = postedData["x"]
        y = postedData["y"]

        #STEP 2: Do the processing
        subtracted  = int(x) - int(y)

        #STEP 3: Return the output in JSON
        subtractedMap = {
            "Message":subtracted,
            "Status Code" : 200
        }

        return subtractedMap

    def get(self):
        # This will do a get request on the Resource Add.
        pass

class Multiply(Resource):
    def post(self):
        #If I am here, then the resource multiply as requested using the method POST

        #STEP 1: Get posted data
        postedData = request.get_json()

        #STEP 1b: Verify the validity of the posted data
        status_code = checkPostedData(postedData, "multiply")

        if status_code != 200:
            retJson = {
                "Message": "Missing Data. Check the body again.",
                "Status Code" : status_code
            }
            return retJson


        x = postedData["x"]
        y = postedData["y"]

        #STEP 2: Do the processing
        multiplied  = int(x) * int(y)

        #STEP 3: Return the output in JSON
        multipliedMap = {
            "Message":multiplied,
            "Status Code" : 200
        }

        return multipliedMap

    def get(self):
        # This will do a get request on the Resource Add.
        pass

class Divide(Resource):
    def post(self):
        #If I am here, then the resource Divide as requested using the method POST

        #STEP 1: Get posted data
        postedData = request.get_json()

        #STEP 1b: Verify the validity of the posted data
        status_code = checkPostedData(postedData, "divide")

        if status_code != 200:
            retJson = {
                "Message": "Error happened. Check the body again.",
                "Status Code" : status_code
            }
            return retJson


        x = postedData["x"]
        y = postedData["y"]

        #STEP 2: Do the processing
        divided  = int(x) / int(y)

        #STEP 3: Return the output in JSON
        dividedMap = {
            "Message":divided,
            "Status Code" : 200
        }

        return dividedMap

    def get(self):
        # This will do a get request on the Resource Add.
        pass



api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)  