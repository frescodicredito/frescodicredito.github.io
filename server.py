import os
from flask import Flask, request, jsonify
from github import Github

app = Flask(__name__)

# Configura il token GitHub
token = os.getenv("MY_GITHUB_TOKEN")
if not token:
    raise ValueError("Errore: MY_GITHUB_TOKEN non trovato.")
else:
    print("MY_GITHUB_TOKEN caricato con successo.")

# Connessione al repository
repo_name = "frescodicredito/frescodicredito.github.io"
try:
    g = Github(token)
    repo = g.get_repo(repo_name)
    print(f"Connessione al repository '{repo_name}' effettuata con successo.")
except Exception as e:
    raise ValueError(f"Errore durante la connessione al repository '{repo_name}': {e}")

@app.route('/read', methods=['GET'])
def read_file():
    """Endpoint per leggere un file dal repository."""
    file_path = request.args.get('file_path')
    print(f"Tentativo di leggere il file '{file_path}'...")
    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode()
        print(f"File '{file_path}' letto con successo.")
        return jsonify({"content": content})
    except Exception as e:
        print(f"Errore durante la lettura del file '{file_path}': {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/update', methods=['POST'])
def update_file():
    """Endpoint per aggiornare un file esistente."""
    data = request.json
    file_path = data.get('file_path')
    new_content = data.get('new_content')
    commit_message = data.get('commit_message')
    print(f"Tentativo di aggiornare il file '{file_path}'...")
    try:
        file = repo.get_contents(file_path)
        repo.update_file(file.path, commit_message, new_content, file.sha, branch="main")
        print(f"File '{file_path}' aggiornato con successo.")
        return jsonify({"message": f"File '{file_path}' aggiornato con successo."})
    except Exception as e:
        print(f"Errore durante l'aggiornamento del file '{file_path}': {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/create', methods=['POST'])
def create_file():
    """Endpoint per creare un nuovo file."""
    data = request.json
    file_path = data.get('file_path')
    content = data.get('content')
    commit_message = data.get('commit_message')
    print(f"Tentativo di creare il file '{file_path}'...")
    try:
        repo.create_file(file_path, commit_message, content, branch="main")
        print(f"File '{file_path}' creato con successo.")
        return jsonify({"message": f"File '{file_path}' creato con successo."})
    except Exception as e:
        print(f"Errore durante la creazione del file '{file_path}': {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Configura l'host e la porta per Railway
    port = int(os.environ.get('PORT', 5000))  # Usa la porta specificata da Railway o 5000 come fallback
    print(f"Avvio del server Flask sulla porta {port}...")
    app.run(debug=True, host='0.0.0.0', port=port)
