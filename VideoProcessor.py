import cv2
import numpy as np
import time
import os
import subprocess
from moviepy.editor import VideoFileClip, vfx

os.environ['MKL_SERVICE_FORCE_INTEL'] = '1'

class VideoProcessor:
    def __init__(self):
        pass

    def create_video(self, image_path, output_path, duration, frame_rate):
        image = cv2.imread(image_path)
        height, width, _ = image.shape
        video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))
        total_frames = int(duration * frame_rate)
        for _ in range(total_frames):
            video_writer.write(image)
        video_writer.release()

    def convert_video_to_fps(self, input_video, output_video, fps_nb=60):
        clip = VideoFileClip(input_video)
        clip = clip.fx(vfx.speedx, fps_nb/clip.fps)
        clip.write_videofile(output_video, fps=fps_nb)

    def remove_background(self, video_path):
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        fps = round(fps)
        video_fps = video_path.replace(".mp4", "_fps.mp4")
        self.convert_video_to_fps(video_path, video_fps, fps_nb=fps)
        cv2.destroyAllWindows()
        video_output_path = video_path.replace(".mp4", "_output.mov")
        commands = ["export MKL_SERVICE_FORCE_INTEL=1",f"python -m backgroundremover.cmd.cli -i \"{video_fps}\" -mk -o \"{video_output_path}\"", "cd .."]
        for command in commands:
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
                if result.stdout != "":
                    print(result.stdout)
                if result.stderr != "":
                    print(result.stderr)
            except subprocess.CalledProcessError as e:
                raise Exception(f"Erreur lors de l'exécution de la commande : {e.stderr}")
        return video_output_path

    def combine_videos(self, video_originale_path, background_path, masque_path):
        if background_path.endswith(('.jpg', '.jpeg', '.png')):
            background_video_path = background_path.replace(".jpg", ".mp4").replace(".jpeg", ".mp4").replace(".png", ".mp4")
            video = cv2.VideoCapture(video_originale_path)
            duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
            fps = video.get(cv2.CAP_PROP_FPS)
            self.create_video(background_path, background_video_path, duration, fps)
            background_path = background_video_path
        video_originale = cv2.VideoCapture(video_originale_path)
        background = cv2.VideoCapture(background_path)
        masque = cv2.VideoCapture(masque_path)
        if not video_originale.isOpened() or not background.isOpened() or not masque.isOpened():
            print("Erreur lors de l'ouverture des vidéos")
            print( video_originale_path)
            print( background_path)
            print( masque_path)
            exit()

        # Obtenir les largeurs et les hauteurs des vidéos
        video_originale_width = int(video_originale.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_originale_height = int(video_originale.get(cv2.CAP_PROP_FRAME_HEIGHT))
        background_width = int(background.get(cv2.CAP_PROP_FRAME_WIDTH))
        background_height = int(background.get(cv2.CAP_PROP_FRAME_HEIGHT))
        masque_width = int(masque.get(cv2.CAP_PROP_FRAME_WIDTH))
        masque_height = int(masque.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Vérifier que les tailles des vidéos sont les mêmes tailles
        if video_originale_width != masque_width or video_originale_height != masque_height:
            print("WARNING : les tailles des vidéos ne correspondent pas \n Vidéo originale : ", video_originale_width, "x", video_originale_height, "\n Masque : ", masque_width, "x", masque_height)
            masque_resize = cv2.VideoCapture()
            masque_resize.set(cv2.CAP_PROP_FRAME_WIDTH, video_originale_width)
            masque_resize.set(cv2.CAP_PROP_FRAME_HEIGHT, video_originale_height)

        # Redimensionner la vidéo originale pour qu'elle corresponde à la taille de la vidéo d'arrière-plan
        video_originale_resize = cv2.VideoCapture()
        video_originale_resize.set(cv2.CAP_PROP_FRAME_WIDTH, background_width)
        video_originale_resize.set(cv2.CAP_PROP_FRAME_HEIGHT, background_height)

        # Redimensionner le masque pour qu'il corresponde à la taille de la vidéo d'arrière-plan
        masque_resize = cv2.VideoCapture()
        masque_resize.set(cv2.CAP_PROP_FRAME_WIDTH, background_width)
        masque_resize.set(cv2.CAP_PROP_FRAME_HEIGHT, background_height)

        # Vérifier si les videos ont les mêmes fréquences d'images
        if video_originale.get(cv2.CAP_PROP_FPS) != background.get(cv2.CAP_PROP_FPS) or masque.get(cv2.CAP_PROP_FPS) != background.get(cv2.CAP_PROP_FPS):
            print("WARNING : les fréquences d'images des vidéos ne correspondent pas \n Vidéo originale : ", video_originale.get(cv2.CAP_PROP_FPS), "\n Masque : ", masque.get(cv2.CAP_PROP_FPS), "\n Vidéo d'arrière-plan : ", background.get(cv2.CAP_PROP_FPS))
            video_originale.set(cv2.CAP_PROP_FPS, masque.get(cv2.CAP_PROP_FPS))
            background.set(cv2.CAP_PROP_FPS, masque.get(cv2.CAP_PROP_FPS))


        # Définir la position de lecture de la vidéo originale et du masque pour qu'elles commencent au même moment
        video_originale.set(cv2.CAP_PROP_POS_FRAMES, 0)
        masque.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # Obtenir les fréquences d'images des vidéos
        fps_originale = video_originale.get(cv2.CAP_PROP_FPS)
        fps_masque = masque.get(cv2.CAP_PROP_FPS)

        # Créer un objet VideoWriter pour enregistrer la vidéo de sortie
        # Utilisez la fréquence d'images de la vidéo d'arrière-plan pour la vidéo de sortie
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(video_originale_path.replace(".mp4", "__final.mp4"), fourcc, fps_originale, (background_width, background_height))

        # Créer des compteurs de frames pour les vidéos
        frame_count_originale = 0

        while True:
            # Lire les frames des vidéos
            ret_originale, frame_originale = video_originale.read()
            ret_background, frame_background = background.read()

            # Vérifier que les frames ont été lues correctement
            if not ret_originale or not ret_background:
                break

            # Lire la frame correspondante du masque en fonction du compteur de frames
            frame_count_originale += 1
            masque.set(cv2.CAP_PROP_POS_FRAMES, frame_count_originale * fps_originale / fps_masque)
            ret_masque, frame_masque = masque.read()

            if not ret_masque:
                break
            # Redimensionner la frame de la vidéo originale
            frame_originale_resize = cv2.resize(frame_originale, (background_width, background_height))

            # Redimensionner la frame du masque
            frame_masque_resize = cv2.resize(frame_masque, (background_width, background_height))

            
            # Convertir les frames en noir et blanc
            gray_masque = cv2.cvtColor(frame_masque_resize, cv2.COLOR_BGR2GRAY)

            # Créer un masque binaire à partir de l'image en noir et blanc
            _, mask = cv2.threshold(gray_masque, 10, 255, cv2.THRESH_BINARY)

            # Créer une image de la même taille que la vidéo d'arrière-plan remplie de zeros
            foreground = np.zeros_like(frame_background)

            # Copier la vidéo originale redimensionnée dans l'image de premier plan en utilisant le masque
            foreground[np.where(mask == 255)] = frame_originale_resize[np.where(mask == 255)]

            # Créer un masque inversé pour la vidéo d'arrière-plan
            mask_inv = cv2.bitwise_not(mask)

            # Créer une image de la même taille que la vidéo d'arrière-plan remplie de zeros
            background_inv = np.zeros_like(frame_background)

            # Copier la vidéo d'arrière-plan dans l'image de premier plan en utilisant le masque inversé
            background_inv[np.where(mask_inv == 255)] = frame_background[np.where(mask_inv == 255)]

            # Superposer l'image de premier plan sur la vidéo d'arrière-plan
            output = cv2.add(foreground, background_inv)
            # Écrire la frame de sortie dans l'objet VideoWriter
            out.write(output)

        # Libérer les ressources
        video_originale.release()
        background.release()
        masque.release()
        video_originale_resize.release()
        masque_resize.release()
        out.release()
        cv2.destroyAllWindows()

        return video_originale_path.replace(".mp4", "__final.mp4")
