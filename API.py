from flask import Flask, jsonify, request
from main import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return "<p>hello World!</p>"


@app.route('/find_person', methods=['GET', 'POST'])
def find():
    return "<p>Find Screen</p>"


@app.route('/find_person/Upload_pic', methods=['GET', 'POST'])
def find_upload():
    return "<p>Find Screen, upload screen</p>"


@app.route('/add_person', methods=['GET', 'POST'])
def add():
    return "<p>Add Screen</p>"


@app.route('/add_person/Upload_pic', methods=['GET', 'POST'])
def add_upload():
    return "<p>Add Screen, upload screen</p>"


@app.route('/find_person/Upload_pic/<string:filename>', methods=['GET', 'POST'])
def Find_person_Uploaded_pic(filename):
    img = cv2.imread(f"./Images/{filename}.jpg")
    names, img = findFace(img)
    returnData = {
        "count": len(names),
        "knownPeople": len(names) - (names.count(None)),
        "people": []
    }
    for name in names:
        if name == None:
            returnData['people'].append(
                {
                    "flag": False,
                    "details": "Not Found"
                })
        else:
            returnData["people"].append(
                {
                    "flag": True,
                    "name": name
                })
    return jsonify(returnData)


@app.route('/add_person/Upload_pic/<string:name>/<string:filename>', methods=['GET', 'POST'])
def add_person_Upload_pic(filename, name):
    filename = f"./Images/{filename}.jpg"
    if userExists(name):
        return jsonify({
            "flag": False,
        })
    else:
        flag = Face_Data_load(
            personName=name, fileName=filename)
        return jsonify({
            "flag": flag
        })


if __name__ == '__main__':
    app.run(debug=True)


# http: // 127.0.0.1: 5000/
# http: // 127.0.0.1: 5000/find_person
# http: // 127.0.0.1: 5000/find_person/Upload_pic
# http: // 127.0.0.1: 5000/find_person/Upload_pic/<string:fileName>
# http: // 127.0.0.1: 5000/add_person
# http: // 127.0.0.1: 5000/add_person/Upload_pic
# http: // 127.0.0.1: 5000/add_person/Upload_pic/<string:name>/<string:filename>
