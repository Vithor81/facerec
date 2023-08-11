import cv2
import os
import face_recognition
import pickle

folderPath = "C:\\imagens"
imgsPath = os.listdir(folderPath)
imgsList = []
morIds =[]
for path in imgsPath:
    imgsList.append(cv2.imread(os.path.join(folderPath, path)))
    morIds.append(os.path.splitext(path)[0])


def findEncodings(imgsList):
    encodeList = []
    for img in imgsList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("enconding start....")
encondeListKnown = findEncodings(imgsList)
encondeListKnownWithIds = [encondeListKnown, morIds]
print ("encoding complete")
folder = "C:\\codes"
if(not os.path.exists(folder)):
    os.mkdir(folder)
file = open("C:\\codes\\encodefile.p", 'wb')
pickle.dump(encondeListKnownWithIds, file)
file.close()
print("file")