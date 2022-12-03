# Pruebas
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import  Adamax

alfa = 0.0004 #learning rate

modelo = load_model('modeloCNNreto.h5')
print(modelo.summary())
modelo.compile(loss='categorical_crossentropy', optimizer=Adamax(learning_rate=alfa), metrics=['accuracy'])

test_path = "C:\Users\nancy\Documents\computo_cognitivo\testing\test" #FROM SOCKET
while True:
    #print("reading...")
    
    file_name = "frame.jpg"
    
    image_path = test_path + "/" + file_name
    image = cv2.imread(image_path)
    
    if image is None:
        continue
    
    image = cv2.resize(image,(80,80))
    image = np.reshape(image,[1,80,80,3])

    classes = modelo.predict(image)
    print(classes)
    if np.argmax(classes) == 0:
        print("DADO EN BUEN ESTADO")
    else:
        print("¡¡ DADO EN MAL ESTADO !!")
        
    os.remove(image_path)