import face_recognition as fr
import cv2
from sklearn import svm
import json
import pyttsx3



def addFace(imgArray, name):
    encodes, name = [], name
    for person in imgArray:
        faceLoc = fr.face_locations(person)
        if len(faceLoc) == 1:
            faceEnc = fr.face_encodings(person)[0]
            encodes.append(list(faceEnc.flatten()))
    return encodes, name

def addFaceData(encodes, name):
    global newFaceAdded
    
    with open("faceEncodes.json", 'r+') as f:
        faceData = json.load(f)
        faceData['faces'].append({'name': name, 'faceEncodes': encodes})
        faceData['names'].append(name)
        f.seek(0)
        json.dump(faceData, f, indent=4)
    newFaceAdded = True

def captureImageTrain(name):
    cap = cv2.VideoCapture(0)
    imgArray = []
    while True:
        _, img = cap.read()
        if _:
            cv2.imshow("Train Image Capture", img)
            k = cv2.waitKey(1)
            if k == 27:
                break
            elif k == 32:
                imgArray.append(img)
    print(len(imgArray), imgArray[0].shape)
    encodes, name = addFace(imgArray, name)
    addFaceData(encodes, name)

def getEncodes():
    names, encodes = [], []
    with open('./faceEncodes.json', 'r') as f:
        faceData = json.load(f)
    for i in faceData['faces']:
        for j in i['faceEncodes']:
            encodes.append(j)
            names.append(i['name'])
    return names, encodes

def getEncodesReTrainModel():
    global clf
    names, encodes = [], []
    with open('./faceEncodes.json', 'r') as f:
        faceData = json.load(f)
    for i in faceData['faces']:
        for j in i['faceEncodes']:
            encodes.append(j)
            names.append(i['name'])
    clf = svm.SVC(gamma='scale')
    clf.fit(encodes, names)


def findFace(img):

    global newFaceAdded, clf

    if newFaceAdded or clf == None:
        getEncodesReTrainModel()
        newFaceAdded = False
    faceLoc = fr.face_locations(img)
    facesPresent = []
    for i in range(len(faceLoc)):
        enc = fr.face_encodings(img)[i]
        name = clf.predict([enc])
        facesPresent.append(name[0])
    return facesPresent

def speechOutput(names):
    greet = "Welcome to the Artificial Intelligence and Machine Learning Lab"
    for name in names:
        engine.say(greet + name)
        engine.runAndWait()

def findFaceCam():
    global detectionStack


    cap = cv2.VideoCapture(0)
    frameCount = 1
    while True:
        _, img = cap.read()
        if _:
            faces = findFace(img)
            names = []
            for i in faces:
                if i in detectionStack:
                    continue
                else:
                    names.append(i)
                    detectionStack.append(i)
            # print(detectionStack, names)
            speechOutput(names)
        if frameCount == 150:
            detectionStack = []
        frameCount += 1

if __name__ == "__main__":
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    # Global Variables
    clf = None
    detectionStack = []
    newFaceAdded = False

    findFaceCam()
    
            



