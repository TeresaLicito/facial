import numpy as np
import cv2
import time
import sys
from PIL import Image
import io
from base_datos import BaseDatos
import matplotlib.pyplot as plt

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def puttext_datadase():
    ret, img = cap.read()
    

bd=BaseDatos()
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
cap = cv2.VideoCapture(2)
num=bd.numRow()[0][0]

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #write text
    cv2.putText(img,"RECONOCIMIENTO FACIAL 1.3",(80,25),cv2.FONT_HERSHEY_SIMPLEX, 1, (124,252,0), 2, cv2.LINE_AA)
 
   

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(124,252,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        cv2.putText(img,"Rostro Detectado", (x,y+250), cv2.FONT_HERSHEY_SIMPLEX, 1, (124,252,0), 2, cv2.LINE_AA)
   
        

        
        sub_face=img[y:y+h,x:x+w]
        if sub_face.any():
            cv2.putText(img,"Conectando con la",(340,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,254), 2, cv2.LINE_AA)
            cv2.putText(img,"Base de Datos",(340,125), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,254), 2, cv2.LINE_AA)
            hora=time.strftime("%H:%M:%S")
            fecha=time.strftime("%d/%m/%y")
            if num==0:
                num=num+1
                name="faces/img"+str(num)+".jpg"
                cv2.imwrite(name,sub_face)
                bd.insertar_imagen(num,name,fecha,hora)
            else:
                for i in range(1,num+1):
                    cv2.imwrite("faces/temp.jpg",sub_face)    
                    original=cv2.imread("faces/img"+str(num)+".jpg")
                    compare=cv2.imread("faces/temp.jpg")
                    original=cv2.resize(original,(300,300))
                    compare=cv2.resize(compare,(300,300))
                    m=mse(original,compare)/100
                    if m<=50:
                        f=bd.buscar(i)[0][2]
                        h=bd.buscar(i)[0][3]
                        print "Se encontro el rostro en la base de datos"
                        print "visto "+str(f)+"  a las "+str(h)
                        cv2.putText(img,"Semejansa al", (10,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (124,252,0), 2, cv2.LINE_AA)
                        cv2.putText(img,str(m)+"%", (10,235), cv2.FONT_HERSHEY_SIMPLEX, 1, (124,252,0), 2, cv2.LINE_AA)
                        
                        cv2.putText(img,"Se encontro el rostro en la", (3,425), cv2.FONT_HERSHEY_SIMPLEX, 1, (254,0,0), 2, cv2.LINE_AA)
                        cv2.putText(img,"Base Datos visto "+str(f), (3,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (254,0,0),2, cv2.LINE_AA)
                        cv2.putText(img,"a las "+str(h), (3,475), cv2.FONT_HERSHEY_SIMPLEX, 1, (254,0,0), 2, cv2.LINE_AA)
                        break
                        #cv2.putText(img,"Rostro en la Base Datos",(345,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (124,252,0), 1, cv2.LINE_AA)
                    else:
                        num=num+1
                        print "no se detectaron rostro"
                        name="faces/img"+str(num)+".jpg"
                        cv2.imwrite(name,sub_face)
                        bd.insertar_imagen(num,name,fecha,hora)

        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
        #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    #title 
    cv2.imshow('FACE 1.3',img)
    
        
                    
        #break;
    
    if cv2.waitKey(1) & 0xff == 27:
        break
   
cap.release()
cv2.destroyAllWindows()
    

"""
bd=BaseDatos()
lista=bd.listar_imagenes()
for data in lista:
    image = Image.open(io.BytesIO(data[1]))
    image2 = Image.fromarray(sub_face, 'RGB')
    plt.savefig("img2.jpg")
    original=cv2.imread("img1.jpg")
    compare=cv2.imread("img2.jpg")
    original=cv2.resize(original,(300,300))
    compare=cv2.resize(compare,(300,300))
    m=mse(original,compare)/100
    if m<=50:
        print 100-m
        print "si"
    else:
        print "no"
        print 100-m
"""
