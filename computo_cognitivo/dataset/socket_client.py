# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 20:42:44 2022 2022

@author: nancy
"""
# Librerias
import cv2
import numpy as np
import socket
import pickle
import struct
# Captura de imagen con camara Raspberry pi
vc = cv2.VideoCapture(0)
# Creacion del cliente
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Comunicacion: tipo de archivo que manda informacion
clientsocket.connect(('192.168.0.105', 8083))

# Procesamiento de imagen una vez establecida la comunicacion
while True:
    # Lectura de la camara identificada
    next, frame = vc.read()
    # Flip de camara tipo espejo
    frame = np.flip(frame, axis=1)
    # Procesamiento a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_BGR = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    # Muestra al usuario lo que esta visualizando la camara
    cv2.imshow("Original", gray_BGR)
    # Deteccion de Circulos
    rows = gray.shape[0]
    # Obtencion de las coordenadas de los circulos con la funcion de OpenCV
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,dp = 1,minDist = rows/8,param1=80,param2=30,minRadius=25,maxRadius=40)
    # Si detecta circulos con las caracterizticas anteriores
    if circles is not None:
        # variable en la que se guarda lo que se detecta como circulo
        circles = np.uint16(np.around(circles))
        # Variables que se ocupan para dibujar visualmente circulos en el area de deteccion
        print(circles)
        radius_center = 1
        thickness_center = 3
        thickness_outline = 3
        # Se establece centro y radio para geometricamente entrar el area de interes
        for i in circles[0,:]:
            center = (i[0],i[1])
            radius_outline = i[2]
            #Dibujamos el centro del circulo
            #cv2.circle(gray_BGR,center,radius_center,(0,255,0),thickness_center) #center
            radius_outline = i[2]
            #cv2.circle(gray_BGR,center,radius_outline,(0,0,255),thickness_outline) #contour
            #cv2.putText(gray_BGR, 'hola', (int(10),int(50)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
            cv2.imshow("HoughCircles", gray_BGR)
            # Para identificar el area de interes (roi) al rededor de los circulos
            x,y,w,h = (center[0]-radius_outline-10,center[1]-radius_outline-10,radius_outline*2+20,radius_outline*2+20)
            margen = 2
            yu, yd = y-margen , y+h+margen
            xu, xd = x-margen , x+w+margen
            # Corta la imagen original para reducirla a la roi
            roi = gray_BGR[yu : yd , xu : xd]
            # muestra la imagen que manda por la comunicacion a la otra compu
            cv2.imshow("Cropped", roi)
            # Envia la imagen a la otra compu
            data = pickle.dumps(roi)
            clientsocket.sendall(struct.pack("L", len(data)) + data)
    if cv2.waitKey(50) >= 0:
        cv2.destroyAllWindows()
        break