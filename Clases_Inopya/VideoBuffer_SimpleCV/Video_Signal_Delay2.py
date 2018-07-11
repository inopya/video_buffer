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
# *          SimpleCV    Versión 1.2   Fecha: 10/07/2018            * #
# *                                                                 * #
# ******************************************************************* #
#######################################################################



#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# SimpleCV
#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

import time
from SimpleCV import Image, Camera, Color, DrawingLayer
import random


class  Video_Signal_Delay():
    '''
    PERMITE SIMULAR UN RETRASO EN LA RECEPCION DE UNA SEÑAL DE VIDEO

    Ejemplo de uso:
    mi_camara = Video_Signal_Delay(camara_id, retraso_video = 10, framerate = 4.0, color=False, size=(320,240), ruido=True), donde:

     - camara_id :      es un numero entero que representa el numeo de dispositivo 
                        que queremos usar
                        por si hay mas de una camara conectada

     - retraso_video :  tiempo ens egundos que se retrasa la señal
                        Si el retraso es cero, la imagen simplemetne cambia el framerate respecto a la original

     - framerate:       numero de framnes por segundo de la señal en diferido

     - color :          si False,  procesa la imagen y la devuelve en gris

     - size(x,y) :      si se da una resocucion valida,  procesa la imagen y la devuelve de menos resolucion

     - ruido:           si True, se añade ruido aleatoriakmente a la señal de video remota, (solo si es procesada)

    Para interactuar con esta clase disponemos de dos metodos:

     - getImage()       --> nos devuelve el video en directo en tamaño original

     - video_remoto()   --> nos devuelve el video con un tiempo de retraso (procesado y con ruido si procede)
    '''

    def __init__(self, camara_id, retraso_video = 10, framerate = 4.0, color=False, size=(320,240), ruido=True):
        self.buffer_size = int(retraso_video*framerate)+ 1              # (nos aseguramos que nunca sea cero)
        self.intervalo_refresco = float(1.0/framerate)                  # periodicidad con que se rerescan los datos del buffer de video
        self.momento_refresco = time.time() + self.intervalo_refresco   # momento en que se debe sacar y añadir informacion al buffer de video
        time.sleep(self.intervalo_refresco)                             # pausa de seguridad para la generacion del buffer
        self.video_buffer = []                                          # contiene los frames equivalentes al tiempo de retraso
        self.imagen = None                                              # almacenamiento temporal de la captura de la camara para hacer operaciones con ella
        self.camara = Camera(camara_id)                                 # creamos una instancia de la clase opencv Camara()
        self.Flag_color = color                                         # si False,  procesa la imagen y la devuelve en gris        
        self.Flag_resize = False                                        # se pone a True si le pasamos una resolucion valida,  para pemitir el reescalado
        self.size = size                                                # si es una resocucion valida reescala la imagen
        if size[0]>0 and size[1]>0:
            self.Flag_resize = True
        
        # control del ruido
        self.duracion_interferencia = (2,14)                            # tiempo en segundos que puede llegar a durar una interferencia
        self.tiempo_entre_interferencias = (25, 45)                     # periodos de señal sin interferencias (de 25 a 45 segundos)
        self.FLAG_ruido_activo = ruido                                  # Si True se activan las interferencias en momentos aleatorios
        self.FLAG_aplicar_ruido_ahora = True                            # si FLAG_ruido_activo = True, indica si es momento o no de meter una interferencia
        if self.Flag_color == False:
            self.video_ruido = [self.resize(self.gris(Image("Clases_Inopya/VideoBuffer_SimpleCV/c_ruido%d.png" %x))) for x in range(5)]    # cargamos la lista de fotogramas correspondientes al ruido
        else:
            self.video_ruido = [self.resize(Image("Clases_Inopya/VideoBuffer_SimpleCV/c_ruido%d.png" %x)) for x in range(5)]  # cargamos la lista de fotogramas correspondientes al ruido

        self.frame_ruido_index = 0                                      # fotograma del ruido que se mostrará
        self.incremento_aleatorio = retraso_video + random.randrange(self.duracion_interferencia[0],self.duracion_interferencia[1])
        self.momento_cambio_bandera = time.time() + self.incremento_aleatorio
        self.nivel_ruido_maximo = 10                                     # intensidad con que se mostrará la interferencia

        #creacion y llenado inicial del buffer de video
        self.video_buffer = []                                          # definir el buffer como una lista
        self.imagen = self.getImage()                                   # capturar un fotograma desde la camara
        self.imagen = self.resize(self.gris(self.imagen))               # reescalarlo y convertirlo a escala de grises
        self.imagen = self.imagen.blur(45,45)                           # hasta superado el retraso, la imagen sera borrosa

        # esto no funciona :(   No se lleva bien con el ruido              
        textLayer = DrawingLayer((self.imagen.width, self.imagen.height))   # crear una capa vacia para escribir texto
        textLayer.text("CONECTANDO...", (40, 70), color=Color.RED)      # poner mensaje "CONECTANDO..." sobre la imagen:
        self.imagen.addDrawingLayer(textLayer)                          # fusionar la capa de imagen y al de texto
        self.video_buffer = [self.imagen for x in range(self.buffer_size)]  # llenar el buffer de video con una imagen estatica"

        
    def getImage(self):
        # metodo que devuelve video en tiempo real (igual que el original de camara() en openCV)
        return self.camara.getImage()


    def video_remoto(self):
        # metodo que devuelve video con retraso y/o distinto framerate
        if time.time() >= self.momento_refresco:
            self.momento_refresco += self.intervalo_refresco
            self.imagen = self.getImage()
            if self.Flag_color == False:
                self.imagen = self.gris(self.imagen)
            if self.Flag_resize == True:
                self.imagen = self.resize(self.imagen)       
            self.video_buffer.append(self.imagen)
            self.imagen = self.video_buffer.pop(0)      # Imagen retrasada  actualizada       

        else:
            self.imagen = self.video_buffer[0]          # Imagen retrasada sin actualizar

        if self.FLAG_ruido_activo == True:
            #solo se aplica si la imagen ha sido procesada, es decir, reescalada y convertida a grises
            self.imagen = self.add_noise(self.imagen)   # aplicar ruido a la imagen (si procede) 

        return self.imagen


    def add_noise(self, imagen):
        # aplicar ruido a la imagen (sobre imagenes en blanco y negro)
        self.frame_ruido_index+=1
        if self.frame_ruido_index >= len(self.video_ruido):
            self.frame_ruido_index = 0

        if time.time() > self.momento_cambio_bandera:
            self.FLAG_aplicar_ruido_ahora = not self.FLAG_aplicar_ruido_ahora
            #print "aplicando ruido: ", self.FLAG_aplicar_ruido_ahora # >> DEBUG
            if self.FLAG_aplicar_ruido_ahora:
                if self.Flag_color == False: 
                    self.nivel_ruido_maximo = random.randrange(2, 30)
                else:
                    self.nivel_ruido_maximo = random.randrange(20, 40)
                self.incremento_aleatorio = random.randrange(self.duracion_interferencia[0],self.duracion_interferencia[1])
            else:
                self.incremento_aleatorio = random.randrange(self.tiempo_entre_interferencias[0],self.tiempo_entre_interferencias[1])
            self.momento_cambio_bandera = time.time()+self.incremento_aleatorio

        if self.FLAG_aplicar_ruido_ahora:
            imagen += self.video_ruido[self.frame_ruido_index]*((random.randrange(1, self.nivel_ruido_maximo))/10.0)
        return imagen  #devolvemos la imagen con ruido


    def resize(self, imagen):
        # metodo interno para procesar el video retrasado y hacerlo mas liviano
        imagen = imagen.resize(self.size[0], self.size[1])
        return imagen 


    def gris(self, imagen):
        # metodo interno para procesar el video retrasado y hacerlo mas liviano
        imagen =  imagen.grayscale()
        return imagen 

