# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 20:42:44 2022

@author: nancy
"""
# Librerias
import socket
import cv2
import pickle
import struct
# Puerto en IP en los que se establece el servidor
HOST = "192.168.0.105"
PORT = 8083
# Creacion de la comunicacion
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')
conn, addr = s.accept()
data = b''
payload_size = struct.calcsize("L")
# Contador para nombrar las imagenes 
cnt=0
# Lectura comntinua hasta que el usuario interrumpa la accion
while True:
    
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]

    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)
        
    # Lectura de la imagen
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data)
    # Se sobreescribe todo el tiempo la imagen con la que se quiere probar el modelo de la red
    cv2.imwrite(r"C:\Users\nancy\Documentos\computo_cognitivo\testing\frame.jpg", frame)
    # Para creacion del dataset
    cv2.imwrite(r"C:\Users\nancy\Documentos\computo_cognitivo\dataset\buenas\frame"+str(cnt)+".jpg", frame)
    # Visualizacion de la imagen guardada en las carpetas
    print(frame.size)
    cnt+=1
    cv2.imshow('frame', frame)
    cv2.waitKey(10)