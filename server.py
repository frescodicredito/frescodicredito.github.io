from flask import Flask, jsonify, request
import os
from github import Github

app = Flask(__name__)

# Carica il token GitHub dalla variabile d'ambiente
MY_GITHUB_TOKEN = os.environ.get("MY_GITHUB_TOKEN")
if not MY_GITHUB_TOKEN:
    raise Exception("GitHub token non configurato correttamente")

# Inizializza l'oggetto GitHub
g = Github(MY_GITHUB_TOKEN)

@app.route('/read_repo', methods=['GET'])
def read_repo():
    """Leggi il contenuto della repository"""
    repo_name = request.args.get('repo_name')
    if not repo_name:
        return jsonify({"error": "Specifica il nome della repository"}), 400

    try:
        repo = g.get_repo(repo_name)
        contents = repo.get_contents("")
        repo_structure = []

        # Ricorsivamente ottieni il contenuto della repo
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            repo_structure.append({
                "name": file_content.name,
                "path": file_content.path,
                "type": file_content.type
            })

        return jsonify(repo_structure)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
