import os
from github import Github

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

# Funzione per generare immagini con DALL·E
def generate_image_with_dalle(prompt):
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response["data"][0]["url"]
        
        # Scarica l'immagine generata
        import requests
        response = requests.get(image_url)
        file_name = "dalle_generated_image.png"
        with open(file_name, "wb") as file:
            file.write(response.content)
        
        print(f"Immagine generata con successo: {file_name}")
        return file_name
    except Exception as e:
        print(f"Errore durante la generazione dell'immagine con DALL·E: {e}")
        return None

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

    elif "genera immagine" in command:
        dalle_prompt = input("Descrivi cosa vuoi generare con DALL·E: ")
        generated_image = generate_image_with_dalle(dalle_prompt)
        if generated_image:
            upload_image(repo, generated_image, "Caricata immagine generata con DALL·E")
            add_to_html = input("Vuoi aggiungere questa immagine a un file HTML? (sì/no): ").lower()
            if add_to_html == "sì":
                html_file = input("Inserisci il nome del file HTML (es. index.html): ")
                add_image_to_html(repo, html_file, os.path.basename(generated_image))

    else:
        print("Comando non riconosciuto. Prova con 'crea pagina', 'aggiungi voce menu', 'carica immagine' o 'genera immagine'.")

# Inizia il processo
def main():
    # Recupera il token GitHub
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("Errore: GITHUB_TOKEN non trovato. Assicurati di aver configurato il secret correttamente.")

    # Connessione a GitHub
    g = Github(token)

    # Nome del repository
    repo_name = "frescodicredito/frescodicredito.github.io"
    repo = g.get_repo(repo_name)

    # Chiedi il comando all'utente
    print("Esempi di comandi:")
    print("- 'Crea pagina'")
    print("- 'Aggiungi voce menu'")
    print("- 'Carica immagine'")
    print("- 'Genera immagine'")
    command = input("Inserisci il comando da eseguire: ").lower()

    # Esegui il comando
    process_command(command, repo)

if __name__ == "__main__":
    main()
