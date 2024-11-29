import os
from github import Github
from dotenv import load_dotenv

# Carica le variabili dal file .env
# Modifica: Specifica manualmente il percorso del file .env
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# Debug: verifica se il token è stato caricato
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("Errore: Il GITHUB_TOKEN non è stato trovato. Assicurati che il file .env sia configurato correttamente.")
else:
    print(f"Token GitHub caricato correttamente: {token[:5]}... (troncato per sicurezza)")

# Funzione per creare un nuovo file
def create_new_file(repo, file_path, content, commit_message):
    try:
        repo.create_file(file_path, commit_message, content, branch="main")
        print(f"File '{file_path}' creato con successo.")
    except Exception as e:
        print(f"Errore durante la creazione del file '{file_path}': {e}")

# Funzione per modificare un file esistente
def update_file(repo, file_path, new_content, commit_message):
    try:
        file = repo.get_contents(file_path)
        repo.update_file(file.path, commit_message, new_content, file.sha, branch="main")
        print(f"File '{file_path}' aggiornato con successo.")
    except Exception as e:
        print(f"Errore durante l'aggiornamento del file '{file_path}': {e}")

# Funzione per caricare immagini nel repository
def upload_image(repo, image_path, commit_message):
    try:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        file_name = os.path.basename(image_path)
        repo.create_file(f"images/{file_name}", commit_message, content, branch="main")
        print(f"Immagine '{file_name}' caricata con successo nella directory 'images/'.")
    except Exception as e:
        print(f"Errore durante il caricamento dell'immagine '{image_path}': {e}")

# Funzione per aggiungere immagini a un file HTML
def add_image_to_html(repo, file_path, image_name, alt_text="Immagine"):
    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode()

        if "</body>" in content:
            new_content = content.replace(
                "</body>",
                f'<img src="images/{image_name}" alt="{alt_text}">\n</body>'
            )
            update_file(repo, file_path, new_content, "Aggiunta immagine al file HTML")
            print(f"Immagine '{image_name}' aggiunta al file '{file_path}'.")
        else:
            print("Struttura del file HTML non trovata.")
    except Exception as e:
        print(f"Errore durante l'aggiunta dell'immagine al file HTML: {e}")

# Funzione per creare una nuova pagina HTML
def create_html_page(repo, page_name, title, content):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <h1>{title}</h1>
        <div>{content}</div>
    </body>
    </html>
    """
    create_new_file(repo, f"{page_name}.html", html_content, f"Creata nuova pagina {page_name}")

# Funzione per aggiungere una voce al menu
def add_menu_item(repo, menu_path, menu_item_name, menu_item_link):
    try:
        file = repo.get_contents(menu_path)
        content = file.decoded_content.decode()

        menu_item = f'<li><a href="{menu_item_link}">{menu_item_name}</a></li>'
        if "</ul>" in content:
            updated_content = content.replace("</ul>", f"  {menu_item}\n</ul>")
            update_file(repo, menu_path, updated_content, "Aggiunta nuova voce di menu")
            print(f"Voce di menu '{menu_item_name}' aggiunta con successo.")
        else:
            print("Struttura del menu non trovata.")
    except Exception as e:
        print(f"Errore durante l'aggiunta della voce di menu: {e}")

# Funzione per gestire comandi dinamici
def process_command(command, repo):
    print(f"Comando ricevuto: {command}")
    if "crea pagina" in command:
        page_name = input("Inserisci il nome del file HTML (senza estensione): ")
        title = input("Inserisci il titolo della pagina: ")
        content = input("Inserisci il contenuto HTML della pagina: ")
        create_html_page(repo, page_name, title, content)

    elif "aggiungi voce menu" in command:
        menu_path = "index.html"
        menu_item_name = input("Inserisci il nome della voce di menu: ")
        menu_item_link = input("Inserisci il link della voce di menu: ")
        add_menu_item(repo, menu_path, menu_item_name, menu_item_link)

    elif "carica immagine" in command:
        image_path = input("Inserisci il percorso dell'immagine da caricare: ")
        upload_image(repo, image_path, "Caricata nuova immagine")

    elif "aggiungi immagine" in command:
        html_file = input("Inserisci il nome del file HTML (es. index.html): ")
        image_name = input("Inserisci il nome dell'immagine (es. banner.jpg): ")
        alt_text = input("Inserisci il testo alternativo (alt) per l'immagine: ")
        add_image_to_html(repo, html_file, image_name, alt_text)

    else:
        print("Comando non riconosciuto. Prova con 'crea pagina', 'aggiungi voce menu', 'carica immagine', o 'aggiungi immagine'.")

# Inizia il processo
def main():
    print("Lo script è stato avviato correttamente.")

    # Connessione a GitHub
    g = Github(token)

    # Nome del repository
    repo_name = "frescodicredito/frescodicredito.github.io"
    repo = g.get_repo(repo_name)

    print("Connessione al repository effettuata con successo!")
    print("Esempi di comandi:")
    print("- 'Crea pagina'")
    print("- 'Aggiungi voce menu'")
    print("- 'Carica immagine'")
    print("- 'Aggiungi immagine'")
    command = input("Inserisci il comando da eseguire: ").lower()

    # Esegui il comando
    process_command(command, repo)

if __name__ == "__main__":
    main()
