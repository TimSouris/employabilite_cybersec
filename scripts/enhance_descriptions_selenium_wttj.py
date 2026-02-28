import pandas as pd
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Configuration
INPUT_FILE = 'data/offres_wttj_raw.csv'
OUTPUT_FILE = 'data/offres_wttj_enhanced.csv'
BATCH_SIZE = 500
MIN_DESC_LENGTH = 800  # On considère qu'en dessous de ça, c'est tronqué ou incomplet

def init_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--width=1920')
    options.add_argument('--height=1080')
    options.set_preference(
        'general.useragent.override',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
    )
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options
    )
    return driver

def get_full_description(driver, url):
    try:
        driver.get(url)
        # Attendre le chargement du corps de page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(1) # Pause humaine
        
        # Tentative 1: Selecteur main (le plus fiable d'après debug)
        try:
            main_el = driver.find_element(By.TAG_NAME, "main")
            text = main_el.text
            if len(text) > 500:
                return text
        except:
            pass
            
        # Tentative 2: Conteneur spécifique APEC
        try:
            container = driver.find_element(By.CSS_SELECTOR, "div.container-fluid.details-offer")
            text = container.text
            if len(text) > 500:
                return text
        except:
            pass
            
        # Fallback: Body
        return driver.find_element(By.TAG_NAME, "body").text
        
    except Exception as e:
        print(f"  Erreur lors du scraping de {url}: {e}")
        return None

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Fichier d'entrée {INPUT_FILE} introuvable.")
        return

    # Chargement des données
    # Si le fichier de sortie existe déjà, on le charge pour reprendre, sinon on part du raw
    if os.path.exists(OUTPUT_FILE):
        print(f"Reprise du fichier existant {OUTPUT_FILE}...")
        df = pd.read_csv(OUTPUT_FILE)
    else:
        print(f"Chargement du fichier brut {INPUT_FILE}...")
        df = pd.read_csv(INPUT_FILE)
    
    # Identifier les lignes à traiter
    # Critère: Description courte ou vide ET Source WTTJ
    # On crée une colonne 'is_enriched' si elle n'existe pas
    if 'is_enriched' not in df.columns:
        df['is_enriched'] = False
        
    # Masque des offres à traiter
    # Source WTTJ + Pas encore enrichi + Description courte
    to_process_mask = (df['source'] == 'WTTJ') & (~df['is_enriched']) & (df['description'].fillna('').astype(str).str.len() < MIN_DESC_LENGTH)
    
    indices_to_process = df[to_process_mask].index.tolist()
    
    print(f"Total offres WTTJ: {len(df[df['source'] == 'WTTJ'])}")
    print(f"Offres nécessitant enrichissement: {len(indices_to_process)}")
    
    # # On limite au batch size
    # batch_indices = indices_to_process[:BATCH_SIZE]
    # print(f"Traitement de ce lot: {len(batch_indices)} offres.")
    
    # if not batch_indices:
    #     print("Rien à faire.")
    #     return

    driver = init_driver()
    
    count = 0
    try:
        for idx in indices_to_process:
            row = df.loc[idx]
            url = row['lien']
            print(f"[{count+1}/{len(indices_to_process)}] Scraping {row['titre']} ({url})...")
            
            full_desc = get_full_description(driver, url)
            
            if full_desc and len(full_desc) > len(str(row['description'])):
                df.at[idx, 'description'] = full_desc
                df.at[idx, 'is_enriched'] = True
                print(f"  -> Succès! Nouvelle longueur: {len(full_desc)}")
            else:
                print("  -> Échec ou pas mieux. On marque comme traité pour ne pas boucler.")
                df.at[idx, 'is_enriched'] = True # On marque quand même pour avancer
            
            # Sauvegarde intermédiaire toutes les 10 offres
            if count % 10 == 0:
                df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
                
            count += 1
            
    except KeyboardInterrupt:
        print("Interruption utilisateur. Sauvegarde...")
        
    finally:
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        driver.quit()
        print(f"Fini. Données sauvegardées dans {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
