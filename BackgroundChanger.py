import cv2
import requests
import numpy as np
from VideoProcessor import VideoProcessor
import os
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from langdetect import detect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class BackgroundChanger(VideoProcessor):
    def __init__(self, video_input):
        super().__init__()
        self.video_input = video_input
        self.querry = None
        self.path_background_perso = None
        self.background_path = None
        self.video_fps = None
        self.masque = None
        self.combined = None

        self.__ask_for_background()

    def __ask_for_background(self):
        while True:
            if "o" in input("Voulez-vous télécharger votre propre fond ? (O/[N]) : ").lower():
                self.path_background_perso = input("Entrez le chemin du fond : ")
                break
            else :
                self.querry = self.__extract_keywords(input("Par quoi voulez-vous remplacer le fond de l'image ? "))
                break

    def __extract_keywords(self,sentence):
        try:
            # Détection automatique de la langue
            language = detect(sentence)
        except:
            # Utiliser la langue par défaut en cas d'échec de détection de la langue
            language = 'english'
        
        # Spécifier la langue des mots vides
        stop_words = set(stopwords.words('english')) if language != 'fr' else set(stopwords.words('french'))
        
        # Tokenisation de la phrase en mots
        words = word_tokenize(sentence)
        
        # Suppression des mots vides (stopwords)
        words = [word for word in words if word.lower() not in stop_words]
        
        # Partie du discours (POS tagging)
        tagged_words = pos_tag(words)
        
        # Liste des parties du discours qui représentent des mots importants
        important_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']  # Noms et adjectifs
        
        # Extraction des mots importants en fonction des parties du discours
        keywords = [word for word, tag in tagged_words if tag in important_tags]
        
        return keywords

    def __recuperer_url_premiere_image_google(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Activer le mode sans tête
        chrome_options.add_argument("--window-size=1920,1080")  # Définir la taille de la fenêtre
        chrome_options.add_argument("--disable-gpu")  # Désactiver le GPU (recommandé pour le mode headless)
        chrome_options.add_argument("--no-sandbox")  # Désactiver le mode sandbox (important pour certains environnements, comme Docker)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 100)  # Définir un temps d'attente maximal de 10 secondes

        try:
            driver.get(url)
            
            # Attendre et cliquer sur le bouton d'acceptation des cookies si présent
            try:
                accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'L2AGLb')))
                accept_button.click()
            except Exception as e:
                print(f"Le bouton d'acceptation des cookies n'est pas présent ou une autre erreur est survenue : {e}")

            # Attendre que la première image soit cliquable et cliquer dessus
            try :
                image_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.F0uyec')))
                image_element.click()
                
                # Attendre que l'image agrandie soit chargée et récupérer l'URL
                enlarged_image = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img.iPVvYb')))
                image_url = enlarged_image.get_attribute('src')

                if image_url and image_url.startswith('http'):
                    print("URL de l'image :", image_url)
                    return image_url
                else:
                    print(f"URL de l'image non valide : {image_url}")
                    return None
            except Exception as e:
                print(f"Une erreur s'est produite lors de la récupération de l'image : {str(e)}")
                return None
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'accès à l'URL : {str(e)}")
            return None
        finally:
            driver.quit()

    def __get_background(self):
        if self.path_background_perso is None:
            video = cv2.VideoCapture(self.video_input)
            ret, frame = video.read()
            if not ret:
                print("Erreur lors de la lecture de la vidéo")
                exit()
            video_res = f"{frame.shape[1]}x{frame.shape[0]}"
            self.querry.append(video_res)
            request = "+".join(self.querry)
            url = f"https://www.google.com/search?q={request}&tbm=isch&tbs=isz:ex,iszw:{frame.shape[1]},iszh:{frame.shape[0]}"
            try:
                image_url = self.__recuperer_url_premiere_image_google(url)
            except:
                print(f"Une erreur s'est produite lors de la récupération de l'URL de l'image : {url}")
                self.__ask_for_background()
                exit

            try:
                response = requests.get(image_url)
                background = np.asarray(bytearray(response.content), dtype="uint8")
                background = cv2.imdecode(background, cv2.IMREAD_COLOR)
            except Exception as e:
                print(f"Une erreur s'est produite lors du téléchargement de l'image : {image_url} \n Recherche : {url}")
                print(e)
                exit()
            background = cv2.resize(background, (frame.shape[1], frame.shape[0]))
            self.background_path = "background.jpg"
            cv2.imwrite(self.background_path, background)
        else :
            self.background_path = self.path_background_perso
            if not os.path.exists(self.background_path):
                print(f"Le fichier {self.background_path} n'existe pas")
                exit()

    def __process_video(self):
        self.masque = self.remove_background(self.video_input)
        self.video_fps = self.video_input.replace(".mp4", "_fps.mp4")
        self.combined = self.combine_videos(self.video_fps, self.background_path, self.masque)

    def __clean_up(self):
        os.remove(self.background_path)
        if self.background_path.replace(".jpg", ".mp4") in os.listdir():
            os.remove(self.background_path.replace(".jpg", ".mp4"))
        os.remove(self.masque)
        os.remove(self.video_fps)

    def change_bg(self):
        self.__get_background()
        self.__process_video()
        self.__clean_up()
        print("\033c")
        print(f"La vidéo a été créée avec succès : {self.combined}")


if __name__ == "__main__":
    video_input = "/home/melissa/Documents/EPSI/Bachelor/B3/vidai/greenscreen/1.mp4"
    bg_changer = BackgroundChanger(video_input)
    bg_changer.change_bg()
