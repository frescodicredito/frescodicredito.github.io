import os
from github import Github

from dotenv import load_dotenv
import os

# Carica il file .env dal percorso specifico
dotenv_path = os.path.join(os.getcwd(), ".env")
print(f"Tentativo di caricare il file .env dal percorso: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)

# Debug: verifica il valore del token
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("Errore: GITHUB_TOKEN non trovato. Assicurati che il file .env sia nella directory corretta.")
else:
    print(f"Token trovato: {token[:5]}... (troncato per sicurezza)")

def list_repo_files(repo):
    """Elenca i file nel repository."""
    print("Elenco dei file nel repository:")
    try:
        contents = repo.get_contents("")
        for content in contents:
            print(f"- {content.path}")
    except Exception as e:
        print(f"Errore durante l'elenco dei file: {e}")

def read_file_content(repo, file_path):
    """Legge il contenuto di un file nel repository."""
    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode()
        print(f"\nContenuto del file '{file_path}':\n{content[:500]}...\n")
        return content
    except Exception as e:
        print(f"Errore durante la lettura del file '{file_path}': {e}")
        return None

import sys

def main():
    # Leggi il comando dalla riga di comando
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if not command:
        print("Errore: Nessun comando fornito.")
        return

    print(f"Comando ricevuto: {command}")

    # Configura il token GitHub
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Errore: GITHUB_TOKEN non trovato. Assicurati di aver configurato il file .env.")

    # Connessione a GitHub
    g = Github(token)

    # Nome del repository
    repo_name = "frescodicredito/frescodicredito.github.io"
    try:
        repo = g.get_repo(repo_name)
        print(f"Connessione al repository '{repo_name}' effettuata con successo!")
    except Exception as e:
        print(f"Errore durante la connessione al repository: {e}")
        return

    # Esegui il comando
    process_command(command, repo)

if __name__ == "__main__":
    main()
