import cv2
import numpy as np
from transformers import ViTFeatureExtractor, ViTForImageClassification
import torch
TF_ENABLE_ONEDNN_OPTS=0

def remove_background(image):
    # Convertir l'image en couleur BGR en couleur RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Redimensionner l'image pour accélérer le traitement
    resized_image = cv2.resize(image_rgb, (100, 100))

    # Convertir l'image en une liste de pixels
    pixels = resized_image.reshape((-1, 3))

    # Convertir les données en type float
    pixels = np.float32(pixels)

    # Définir les critères de l'algorithme K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Spécifier le nombre de clusters (couleurs) à trouver
    k = 3

    # Appliquer l'algorithme K-means
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convertir les centres des clusters en entiers
    centers = np.uint8(centers)

    # Identifier la couleur dominante (le cluster le plus grand)
    unique, counts = np.unique(labels, return_counts=True)
    dominant_color_index = unique[np.argmax(counts)]

    # Reformater le tableau labels pour correspondre aux dimensions du masque
    labels_reshaped = labels.reshape(resized_image.shape[:2])

    # Créer le masque en fonction de la couleur dominante
    mask = np.zeros_like(labels_reshaped, dtype=np.uint8)
    mask[labels_reshaped == dominant_color_index] = 255

    # Redimensionner le masque à la taille de l'image d'origine
    mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))

    # Inverser le masque
    inverted_mask = cv2.bitwise_not(mask_resized)

    # Appliquer le masque inversé pour enlever le fond
    bg_removed = cv2.bitwise_and(image_rgb, image_rgb, mask=inverted_mask)

    return bg_removed, inverted_mask

def detect_background(image, mask):
    pass

def combine_images(foreground, background, mask):
    
    # Redimensionner le fond pour qu'il corresponde à la taille de l'avant-plan
    scale_factor = min(foreground.shape[1] / background.shape[1], foreground.shape[0] / background.shape[0])
    resized_width = int(background.shape[1] * scale_factor)
    resized_height = int(background.shape[0] * scale_factor)
    resized_background = cv2.resize(background, (resized_width, resized_height))

    # Décider les coordonnées de départ pour placer le fond
    start_x = max((foreground.shape[1] - resized_width) // 2, 0)
    start_y = max((foreground.shape[0] - resized_height) // 2, 0)
    end_x = min(start_x + resized_width, foreground.shape[1])
    end_y = min(start_y + resized_height, foreground.shape[0])

    # Créer une masque inversée
    mask_inv = cv2.bitwise_not(mask)

    # Créer une image noire avec le fond placé au bon endroit
    combined = np.copy(foreground)
    combined[start_y:end_y, start_x:end_x] = resized_background

    # Appliquer le masque pour ne garder que l'avant-plan
    combined_masked = cv2.bitwise_and(combined, combined, mask=mask_inv)

    # Appliquer un flou gaussien sur le masque pour adoucir les transitions
    mask_blurred = cv2.GaussianBlur(mask, (21, 21), 0)

    # Normaliser le masque flou pour qu'il soit entre 0 et 1
    mask_blurred = mask_blurred / 255.0

    # Redimensionner le masque flou pour correspondre à la forme de l'image avant-plan
    mask_blurred_resized = cv2.resize(mask_blurred, (foreground.shape[1], foreground.shape[0]))

    # Appliquer le masque flou aux images avant-plan et arrière-plan
    foreground_masked = foreground * mask_blurred_resized[:,:,np.newaxis]
    background_masked = resized_background * (1 - mask_blurred_resized[:,:,np.newaxis])

    # Fusionner les deux images
    final_combined = cv2.add(foreground_masked, background_masked)

    return final_combined.astype(np.uint8)


# Charger les images
foreground = cv2.imread("2.jpg")
background = cv2.imread("final_image.jpg")
# resize l'image backgroud a la taille du foreground
background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]))

# Supprimer l'arrière-plan de l'image avant-plan
foreground_no_bg, mask = remove_background(foreground)

# Détecter automatiquement le fond de l'image arrière-plan
background_detected = detect_background(background, mask)

# Combinaison des images
result = combine_images(foreground_no_bg, background_detected, mask)

# Afficher le résultat
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
