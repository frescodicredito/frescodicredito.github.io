import os
from flask import Flask, request, jsonify
from github import Github

app = Flask(__name__)

# Configura il token GitHub
import os

# Debug temporaneo per verificare il token
token = os.getenv("MY_GITHUB_TOKEN")
if not token:
    raise ValueError("Errore: MY_GITHUB_TOKEN non trovato.")
else:
    print(f"Token caricato: {token[:5]}... (troncato per sicurezza)")


g = Github(token)
repo_name = "frescodicredito/frescodicredito.github.io"
repo = g.get_repo(repo_name)

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('file_path')
    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/update', methods=['POST'])
def update_file():
    data = request.json
    file_path = data.get('file_path')
    new_content = data.get('new_content')
    commit_message = data.get('commit_message')
    try:
        file = repo.get_contents(file_path)
        repo.update_file(file.path, commit_message, new_content, file.sha, branch="main")
        return jsonify({"message": f"File '{file_path}' aggiornato con successo."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/create', methods=['POST'])
def create_file():
    data = request.json
    file_path = data.get('file_path')
    content = data.get('content')
    commit_message = data.get('commit_message')
    try:
        repo.create_file(file_path, commit_message, content, branch="main")
        return jsonify({"message": f"File '{file_path}' creato con successo."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa la porta specificata da Railway o 5000 come fallback
    app.run(debug=True, host='0.0.0.0', port=port)
