import cv2
import time
import speech_recognition as sr
import numpy as np
import ctypes

class ImageGenerator:
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

    def run(self):
        # Configura el reconocimiento de voz
        r = sr.Recognizer()
        mic = sr.Microphone()

        # Inicializa la pantalla
        self.initialize_screen()

        # Inicia la escucha continua
        with mic as source:
            print("Escuchando...")

            while True:
                try:
                    # Escucha el audio desde el micrófono
                    audio = r.listen(source)

                    # Utiliza el reconocimiento de voz para obtener el texto
                    text = r.recognize_google(audio, language="es-ES")

                    # Muestra el texto reconocido
                    print("Texto reconocido:", text)

                    # Genera una imagen basada en el texto
                    img = self.generate_image(text)

                    # Muestra la imagen generada
                    self.show_image(img)

                except sr.UnknownValueError:
                    print("No se pudo reconocer el audio")
                except sr.RequestError as e:
                    print("Error en la solicitud de reconocimiento de voz:", str(e))

                # Tiempo de espera entre cada generación de imágenes
                time.sleep(5)


if __name__ == "__main__":
    generator = ImageGenerator()
    generator.run()
