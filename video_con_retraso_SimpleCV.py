# -*- coding: cp1252 -*-

#         _\|/_
#         (O-O)
# -----oOO-(_)-OOo----------------------------------------------------


#######################################################################
# ******************************************************************* #
# *                                                                 * #
# *                   Autor:  Eulogio López Cayuela                 * #
# *                                                                 * #
# *   Simular el retraso en la recepcion de una señal de video      * #
# *                                                                 * #
# *                  Versión 1.2   Fecha: 10/07/2018                * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################

'''
    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    # SimpleCV
    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

    Ejemplo de uso de la Clase  >> Video_Signal_Delay <<

    PERMITE SIMULAR UN RETRASO EN LA RECEPCION DE UNA SEÑAL DE VIDEO

    Ejemplo de uso:
    mi_camara = Video_Signal_Delay(camara_id, retraso_video = 10, framerate = 4.0, color=False, size=(320,240),ruido=True), donde:

     - camara_id :      es un numero entero que representa el numeo de dispositivo 
                        que queremos usar
                        por si hay mas de una camara conectada

     - retraso_video :  tiempo ens egundos que se retrasa la señal
                        Si el retraso es cero, la imagen simplemetne cambia el framerate respecto a la original

     - framerate:       numero de framnes por segundo de la señal en diferido

     - color :          si False,  procesa la imagen y la devuelve en gris

     - size(x,y) :      si se da una resocucion valida,  procesa la imagen y la devuelve de menos resolucion

     - ruido:           si True, se añade ruido aleatoriakmente a la señal de video remota, (solo si ha sido procesada)


    Para interactuar con esta clase disponemos de dos metodos:

     - getImage()       --> nos devuelve el video en directo en tamaño original

     - video_remoto()   --> nos devuelve el video con un tiempo de retraso (procesado y con ruido si procede)
'''



from Clases_Inopya.VideoBuffer_SimpleCV.Video_Signal_Delay import Video_Signal_Delay
import time






print ">> Modulos de Video cargados"

mensaje = "   creando enlace con el satelite........" 
for letra in mensaje:
    letra +='\r'
    time.sleep(0.05)
    print letra,
print "   \n"



framerate = 8           # numero de fotogramas recibidos por segundo
retraso_video = 7       # retraso deseado en la señal de video en segundos
camara_id = 0           # camara_id  (numero de dispositivo, por si se tienen varis camaras conectadas)


# Definir una instancia a la camara extraplanetaria
webCam =  Video_Signal_Delay(camara_id, retraso_video, framerate, color=False, size=(320,91), ruido=True)


while True:

    # leer un fotograma desde la camara video con retraso 
    # (para dificultar la visualizacion)
    imagen_diferido = webCam.video_remoto()

        
    # video en directo para las funciones 
    # que hagan deteccion de objetos
    imagen_directo = webCam.getImage()

    # DEBUG  mostrar al mismo tiempo la imagen en diferido (Izquierda)
    # y la imagen en directo (Derecha)
    # ****  ojo para la vista dual la imagen en dirteco se ha de reescaalr igual que la retrasada ****
    dual_view = imagen_diferido.sideBySide(imagen_directo.resize(320, 91)) 


    # Mostar la imagen de la camara
    #imagen_diferido.show()     # mostrar solo imagen con retraso
    #imagen_directo.show()      # mostrar solo imagen en directo

    dual_view.show()            # DEBUG mostramos ambas imagenes apra ver la diferencia


