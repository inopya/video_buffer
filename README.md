# video_buffer
Simula el retraso en la recepcion de una señal de video

    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
    # OpenCV y simpleCV
    #mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

    Ejemplo de uso de la Clase  >> Video_Signal_Delay <<

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
     - ruido:           si True, se añade ruido aleatoriakmente a la señal de video remota
                        SIMPLECV solo añade ruido si la imagen es procesada  (reescalada y convertida a grises)
                        en OPENCV el ruido puede añadirse a las imagenes en color y sin reescalar

    Para interactuar con esta clase disponemos de dos metodos:
     - raw()            --> OPENCV, nos devuelve el video en directo en tamaño original (solo el video)
     - read()           --> OPENCV, nos devuelve el 'ret' y el video en directo en tamaño original
     - getimage()       --> SIMPLECV,  nos devuelve el video en directo en tamaño original
     - video_remoto()   --> COMUN, nos devuelve el video con un tiempo de retraso (procesado y con ruido si procede)
