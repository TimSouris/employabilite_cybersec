
import pandas as pd
import re
import os

# --- Configuration des Mots-clés ---

KEYWORDS = {
    # Langages de programmation
    "Python": [r"python"],
    "C": [r"\bC\b"],
    "C++": [r"c\+\+"],
    "C#": [r"c#"],
    "Java": [r"\bjava\b"],
    "JavaScript": [r"javascript", r"js"],
    "Go": [r"\bgo\b", r"golang"],
    "Rust": [r"rust"],
    "Bash": [r"bash", r"shell scripting"],
    "PowerShell": [r"powershell"],
    "SQL": [r"sql"],
    "Assembly": [r"assembly", r"assembleur"],

    # Networking & Protocols
    "TCP/IP": [r"tcp/ip", r"tcp"],
    "DNS": [r"\bdns\b"],
    "VPN": [r"\bvpn\b"],
    "BGP": [r"\bbgp\b"],
    "OSPF": [r"\bospf\b"],
    "SSL/TLS": [r"ssl/tls", r"ssl", r"tls"],

    # Cloud & DevOps
    "AWS": [r"aws", r"amazon web services"],
    "Azure": [r"azure"],
    "GCP": [r"gcp", r"google cloud"],
    "Docker": [r"docker"],
    "Kubernetes": [r"kubernetes", r"k8s"],
    "Git": [r"git", r"github", r"gitlab"],
    "Linux": [r"linux"],
    "Windows Server": [r"windows server"],
    "CI/CD": [r"ci/cd", r"cicd", r"jenkins", r"gitlab ci"],

    # Outils Pentest & Offensive Security
    "Nmap": [r"nmap"],
    "Metasploit": [r"metasploit"],
    "Wireshark": [r"wireshark"],
    "Tcpdump": [r"tcpdump"],
    "Burp Suite": [r"burp suite", r"burpsuite"],
    "SQLmap": [r"sqlmap"],
    "Hydra": [r"hydra"],
    "John The Ripper": [r"john the ripper", r"john"],
    "Hashcat": [r"hashcat"],
    "Aircrack-ng": [r"aircrack-ng", r"aircrack"],
    "Nessus": [r"nessus"],
    "OpenVAS": [r"openvas"],
    "Kali Linux": [r"kali linux", r"kalilinux"],

    # Outils Security & Defensive
    "Splunk": [r"splunk"],
    "ELK Stack": [r"elk", r"elasticsearch", r"logstash", r"kibana"],
    "SIEM": [r"siem"],
    "IDS/IPS": [r"ids/ips", r"ids", r"ips", r"suricata", r"snort"],
    "EDR": [r"edr", r"endpoint detection response"],
    "WAF": [r"\bwaf\b", r"web application firewall"],
    "Firewall": [r"firewall", r"palo alto", r"checkpoint", r"fortinet"],

    # Cybersecurity Concepts & Practices
    "Pentest": [r"pentest", r"penetration testing", r"penetration test"],
    "Vulnerability Assessment": [r"vulnerability assessment", r"vulnerabilité"],
    "OSINT": [r"osint", r"open source intelligence", r"reconnaissance"],
    "Threat Intelligence": [r"threat intelligence", r"renseignement de menace"],
    "Incident Response": [r"incident response", r"réponse aux incidents"],
    "Malware Analysis": [r"malware analysis", r"analyse de malware"],
    "Reverse Engineering": [r"reverse engineering", r"rétro-ingénierie"],
    "Forensics": [r"forensics", r"digital forensics", r"forensique"],
    "SOC": [r"\bsoc\b", r"security operations"],
    "Cryptography": [r"cryptography", r"cryptographie", r"encryption"],
    "PKI": [r"\bpki\b", r"public key infrastructure"],
    "OWASP": [r"owasp", r"top 10"],

    # CTF platforms
    "Hack The Box": [r"hack the box", r"htb"],
    "TryHackMe": [r"tryhackme", r"thm"],
    "HackTheBox": [r"hackthebox"],

    # Security Certifications & Standards
    "CISSP": [r"cissp"],
    "CEH": [r"ceh", r"certified ethical hacker"],
    "OSCP": [r"oscp", r"offensive security"],
    "Security+": [r"security\+", r"comptiа\+"],
    "CySA+": [r"cysa\+"],
    "ISO 27001": [r"iso 27001", r"iso27001"],
    "NIST": [r"nist", r"cybersecurity framework"],

    # Soft Skills & Langues
    "Anglais": [r"anglais", r"english"],
    "Agile": [r"agile", r"scrum", r"kanban"],
    "Communication": [r"communication"],
    "Rigueur": [r"rigueur", r"rigoureux"],
    "Curiosité": [r"curiosité", r"curieux"],
    "Travail d'équipe": [r"travail d'équipe", r"team player", r"esprit d'équipe"],
    "Gestion de projet": [r"gestion de projet", r"chef de projet"],
}

