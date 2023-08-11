import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
from datetime import datetime
import time
import pymssql
conn = pymssql.connect("10.68.45.38", "sa", "Senac123", "BancoGestao")
cursor = conn.cursor(as_dict=True)


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

bG = cv2.imread('Resources/backgraund1ziz.png')

folderModePath = 'Resources/modes'
modePath = os.listdir(folderModePath)
imgModeList = []
for path in modePath:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))


#load do reconhecimento
file = open("C:\\codes\\encodefile.p", 'rb')
encondeListKnownWithIds = pickle.load(file)
file.close()
encondeListKnown, morIds = encondeListKnownWithIds

validar = 0

start_time = time.time()

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

   
    bG[120:120 + 480, 67:67 + 640] = img
    bG[65:65 + 619, 760:760 + 498] = imgModeList[0]
    
  
    validar = 0
    
    for encoFace, faceloc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encondeListKnown, encoFace)
        faceDist = face_recognition.face_distance(encondeListKnown, encoFace)
        
        matchIndex = np.argmin(faceDist)
        
        
       

        if matches[matchIndex]:
            #mode = 1
            bG[65:65 + 619, 760:760 + 498] = imgModeList[1]
            end_time = time.time()
            print("Rosto Conhecido as")
            #  print(hoje)
            # print(morIds[matchIndex])
            codigo = morIds[matchIndex]
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 67 + x1, 120+y1, x2-x1, y2-y1
            bG = cvzone.cornerRect(bG, bbox, rt=0)
            slc = cursor.execute("""Select * from tab_morador WHERE id_morador = %d""",codigo)
            for row in cursor:
                         name = ("%s" % (row['nome_social']))
                         ap = ("%i" % (row['num_apt']))

            
            cv2.putText(bG,str(name),(886,507),
                        cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,0),2)
            cv2.putText(bG,str("APARTAMENTO: " + ap),(860,560),
                        cv2.FONT_HERSHEY_TRIPLEX,1,(8,8,8),2)
           
            if validar == 0:
                elapsed_time = end_time - start_time
                print(elapsed_time)
                
                
                if elapsed_time > 5:
                    print('bd')               
                    cursor.execute("""INSERT INTO Recognition2 (reco, id_morador) VALUES ( getdate(), %s)""",codigo)
                    conn.commit()
                                        
                start_time = time.time()
            
            validar = 1
            

        else:
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 67 + x1, 120+y1, x2-x1, y2-y1
            bG = cvzone.cornerRect(bG, bbox, rt=0)
            bG[65:65 + 619, 760:760 + 498] = imgModeList[2]
            # print("Não reconhecido")
            validar = 0
            

   
  
    cv2.imshow("face", bG)
    cv2.waitKey(1)