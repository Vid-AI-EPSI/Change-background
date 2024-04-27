import cv2
import requests
from PIL import Image
import numpy as np
import io
from important_words import extract_keywords
from get_url import recuperer_url_premiere_image_google
from replace_background import combine_images, remove_background

print("\033c")
querry = extract_keywords(input("Par quoi voulez-vous remplacer le fond de l'image ? "))

image_input = "2.jpg"


def main():
    # recuperer la résolution de l'image au fomrax X*Y
    image = cv2.imread(image_input)
    image_res = f"{image.shape[1]}x{image.shape[0]}"
    querry.append(image_res)
    # cree une chaine de caractere avec des + entre chaque pour la recherche
    request = "+".join(querry)
    url = f"https://www.google.com/search?q={request}&tbm=isch&tbs=isz:ex,iszw:{image.shape[1]},iszh:{image.shape[0]}"
    try:
        image_url = recuperer_url_premiere_image_google(url)
    except:
        print(f"Une erreur s'est produite lors de la récupération de l'URL de l'image : {url}")
        main()
        exit

    # Détecter et supprimer le fond vert de l'image originale
    foreground = cv2.imread(image_input)
    fg_without_green, mask = remove_background(foreground)
    try:
        # Charger l'image de fond directement avec OpenCV
        response = requests.get(image_url)
        background = np.asarray(bytearray(response.content), dtype="uint8")
        background = cv2.imdecode(background, cv2.IMREAD_COLOR)

    except Exception as e:
        print(f"Une erreur s'est produite lors du téléchargement de l'image : {image_url} \n Recherche : {url}")
        print(e)
        exit()
    # rogner l'image / agrandir au format de l'image d'origine
    background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]))

    # Combiner l'image originale sans fond vert avec l'image de fond
    combined = combine_images(fg_without_green, background, mask)

    # Enregistrer l'image finale
    cv2.imwrite('final_image_2.jpg', combined)


main()