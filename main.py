import cv2
import face_recognition
import json
import numpy as np
from cv2 import WINDOW_AUTOSIZE

# globals
button = [130, 330, 590, 630]


def userExists(name):
    with open('faces.json') as faces:
        faceData = json.load(faces)
        if name in faceData["names"]:
            return True
        else:
            return False


def Face_Data_load(fileName, personName):
    namesList = [personName]
    fileName = f'{fileName}.jpg'
    img = cv2.imread(f"./Images/{fileName}")
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodeList = face_recognition.face_encodings(imgRGB)
    if len(encodeList) != 0:
        if len(encodeList) > 1:
            for i in range(len(encodeList-1)):
                name = input(f"Enter {i}th person Name: ")
                namesList.append(name)
        for i, encode in enumerate(encodeList):
            flattenEncode = list(encode.flatten())
            faceData = {
                "Name": namesList[i],
                "faceEncode": flattenEncode,
                "fileName": fileName
            }
            with open("faces.json", 'r+') as faces:
                images = json.load(faces)
                images['faces'].append(faceData)
                images['names'].append(personName)
                images['fileName'].append(fileName)
                faces.seek(0)
                json.dump(images, faces, indent=4, sort_keys=True)
    return True


def get_encodes():
    encodes = []
    with open('faces.json') as faces:
        faceData = json.load(faces)
        names = faceData['names']
        for i in faceData["faces"]:
            encodes.append(i["faceEncode"])
    return encodes, names


def findFace(img):
    knownEncodes, knownNames = get_encodes()
    names = []
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceLoc = face_recognition.face_locations(imgS)
    encodeFace = face_recognition.face_encodings(imgS, faceLoc)
    for encode, face in zip(encodeFace, faceLoc):
        # matches = face_recognition.compare_faces(knownEncodes, encode)
        faceDis = face_recognition.face_distance(knownEncodes, encode)
        # print(faceDis, knownNames)
        if len(faceDis) != 0:
            y1, x2, y2, x1 = face
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), -1)
            faceDis = list(faceDis)
            print(faceDis)
            if min(faceDis) > 0.5:
                name = None
            else:
                name = knownNames[faceDis.index(min(faceDis))]
            names.append(name)
            print(names)
            cv2.putText(img, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    return names, img  # img


def writeImage(img, name):
    cv2.imwrite(f"./Images/{name}.jpg", img)


def captureImage():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        cv2.namedWindow("Image Capture", WINDOW_AUTOSIZE)
        # cv2.resizeWindow("Image Capture", 480, 640)
        names, img = findFace(img)
        # img[button[0]:button[1], button[2]:button[3]] = 180
        # cv2.putText(img, 'Button', (620, 180), cv2.FONT_HERSHEY_PLAIN, 2, 0, 3)
        cv2.imshow("Image Capture", img)
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == 32:
            writeImage(img)


def captureImageAddData(name):
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgRGB = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
        cv2.rectangle(img, (10, 10), (100, 20), 0, -1)
        cv2.putText(img, "Press 'space' to take a pic", (12, 12),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)
        faceLoc = face_recognition.face_locations(imgRGB)
        if len(faceLoc) != 0:
            for i in faceLoc:
                y1, x2, y2, x1 = i
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), 0, 2)
        cv2.imshow("Image Capture", img)
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == 32:
            writeImage(img, name)
            break


if __name__ == "__main__":
    print("*" * 30, sep='')
    print("1. If You are Here To Upload a New Face Data: \n")
    print("2. If You are Here to looking for SomeOne: \n")
    print("*" * 30, sep='')
    usrChoice = int(input("Enter Your Choice: \n"))
    if usrChoice == 1:
        print("1 .Want To take a picture\n")
        print("2. Already have a picture\n")
        choice = int(input("Enter Choice: \n"))
        if choice == 1:
            name = input("Enter the person's name: ")
            captureImageAddData(name)
            Face_Data_load(f"{name}.jpg", name)
        elif choice == 2:
            name = input("Enter the person's name: ")
            pictureFile = input(
                "Enter File name of Picture (With Extension): ")
            if userExists(name):
                print("Use Already Exists")
            else:
                Face_Data_load(personName=name, fileName=pictureFile)

    elif usrChoice == 2:
        print("1. If having an image of the person.\n")
        print("2. If want to capture an image")
        type = int(input("Enter Your Choice: "))
        if type == 1:
            path = input("Enter the file Path (With Extension): ")
            img = cv2.imread(f"./Images/{path}")
            face = findFace(img)
            cv2.namedWindow("Image")
            cv2.imshow("Image", img)
            cv2.waitKey(0)
        elif type == 2:
            captureImage()
