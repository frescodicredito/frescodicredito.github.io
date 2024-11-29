import os
from github import Github

# Recupera il token GitHub dalla variabile d'ambiente
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("Token non trovato. Assicurati che GITHUB_TOKEN sia configurato nei Secrets di GitHub.")

# Connessione a GitHub
g = Github(token)

# Nome del repository
repo_name = "frescodicredito/frescodicredito.github.io"
repo = g.get_repo(repo_name)

# Lettura del file index.html
try:
    file_path = "index.html"
    file = repo.get_contents(file_path)
    content = file.decoded_content.decode()
    print(f"Contenuto attuale di {file_path}:\n{content}")

    # Analizza il contenuto (esempio: suggerimento per il tag <title>)
    if "<title>" not in content:
        print("Suggerimento: aggiungi un tag <title> per migliorare la SEO.")

        # Modifica il file aggiungendo un <title>
        new_content = content.replace("<head>", "<head><title>Sito Fresco di Credito</title>")
        repo.update_file(file.path, "Aggiunto tag <title> per SEO", new_content, file.sha)
        print("File aggiornato con successo!")
    else:
        print("Il file ha già un tag <title>, nessuna modifica necessaria.")

except Exception as e:
    print(f"Errore durante la lettura o modifica del file: {e}")
