import nltk
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from langdetect import detect

def extract_keywords(sentence):
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
