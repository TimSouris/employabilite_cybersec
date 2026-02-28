import pyfiglet
import pandas as pd
import scripts.scrapers.scraper_francetravail
import scripts.scrapers.scraper_apec
import scripts.enhance_descriptions_selenium
import scripts.enhance_descriptions_selenium_wttj
import scripts.enrich_data
import scripts.clean_data


# banner = pyfiglet.figlet_format("F*ck le chomage")
# print(banner)
# print("\n\nLancement du scraping...\n\n")
# scripts.scrapers.scraper_francetravail.main()
# scripts.scrapers.scraper_apec.main()
# print("Scraping terminé !\nEnrichissement de la donnée en cours...")
# scripts.enhance_descriptions_selenium.main()
# scripts.enhance_descriptions_selenium_wttj.main()
scripts.enrich_data.main()
scripts.clean_data.main()
print("Enrichissement terminé !\n Génération du fichier final...")

df = pd.read_csv("./data/offres_enriched.csv")
filtered_df = df[
    (df['experience_estimee'] == "Junior") & 
    (df['niveau_etude_estime'] == "Bac+5") & 
    (
        # Je ne cherche qu'en IDF, à personnaliser selon les besoins (ex: "Lyon" ou "69" pour Lyon)
        (df['localisation'] == "Paris") |
        df['localisation'].astype(str).str.startswith("75") |
        df['localisation'].astype(str).str.startswith("92") |
        df['localisation'].astype(str).str.startswith("93") |
        df['localisation'].astype(str).str.startswith("94") |
        df['localisation'].astype(str).str.startswith("Île-de-France")
    )
]
colonnes_finales = ["lien", "titre", "entreprise", "contrat", "localisation", "description", "date_scraping", "source", "experience_estimee", "niveau_etude_estime"]
filtered_df = filtered_df[colonnes_finales]
filtered_df.to_csv("./data/offres_finales.csv", index=False, encoding="utf-8-sig")
print("Fichier final généré (total de " + str(len(filtered_df)) + " offres): data/offres_finales.csv")
