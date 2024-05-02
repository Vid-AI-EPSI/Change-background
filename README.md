# Video Background Changer

Video Background Changer est un projet Python qui permet de remplacer le fond d'une vidéo par une image ou une autre vidéo. Le projet utilise des techniques de traitement d'images et de vidéos, ainsi que des bibliothèques telles que OpenCV, MoviePy et PyMatting pour extraire le premier plan de la vidéo et le combiner avec un nouveau fond.

## Table des matières

1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Fonctionnalités](#fonctionnalités)
4. [Structure du projet](#structure-du-projet)
5. [Historique des versions](#historique-des-versions)
6. [Contact](#contact)
7. [Axes d'amélioration](#axes-damélioration)

## Installation

Pour utiliser Video Background Changer, nous recommandons d'utiliser Anaconda pour une gestion optimale des dépendances. Vous pouvez installer Anaconda à partir de [https://www.anaconda.com/](https://www.anaconda.com/).

Une fois que vous avez installé Anaconda, vous pouvez créer un nouvel environnement en utilisant la commande suivante :
```bash
conda create -n video-bg-changer python=3.10
```
Ensuite, activez l'environnement en utilisant la commande suivante :
```bash
conda activate video-bg-changer
```
Vous pouvez maintenant installer les dépendances nécessaires en utilisant pip :
```
pip install -r requirements.txt
```
Notez que PyTorch est utilisé dans ce projet, nous vous recommandons donc d'utiliser la commande suivante pour installer PyTorch en fonction de votre système d'exploitation et de votre carte graphique :
```bash
conda install pytorch torchvision torchaudio -c pytorch
```
Pour plus d'informations sur l'installation de PyTorch, consultez [https://pytorch.org/](https://pytorch.org/).

## Utilisation

Pour utiliser Video Background Changer, vous devez créer une instance de la classe `BackgroundChanger` en lui passant le chemin de la vidéo que vous voulez modifier. Ensuite, vous pouvez appeler la méthode `change_bg()` pour remplacer le fond de la vidéo.

Voici un exemple d'utilisation :
```python
from BackgroundChanger import BackgroundChanger

video_input = "/home/melissa/Documents/EPSI/Bachelor/B3/vidai/greenscreen/1.mp4"
bg_changer = BackgroundChanger(video_input)
bg_changer.change_bg()
```
Lorsque vous appelez la méthode `change_bg()`, le programme vous demandera si vous voulez télécharger votre propre fond ou si vous voulez utiliser une image trouvée sur Google. Si vous choisissez la deuxième option, le programme utilisera des techniques de NLP (Natural Language Processing) pour simplifier votre requête de recherche et trouver des images pertinentes.

Une fois que vous avez choisi le fond, le programme extrait le premier plan de la vidéo en utilisant la bibliothèque PyMatting, puis combine le premier plan avec le nouveau fond en utilisant OpenCV et MoviePy. Le résultat final est enregistré dans un fichier vidéo.

## Fonctionnalités

Voici les fonctionnalités de Video Background Changer :

* Extraction du premier plan de la vidéo à l'aide de PyMatting
* Recherche d'une image de fond sur Google en fonction d'une requête de recherche simplifiée par NLP
* Utilisation d'une image personnalisée comme fond
* Combinaison du premier plan et du fond en utilisant OpenCV et MoviePy
* Enregistrement du résultat final dans un fichier vidéo

## Structure du projet

Le projet est structuré comme suit :
```markdown
video-background-changer/
├── BackgroundChanger.py
├── VideoProcessor.py
├── backgroundremover/
│   ├── cmd/
│   │   └── cli.py
│   ├── data/
│   ├── models/
│   ├── utils/
│   ├── __init__.py
│   └── ...
├── requirements.txt
└── README.md
```
* `BackgroundChanger.py` : contient la classe principale `BackgroundChanger` qui gère l'ensemble du processus de remplacement du fond de la vidéo.
* `VideoProcessor.py` : contient la classe `VideoProcessor` qui gère la création de vidéos et la conversion de vidéos en différents formats.
* `backgroundremover/` : contient une version adaptée du code de [https://github.com/nadermx/backgroundremover](https://github.com/nadermx/backgroundremover) qui est utilisé par la classe `BackgroundChanger` pour extraire le premier plan de la vidéo.
* `requirements.txt` : contient la liste des bibliothèques requises pour le projet.
* `README.md` : contient les instructions d'installation et d'utilisation du projet.

## Historique des versions

* 0.1 : version initiale

## Contact

Si vous avez des questions ou des commentaires sur Video Background Changer, n'hésitez pas à contacter [Mélissa Colin](mailto:melissa.colin0@proton.me).

## Axes d'amélioration

Voici quelques axes d'amélioration possibles pour Video Background Changer :

* Ajout de la possibilité d'utiliser des images ou des vidéos générées par une IA comme fond.
* Ajout de la possibilité de charger des vidéos de fond à partir d'Internet.
* Amélioration de la qualité de l'extraction du premier plan en utilisant des techniques plus avancées de traitement d'images.
* Optimisation des performances du programme pour réduire le temps de traitement.