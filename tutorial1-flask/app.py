from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return ("Hello, World!")




@app.route('/add_two_nums', methods = ['POST'])
def add_two_nums():
    #get the data
    data_json = request.get_json()
    
    #calculate the sum
    x = data_json['x']
    y = data_json['y']

    z = int(x) + int(y)

    #turn to json
    result_json = {
        "sum" : z
    }
    #return jsonify(json)
    return jsonify(result_json)


if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000, debug = True)  