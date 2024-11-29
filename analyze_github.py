import os
from github import Github

# Funzione per processare comandi dal GPT
def process_command_from_gpt(command, repo):
    if "crea pagina" in command:
        # Estrarre i dettagli del comando
        page_name = input("Nome della pagina HTML (senza estensione): ")
        title = input("Titolo della pagina: ")
        content = input("Contenuto HTML della pagina: ")

        # Genera il file HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
            {content}
        </body>
        </html>
        """
        # Crea la nuova pagina nel repository
        file_path = f"{page_name}.html"
        commit_message = f"Creata nuova pagina {page_name}"
        try:
            repo.create_file(file_path, commit_message, html_content, branch="main")
            print(f"Pagina {page_name}.html creata con successo!")
        except Exception as e:
            print(f"Errore durante la creazione della pagina: {e}")

# Connessione a GitHub
def main():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Errore: GITHUB_TOKEN non trovato. Configura il file .env.")

    g = Github(token)
    repo_name = "frescodicredito/frescodicredito.github.io"
    repo = g.get_repo(repo_name)

    print("Inserisci un comando per il GPT:")
    command = input("> ").lower()

    process_command_from_gpt(command, repo)

if __name__ == "__main__":
    main()