EDUCATION_LEVELS = {
    "Bac+5": [r"bac\+5", r"master", r"ingénieur", r"msc", r"grande école"],
    "Bac+3/4": [r"bac\+3", r"bac\+4", r"licence", r"bachelor"],
    "PhD": [r"phd", r"doctorat", r"docteur"]
}

def extract_skills(text, keywords_dict):
    found_skills = {}
    if not isinstance(text, str):
        for k in keywords_dict:
            found_skills[k] = False
        return found_skills
    
    text_lower = text.lower()
    
    for skill, patterns in keywords_dict.items():
        found = False
        for pat in patterns:
            if re.search(pat, text_lower):
                found = True
                break
        found_skills[skill] = int(found) # 1 si trouvé, 0 sinon pour Power BI
        
    return found_skills

def extract_experience(text):
    if not isinstance(text, str):
        return "Non précisé"
    
    text_lower = text.lower()
    
    # Motifs explicites
    if re.search(r"débutant|junior|première expérience", text_lower):
        return "Junior"
    
    match_years = re.search(r"(\d+)\s*(?:ans|années|an|year)", text_lower)
    if match_years:
        try:
            years = int(match_years.group(1))
            if years <= 2:
                return "Junior"
            elif years <= 5:
                return "Confirmé"
            else:
                return "Senior"
        except:
            pass
            
    if re.search(r"senior|expert|lead|manager", text_lower):
        return "Senior"
        
    if re.search(r"confirmé|expérimenté|experienced", text_lower):
        return "Confirmé"
        
    return "Non précisé"

