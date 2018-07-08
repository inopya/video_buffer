# -*- coding: cp1252 -*-

#         _\|/_
#         (O-O)
# -----oOO-(_)-OOo----------------------------------------------------


#######################################################################
# ******************************************************************* #
# *                                                                 * #
# *                   Autor:  Eulogio López Cayuela                 * #
# *                                                                 * #
# *      Clase que simula el retraso en una recepcion de video      * #
# *                                                                 * #
# *            OpenCV    Versión 1.0   Fecha: 04/07/2018            * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# OPENCV
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

import time                 # funciones de tiempo (fechas, horas, pausas...)
import cv2                  # modulo de vision artificial
import numpy                # funciones matematicas avanzadas
import random


class  Video_Signal_Delay():
    '''
    PERMITE SIMULAR UN RETRASO EN LA RECEPCION DE UNA SEÑAL DE VIDEO

    Ejemplo de uso:
    mi_camara = Video_Signal_Delay(camara_id, retraso_video = 10, framerate = 4.0, procesar=True), donde:

     - camara_id :      es un numero entero que representa el numeo de dispositivo 
                        que queremos usar
                        por si hay mas de una camara conectada

     - retraso_video :  tiempo ens egundos que se retrasa la señal
                        Si el retraso es cero, la imagen simplemetne cambia el framerate respecto a la original

     - framerate:       numero de framnes por segundo de la señal en diferido

     - procesar :       si True,  procesa la imagen y la devuelve en gris y de menos resolucion

     - ruido:           si True, se añade ruido aleatoriakmente a la señal de video remota, (solo si es procesada)

    Para interactuar con esta clase disponemos de dos metodos:

     - read()           --> nos devuelve el video en directo en tamaño original

     - video_remoto()   --> nos devuelve el video con un tiempo de retraso (procesado y con ruido si procede)
    '''

    def __init__(self, camara_id, retraso_video = 10, framerate = 4.0, procesar=True, ruido = True):
        self.buffer_size = int(retraso_video*framerate)+ 1              # (nos aseguramos que nunca sea cero)
        self.intervalo_refresco = float(1.0/framerate)                  # periodicidad con que se rerescan los datos del buffer de video
        self.momento_refresco = time.time() + self.intervalo_refresco   # momento en que se debe sacar y añadir informacion al buffer de video
        time.sleep(self.intervalo_refresco)                             # pausa de seguridad para la generacion del buffer
        self.video_buffer = []                                          # definir el buffer como una lista
        self.procesar = procesar                                        # True o False, indicando si se devuelve un fotogrma procesado o en raw

        self.camara = cv2.VideoCapture(camara_id)                       # creamos una instancia de la clase opencv Camara()
        self.FLAG_estado_camara = self.camara.isOpened()
        self.imagen = self.read()                                       # almacenamiento temporal de la captura de la camara para hacer operaciones con ella
      
        # control del ruido
        self.duracion_interferencia = (2,14)                            # tiempo en segundos que puede llegar a durar una interferencia
        self.tiempo_entre_interferencias = (25, 45)                     # periodos de señal sin interferencias (de 25 a 45 segundos)
        self.FLAG_ruido_activo = ruido #* self.procesar                  # solo se aplica si la imagen ha sido procesada
        self.FLAG_aplicar_ruido_ahora = True                            # si FLAG_ruido_activo = True, indica si es momento o no de meter una interferencia

        self.incremento_aleatorio = retraso_video + random.randrange(self.duracion_interferencia[0],self.duracion_interferencia[1])
        self.momento_cambio_bandera = time.time() + self.incremento_aleatorio
        self.nivel_ruido_maximo = 5    

        # hasta superado el retraso la primera vez, la imagen sera borrosa
        self.imagen = cv2.GaussianBlur(self.imagen,(111,111),0)
        for x in range(self.buffer_size):
            self.temp = self.add_noise(self.imagen)  # almacenamiento temporal de la imagen procesada
            if self.procesar:
                self.temp = self.resize(self.gris(self.temp))               #reescalarlo y convertirlo a escala de grises
            else:
                self.temp = self.gris(self.temp)
            # poner mensaje "CONECTANDO..." sobre la imagen:
            cv2.putText(self.temp, "CONECTANDO...",(10,140), cv2.FONT_HERSHEY_PLAIN, 2,(0,0,0),3,cv2.LINE_AA)
            self.video_buffer.append(self.temp)

        
    def read(self):
        # metodo que devuelve video en tiempo real (igual que el original de camara() en openCV)
        _, self.imagen = self.camara.read()
        return self.imagen
    

    def video_remoto(self):
        # metodo que devuelve video con retraso y/o distinto framerate
        if time.time() >= self.momento_refresco:
            self.momento_refresco += self.intervalo_refresco
            self.imagen = self.read()

        if self.FLAG_ruido_activo == True:
            #solo se aplica si la imagen ha sido procesada, es decir, reescalada y convertida a grises
            self.imagen = self.add_noise(self.imagen)   # aplicar ruido a la imagen (si procede) 

            if self.procesar == True:
                self.imagen = self.resize(self.gris(self.imagen))
            self.video_buffer.append(self.imagen)
            self.imagen = self.video_buffer.pop(0)      # Imagen retrasada  actualizada       

        else:
            self.imagen = self.video_buffer[0]          # Imagen retrasada sin actualizar

        return self.imagen


    def add_noise(self, imagen):

        if time.time() > self.momento_cambio_bandera:
            self.FLAG_aplicar_ruido_ahora = not self.FLAG_aplicar_ruido_ahora
            #print ("aplicando ruido: ", self.FLAG_aplicar_ruido_ahora) # >> DEBUG
            if self.FLAG_aplicar_ruido_ahora:
                self.nivel_ruido_maximo = random.randrange(2, 30)
                self.incremento_aleatorio = random.randrange(self.duracion_interferencia[0],self.duracion_interferencia[1])
            else:
                self.incremento_aleatorio = random.randrange(self.tiempo_entre_interferencias[0],self.tiempo_entre_interferencias[1])
            self.momento_cambio_bandera = time.time()+self.incremento_aleatorio

        if self.FLAG_aplicar_ruido_ahora:
            ruido = imagen.copy()
            m = 50
            s = 255
            nivel_ruido = random.randrange(45, 99,4)
            mean = (m,m,m) 
            sigma = (s,s,s)
            ruido = cv2.randn(ruido,mean,sigma)
            mezcla = cv2.addWeighted(imagen,1,ruido,nivel_ruido/100.0,0)
            imagen = mezcla
        return imagen  #devolvemos la imagen con ruido


    def resize(self, imagen):
        try:
            imagen = cv2.resize(imagen, (320,240), interpolation = cv2.INTER_AREA)
        except:
            pass
        return imagen 

    def gris(self, imagen):
        try:
            imagen =  cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        except:
            pass
        return imagen 



    def release(self):
        self.camara.release()
        cv2.destroyAllWindows()



