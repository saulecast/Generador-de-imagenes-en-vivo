from google_images_download import google_images_download
from PIL import Image

def descargar_imagen_google(query):
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords": query, "limit":4}
    paths = response.download(arguments)
    if paths:
        img = Image.open(paths[0][query][0])
        img.show()
    else:
        print("No se encontraron imágenes para la consulta:", query)

descargar_imagen_google("un dragon")

# import requests
# from io import BytesIO
# from PIL import Image
# from googlesearch import search

# def descargar_imagen_google(query):
#     url = next(search(query, num=1, stop=1))
#     response = requests.get(url)
#     img = Image.open(BytesIO(response.content))
#     img.show()

# descargar_imagen_google("un dragon")
