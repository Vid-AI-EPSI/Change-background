from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def recuperer_url_premiere_image_google(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)
        try:
            accept_button = driver.find_element(By.ID, 'L2AGLb')
            accept_button.click()
            time.sleep(1)
        except Exception as e:
            pass
        # Localiser la première image et cliquer dessus pour l'afficher en grand
        image_element = driver.find_element(By.CSS_SELECTOR, 'div.F0uyec')
        image_element.click()
        time.sleep(5)
        # faire clqiue droit "copier l'adresse de l'image"
        image_url = driver.find_element(By.CSS_SELECTOR, 'img.iPVvYb').get_attribute('src')

        if image_url.startswith('http'):
            print("URL de l'image :", image_url)
            return image_url
        else:
            print(f"URL de l'image non valide : {image_url} .")
            return None
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None
    finally:
        driver.quit()

