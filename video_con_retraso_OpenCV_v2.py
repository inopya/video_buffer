# -*- coding: cp1252 -*-

#         _\|/_
#         (O-O)
# -----oOO-(_)-OOo----------------------------------------------------


#######################################################################
# ******************************************************************* #
# *                                                                 * #
# *                   Autor:  Eulogio L�pez Cayuela                 * #
# *                                                                 * #
# *   Simular el retraso en la recepcion de una se�al de video      * #
# *                                                                 * #
# *                  Versi�n 1.1   Fecha: 10/07/2018                * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################

'''
    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    # OpenCV
    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

    Ejemplo de uso de la Clase  >> Video_Signal_Delay <<

    PERMITE SIMULAR UN RETRASO EN LA RECEPCION DE UNA SE�AL DE VIDEO

    Ejemplo de uso:
    mi_camara = Video_Signal_Delay(camara_id, retraso_video = 10, framerate = 4.0, color=False, size=(320,240), ruido=True), donde:

     - camara_id :      es un numero entero que representa el numeo de dispositivo 
                        que queremos usar
                        por si hay mas de una camara conectada

     - retraso_video :  tiempo ens egundos que se retrasa la se�al
                        Si el retraso es cero, la imagen simplemetne cambia el framerate respecto a la original

     - framerate:       numero de framnes por segundo de la se�al en diferido

     - color :          si False,  procesa la imagen y la devuelve en gris

     - size(x,y) :      si se da una resocucion valida,  procesa la imagen y la devuelve de menos resolucion

     - ruido:           si True, se a�ade ruido aleatoriakmente a la se�al de video remota


    Para interactuar con esta clase disponemos de dos metodos:

     - raw()            --> nos devuelve el video en directo en tama�o original (solo el video)
     
     - read()           --> nos devuelve el video en directo en tama�o original y el 'ret' como lo hace la clase origial de openCV
     
     - video_remoto()   --> nos devuelve el video con un tiempo de retraso (procesado y con ruido si procede)
'''




import time                 # funciones de tiempo (fechas, horas, pausas...)
from Clases_Inopya.VideoBuffer_OpenCV.Video_Signal_Delay2 import Video_Signal_Delay

import cv2



framerate = 10          # numero de fotogramas recibidos por segundo
retraso_video = 8       # retraso deseado en la se�al de video en segundos
camara_id = 0           # camara_id  0numero de dispositivo, por si se tienen varis camaras conectadas


# Definir una instancia a la camara extraplanetaria
webCam =  Video_Signal_Delay(camara_id, retraso_video, framerate, color=True, size=(320,240), ruido=True)



# Consultamos el estado de la camara
if webCam.FLAG_estado_camara:
    print (">> Modulos de Video cargados")
    mensaje = "   creando enlace con el satelite........" 
    for letra in mensaje:
        time.sleep(0.03)
        print (letra,end="")
    print("\n")

    
while webCam.FLAG_estado_camara:

    # leer un fotograma desde la camara video con retraso 
    # (para dificultar la visualizacion)
    imagen_diferido = webCam.video_remoto()
    cv2.imshow("CONEXION MARTE", imagen_diferido)
        
    # video en directo para las funciones 
    # que hagan deteccion de objetos
    imagen_directo = webCam.raw()
    cv2.imshow("TIEMPO REAL", imagen_directo)


    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27 or tecla == ord('q'):
        webCam.release()
        break 