def extract_education(text):
    if not isinstance(text, str):
        return "Non précisé"
    
    text_lower = text.lower()
    for level, patterns in EDUCATION_LEVELS.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                return level
    return "Non précisé"

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    # 1. Charger les fichier bruts (selon ce qui existe)
    # 1. Charger les fichier bruts
    dfs = []
    
    # On charge TOUT (Enhanced en premier pour priorite)
    files = ["offres_apec_enhanced.csv", "offres_apec_raw.csv", "offres_francetravail_raw.csv", "offres_wttj_raw.csv", "offres_apec_listings.csv"]
    
    for f in files:
        path = os.path.join(data_dir, f)

        if os.path.exists(path):
            print(f"Chargement de {f}...")
            # Try/except pour utf-8 vs cp1252 si besoin, mais pandas gère souvent bien
            try:
                df_tmp = pd.read_csv(path)
            except UnicodeDecodeError:
                df_tmp = pd.read_csv(path, encoding='cp1252')
            
            # Standardisation immédiate des colonnes clés
            df_tmp.columns = [c.lower().strip() for c in df_tmp.columns] # tout en minuscule et strip
            
            # Remove duplicate columns if any (prevents concat crash)
            if df_tmp.columns.duplicated().any():
                print(f"  -> Parsing: Removing duplicate columns in {f}: {df_tmp.columns[df_tmp.columns.duplicated()].tolist()}")
                df_tmp = df_tmp.loc[:, ~df_tmp.columns.duplicated()]
            
            print(f"  -> Colonnes trouvées (normalisées): {list(df_tmp.columns)}")

            # Renommage spécifique si besoin (ex: 'post_description' -> 'description')
            rename_map = {}
            for col in df_tmp.columns:
                if 'desc' in col and 'description' not in rename_map.values():
                    rename_map[col] = 'description'
                if 'titre' in col or 'title' in col:
                     rename_map[col] = 'titre'
                if 'company' in col or 'entreprise' in col:
                     rename_map[col] = 'entreprise'
                if 'link' in col or 'lien' in col or 'url' in col:
                     rename_map[col] = 'lien'
                if 'contrat' in col or 'contract' in col:
                     rename_map[col] = 'contrat'
                if 'location' in col or 'localisation' in col:
                     rename_map[col] = 'localisation'
                if 'date' in col:
                     rename_map[col] = 'date_scraping'

            print(f"  -> Mapping: {rename_map}")
            df_tmp.rename(columns=rename_map, inplace=True)
            
            # Re-dedup columns after rename (rename can create duplicates!)
            if df_tmp.columns.duplicated().any():
                print(f"  -> Parsing: Removing duplicate columns after rename: {df_tmp.columns[df_tmp.columns.duplicated()].tolist()}")
                df_tmp = df_tmp.loc[:, ~df_tmp.columns.duplicated()]
            
            # --- RECUPERATION DES DONNEES MANQUANTES ---
            # Pour APEC, contrat et loc sont souvent dans la description
            def recover_data(row):
                desc = str(row.get('description', '')).lower()
                
                # Recuperation Contrat
                if pd.isna(row.get('contrat')) or str(row.get('contrat')).strip() == '':
                    if 'cdi' in desc: row['contrat'] = 'CDI'
                    elif 'cdd' in desc: row['contrat'] = 'CDD'
                    elif 'stage' in desc: row['contrat'] = 'Stage'
                    elif 'alternance' in desc or 'contrat pro' in desc or 'apprentissage' in desc: row['contrat'] = 'Alternance'
                    elif 'freelance' in desc or 'indépendant' in desc: row['contrat'] = 'Freelance'
                    elif 'intérim' in desc: row['contrat'] = 'Intérim'
                
                # Recuperation Localisation
                if pd.isna(row.get('localisation')) or str(row.get('localisation')).strip() == '':
                    # Liste des grandes villes et hubs tech
                    cities = ['paris', 'lyon', 'bordeaux', 'lille', 'nantes', 'toulouse', 'marseille', 'rennes', 'strasbourg', 'montpellier', 'nice', 'sophia antipolis', 'la défense', 'boulogne', 'courbevoie', 'levallois', 'issy', 'télétravail', 'remote', 'france']
                    for city in cities:
                        if city in desc:
                            row['localisation'] = city.title()
                            break # On prend la première trouvée
                            
                return row

            print("  -> Tentative de récupération des données manquantes (Contrat/Loc)...")
            df_tmp = df_tmp.apply(recover_data, axis=1)

            # Debug stats colonnes
            if 'contrat' in df_tmp.columns:
                print(f"  -> Contrat non-null (apres recovery): {df_tmp['contrat'].notna().sum()} / {len(df_tmp)}")
            if 'localisation' in df_tmp.columns:
                print(f"  -> Localisation non-null (apres recovery): {df_tmp['localisation'].notna().sum()} / {len(df_tmp)}")
            
            # Ajouter colonne source si absente
            if 'source' not in df_tmp.columns:
                if 'apec' in f:
                    df_tmp['source'] = 'APEC'
                elif 'wttj' in f:
                    df_tmp['source'] = 'WTTJ'
                elif 'francetravail' in f:
                    df_tmp['source'] = 'France Travail'
            
            print(f"  -> {len(df_tmp)} offres chargées. Colonnes: {list(df_tmp.columns)}")
            dfs.append(df_tmp)
    
    if not dfs:
        print("Aucun fichier de données trouvé dans data/")
        return

    df_full = pd.concat(dfs, ignore_index=True)
    print(f"Total offres brutes concaténées : {len(df_full)}")
    
    # Deduplicate columns globally (failsafe)
    if df_full.columns.duplicated().any():
        print(f"CRITICAL: Found duplicate columns in combined DF: {df_full.columns[df_full.columns.duplicated()].tolist()}")
        df_full = df_full.loc[:, ~df_full.columns.duplicated()]
        print("CRITICAL: Removed duplicate columns.")

    # Deduplication rows (Priorité au premier chargé -> Enhanced)
    if 'lien' in df_full.columns:
        before = len(df_full)
        df_full.drop_duplicates(subset=['lien'], keep='first', inplace=True)
        print(f"Deduplication (sur lien) : {before} -> {len(df_full)} (-{before - len(df_full)})")
    
    # 2. Nettoyage de base
    def sanitize_text(text):
        if not isinstance(text, str):
            return ""
        # Nettoyage HTML residuel
        text = re.sub(r'<[^>]+>', ' ', text)
        # Remplacer sauts de ligne et tabulations par des espaces
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        # Remplacer les points virgules (conflit CSV parfois) par des virgules
        text = text.replace(';', ',')
        # Enlever les espaces multiples
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    # S'assurer que 'description' existe
    if 'description' not in df_full.columns:
        print("ATTENTION: Colonne 'description' introuvable après standardisation. Création vide.")
        df_full['description'] = ""
    
    # Remplir description vide et nettoyer
    df_full['description'] = df_full['description'].fillna("").astype(str).apply(sanitize_text)
    df_full['titre'] = df_full['titre'].fillna("").astype(str).apply(sanitize_text)
    df_full['entreprise'] = df_full['entreprise'].fillna("").astype(str).apply(sanitize_text)
    
    # Check stats descriptions
    nb_desc = df_full[df_full['description'].str.len() > 20].shape[0]
    print(f"Nombre d'offres avec description > 20 chars : {nb_desc} / {len(df_full)}")
    
    # 3. Enrichissement
    print("Enrichissement en cours (Extraction des compétences)...")
    
    # Reset index pour alignement parfait
    df_full = df_full.reset_index(drop=True)
    
    # Appliquer extraction skills
    skills_data = df_full['description'].apply(lambda x: extract_skills(x, KEYWORDS))
    df_skills = pd.DataFrame(skills_data.tolist())
    
    # Fusionner via assignation directe (plus robuste que concat axis=1)
    df_enriched = df_full.copy()
    for col in df_skills.columns:
        df_enriched[col] = df_skills[col]
        
    print(f"Fusion compétences terminée. Shape: {df_enriched.shape}")
    
    # Extraire Expérience & Formation
    df_enriched['experience_estimee'] = (df_enriched['titre'].astype(str) + " " + df_enriched['description'].astype(str)).apply(extract_experience)
    df_enriched['niveau_etude_estime'] = df_enriched['description'].apply(extract_education)
    
    # 4. Sauvegarde Format Large (Tout en un)
    # On garde les colonnes principales + skills
    cols_base = ['titre', 'entreprise', 'contrat', 'localisation', 'date_scraping', 'source', 'lien', 'experience_estimee', 'niveau_etude_estime', 'description']
    
    # Ajouter toutes les colonnes skills
    cols_final = []
    for c in df_enriched.columns:
        if c in cols_base or c in KEYWORDS.keys():
            cols_final.append(c)
    
    # Assurer que toutes les colonnes de base sont là (même vides)
    for c in cols_base:
        if c not in df_enriched.columns:
             df_enriched[c] = None

    # Garder aussi région si dispo
    if 'region' in df_enriched.columns:
         cols_final.append('region')

    df_final = df_enriched[cols_final]

    output_wide = os.path.join(data_dir, "offres_enriched.csv")
    df_final.to_csv(output_wide, index=False, encoding='utf-8-sig')
    print(f"Fichier enrichi sauvegardé : {output_wide}")
    
    # 5. Sauvegarde Format Long (Un skill par ligne) pour Power BI
    print("Génération du format 'Skills Long' pour Power BI...")
    
    # On doit avoir un identifiant unique. Si 'lien' est vide ou dupliqué, on crée un ID
    df_enriched['id_offre'] = df_enriched.index
    
    skills_cols = list(KEYWORDS.keys())
    
    # Vérifier que les skills sont bien dans le df
    present_skills = [c for c in skills_cols if c in df_enriched.columns]
    
    if not present_skills:
        print("Erreur : Aucune colonne compétence trouvée pour le pivot.")
        return

    df_long = pd.melt(df_enriched, 
                      id_vars=['id_offre', 'titre', 'entreprise', 'source'], 
                      value_vars=present_skills, 
                      var_name='Competence', 
                      value_name='Present')
    
    # Garder que les lignes où Present = 1
    df_long = df_long[df_long['Present'] == 1].drop(columns=['Present'])
    
    # output_long = os.path.join(data_dir, "skills_powerbi.csv")
    # df_long.to_csv(output_long, index=False, encoding='utf-8-sig')
    # print(f"Fichier Skills Long sauvegardé : {output_long} ({len(df_long)} lignes)")

if __name__ == "__main__":
    main()
