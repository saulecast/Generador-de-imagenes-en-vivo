#intento de descargar imagenes con icrawler (como en mi asistente)

from icrawler.builtin import GoogleImageCrawler
import os

def Fdescargar_imagenes(text_busqueda):
    tema_de_imagenes = text_busqueda
    print("¿Cuántas imágenes quieres sobre el tema?, por favor dí solo el número")
    
    # esto designa donde se van a guardar las imagenes descargadas por la asistente
    google_crawler = GoogleImageCrawler(
        storage={'root_dir': os.getcwd() + '\imagenes descargadas\imagenes de ' + tema_de_imagenes})
    google_crawler.crawl(keyword = tema_de_imagenes, max_num = 1)
    print("imágenes descargadas")
    

Fdescargar_imagenes("un dragón")
