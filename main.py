import cv2
import time
import speech_recognition as sr
import numpy as np
import ctypes
from icrawler.builtin import GoogleImageCrawler
import os
from PIL import Image

class ImageGeneratorCV:
    def __init__(self):
        self.screen_width = None
        self.screen_height = None

    def initialize_screen(self):
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)

    def generate_image(self, text):
        # Ajusta el tamaño de la imagen al tamaño completo de la pantalla
        image_width = self.screen_width
        image_height = self.screen_height

        # Crea una imagen en blanco
        img = np.zeros((image_height, image_width, 3), np.uint8)

        # Configura la fuente y el tamaño del texto
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        line_thickness = 2

        # Divide el texto en palabras
        words = text.split()

        # Variables para realizar el salto de línea
        max_line_width = int(image_width * 0.9)
        current_line_width = 0
        current_line = ""
        line_height = 50

        # Recorre las palabras y las agrega al texto de la imagen con salto de línea
        for word in words:
            # Obtiene el tamaño del texto actual
            (word_width, _), _ = cv2.getTextSize(word, font, font_scale, line_thickness)

            # Verifica si el texto actual excede el ancho máximo de línea
            if current_line_width + word_width > max_line_width:
                # Agrega el texto actual a la imagen y reinicia la línea
                img = cv2.putText(img, current_line, (50, line_height), font, font_scale, (255, 255, 255), line_thickness)
                current_line = ""
                current_line_width = 0

                # Incrementa la posición vertical para el siguiente salto de línea
                line_height += 50

            # Agrega la palabra al texto de la línea actual
            current_line += word + " "
            current_line_width += word_width + 20

        # Agrega el texto final a la imagen
        img = cv2.putText(img, current_line, (50, line_height), font, font_scale, (255, 255, 255), line_thickness)

        return img

    def show_image(self, img):
        cv2.imshow("Generated Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class ImageDownloader():
    def __init__(self):
        pass

    def Fdescargar_imagenes(self, text_busqueda):
        tema_de_imagenes = text_busqueda
        print("¿Cuántas imágenes quieres sobre el tema?, por favor dí solo el número")
        
        # esto designa donde se van a guardar las imagenes descargadas por la asistente
        google_crawler = GoogleImageCrawler(
            storage={'root_dir': os.getcwd() + '\imagenes descargadas\imagenes de ' + tema_de_imagenes})
        google_crawler.crawl(keyword = tema_de_imagenes, max_num = 1)
        print("imágenes descargadas")
    

class Escucha():
    def __init__(self) -> None:
        # Configura el reconocimiento de voz
        self.broca = sr.Recognizer()
        self.mic = sr.Microphone()

    #Su capacidad para escuchar es esta función
    def escuchar(self):    
        with self.mic as oido:

            while True:
                print("Escuchando...")
                try:
                    # Escucha el audio desde el micrófono
                    audio = self.broca.listen(oido, phrase_time_limit= 10, timeout = 10)

                    # Utiliza el reconocimiento de voz para obtener el texto
                    print("Procesando...")
                    text = self.broca.recognize_google(audio, language="es-ES")

                    # Muestra el texto reconocido
                    print("Texto reconocido:", text)

                    if crear == True:
                        # Genera una imagen basada en el texto
                        img = generator.generate_image(text)

                        # Muestra la imagen generada
                        generator.show_image(img)
                    else: 
                        #descarga la imagen
                        ImageDownloader().Fdescargar_imagenes(text)

                        # Muestra la imagen descargada
                        try:
                            im = Image.open(os.getcwd() + '\imagenes descargadas\imagenes de ' + text +"/000001.jpg")
                        except Exception as ex:
                            print("No se pudo mostrar la imagen. Error:\n" + ex)
                        
                        im.show()
                        print("imagen mostrada")

                except sr.UnknownValueError:
                    print("No se pudo reconocer el audio")
                except sr.RequestError as e:
                    print("Error en la solicitud de reconocimiento de voz:", str(e))

                # Tiempo de espera entre cada generación de imágenes
                print("esperando")
                time.sleep(5)
                print("reanudando")


    def oir_pasivamente(self):
        with self.mic as oido:
            print("Oyendo...")
            # audio = self.broca.listen(oido)
            audio = self.broca.record(oido, duration = 5)  # Graba el audio sin analizarlo y se detiene cada 5 segundos
            print("Procesando datos...") # Solo avisa de la pausa para analizar datos
            palabra = ""
            try:
                palabra = self.broca.recognize_google(audio, language = "es-ES")
            except sr.UnknownValueError:
                print("no entiende el audio")
            except sr.RequestError as ex:
                print("Request error (problemas al conectarme): "+ str(ex) )
            except RuntimeError:
                print( "RuntimeError: Demasiado tiempo escuchando")
            except ConnectionResetError as ex:
                print("ConnectionResetError (el host remoto a detenido tu conexión): "+ str (ex) ) 
        print(palabra)
        return palabra

    def calibrar_para_ruido_ambiental(self):
        with self.mic as oido:              
            self.broca.adjust_for_ambient_noise(oido)         # escucha por 1 segundo para calcular los limites energeticos (energy threshold) del ruido ambiental... Esta linea es lo que realmente importa de esta función
            print("Mi oido se ha adaptado al ruido ambiental, para comprobarlo puedes decirme una oración compleja")
            
            print("escuchando...")
            audio = self.broca.listen(oido)                   # ahora escuchamos audio para probar que se ha calibrado

        try:
            print("Dijiste " + self.broca.recognize(audio))
            
        except LookupError:                            # el audio es ininteligible
            print("No entendí el audio")
            


if __name__ == "__main__":
    generator = ImageGeneratorCV()


    crear = False #si esto está en true creará una imagen con texto usando open cv, en otro caso descargará las imagenes de google 
    def run():
        
        if crear == True:
            # Inicializa la pantalla
            generator.initialize_screen()

        Escucha().escuchar()


    run()

    # imagen = cv2.imread(os.getcwd() + '\imagenes descargadas\imagenes de ' + "un dragón/000001.jpg") 
    # cv2.imshow('Logo OpenCV', imagen)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # from skimage import io
    # import matplotlib.pyplot  as plt


    # image=io.imread(os.getcwd() + '\imagenes descargadas\imagenes de ' + "un dragón/000001.jpg")/255.0 # imread lee las imagenes con los pixeles codificados como enteros 
    # # en el rango 0-255. Por eso la convertimos a flotante y en el rango 0-1

    # print("- Dimensiones de la imagen:")
    # print(image.shape)
    # plt.imshow(image,vmin=0,vmax=1)

    
