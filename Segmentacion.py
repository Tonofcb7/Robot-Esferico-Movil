#Universidad Del Valle de Guatemala
#Autor: Antonio José Ixtecoc 
#Carnet: 15582

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from openpyxl import Workbook

# Definición de límites en el espacio HSV para los colores detectados
lower = {'rojo':(166, 84, 141), 'verde':(66, 122, 129), 'azul':(97, 100, 117), 'amarillo':(23, 59, 119),'naranja':(0, 50, 80) } #assign new item lower['blue'] = (93, 10, 0) 'orange':(0, 50, 80)
upper = {'rojo':(186,255,255), 'verde':(86,255,255), 'azul':(117,255,255), 'amarillo':(54,255,255),'naranja':(20,255,255)}  #'orange':(20,255,255)
data={'Coordenada x':(0),'Coordenada y': (0)}

# Definición de colores para dibujar los círculos
colors = {'rojo':(0,0,255), 'verde':(0,255,0), 'azul':(255,0,0), 'amarillo':(0, 255, 217),'naranja':(0,140,255)} #'orange':(0,140,255)

Y_x=[]
Y_y=[]
R_x=[]
R_y=[]
B_x=[]
B_y=[]

#Asignación de Captura de video; Valor "0" si es cámara de compu; Valor "1" si es webcam externa
camera = cv2.VideoCapture(0)
    
wb = Workbook()
ruta = 'salida.xlsx'

hoja = wb.active
hoja.title = "Coordenada x-Coordenada y"

fila = 1 #Fila donde empezamos
col_X = 1 #Columna donde guardamos las fechas
col_Y = 2 #Columna donde guardamos el dato asociados a cada fecha
while True:
    # Frame Actual 
    (grabbed, frame) = camera.read()
    #
#    if args.get("video") and not grabbed:
#        break

   
    # Se redefine el ancho de la imágen, se le aplica una difuminasión de Gauss y se pasa al espacio de color HSV
    frame = imutils.resize(frame, width=600)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #Para cada color, se revisa en la máscara si hay objetos circulares
    for key, value in upper.items():
        
        #Construye una máscara para los colores de las tuplas definidas
        #Se emplea una serie de dilataciones y erosiones para quitar cualquier mancha no deseada en la mascas
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
                
        # Se encuentra los contornos de las imágenes
        # (x, y); centro de la esfera
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
#        
        # Se activa solo si un contorno fue encontrado
        if len(cnts) > 0:
            # se encuentra el contorno más grande, luego se encuentra el mínimo circulo que encierra esos puntos y se encuentra el centroide
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#
            if key == 'naranja':
                for i in range(len(Y_x)): 
                    x1= Y_x[i] 
                    if abs(x1-x)<5:
                        x=x1
                    else:
                        pass
                    
                for i in range(len(Y_y)): 
                    y1= Y_y[i] 
                    if abs(y1-y)<5:
                        y=y1
                    else:
                        pass
                #colocación de los elementos en la lista para filtrado
                hoja.cell(column=col_X, row=fila, value=x)
                hoja.cell(column=col_Y, row=fila, value=y)
                fila+=1
                if x in Y_x:
                    pass
                else:
                    Y_x.append(x)
                
                if y in Y_y:
                    pass
                else:
                    Y_y.append(y)

            if key == 'rojo':
                if x in R_x:
                    pass
                else:
                    R_x.append(x)
                
                if y in R_y:
                    pass
                else:
                    R_y.append(y)
            
            if key == 'azul':
                if x in B_x:
                    pass
                else:
                    B_x.append(x)
                
                if y in B_y:
                    pass
                else:
                    B_y.append(y)
        
            # Radio mínimo de identificación de círculos 
            if radius > 0.5:
                # Dibuja el círculo encontrado y actualiza la lista de centroides
                for i in range(len(Y_x)): 
                    print Y_x[i]
                    print " "
                    print Y_y[i]
#                    hoja.cell(column=col_X, row=fila, value=Y_x[i])
#                    hoja.cell(column=col_Y, row=fila, value=Y_y[i])
#                    fila+=1
                    Y_x.pop(i)
                    Y_y.pop(i)
#                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
 #               cv2.putText(frame,"Agente "+ key, (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)

     
    # Se enseña la imagen procesada
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    # Precionar la letra "q" para salir del programa 
    if key == ord("q"):
        break
 
# Se cierra la conexión con la cámara y finaliza programa 
wb.save(filename = ruta)
camera.release()
cv2.destroyAllWindows()
