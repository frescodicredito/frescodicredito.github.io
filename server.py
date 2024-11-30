import os
from flask import Flask, request, jsonify
from github import Github
import smtplib

app = Flask(__name__)

# Debug temporaneo: stampiamo le variabili di ambiente disponibili
print("Variabili di ambiente disponibili:")
print(os.environ)

# Configura il token GitHub
token = os.getenv("MY_GITHUB_TOKEN")
if not token:
    raise ValueError("Errore: MY_GITHUB_TOKEN non trovato.")
else:
    print(f"Token caricato correttamente: {token[:5]}... (troncato per sicurezza)")

# Connessione a GitHub
try:
    g = Github(token)
    repo_name = "frescodicredito/frescodicredito.github.io"
    repo = g.get_repo(repo_name)
    print(f"Connesso al repository: {repo_name}")
except Exception as e:
    raise ValueError(f"Errore durante la connessione a GitHub: {e}")

@app.route('/', methods=['GET'])
def home():
    return "Server funzionante!"

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('file_path')
    try:
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": f"Errore durante la lettura del file: {str(e)}"}), 400

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
        return jsonify({"error": f"Errore durante l'aggiornamento del file: {str(e)}"}), 400

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
        return jsonify({"error": f"Errore durante la creazione del file: {str(e)}"}), 400

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return jsonify({"error": "Missing required fields"}), 400

    # Configurazione SMTP
    try:
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')  # Server SMTP (es. Gmail)
        smtp_port = int(os.environ.get('SMTP_PORT', 587))  # Porta SMTP (default 587)
        smtp_user = os.environ.get('SMTP_USER')  # Email mittente
        smtp_pass = os.environ.get('SMTP_PASS')  # Password/App password
        recipient_email = os.environ.get('RECIPIENT_EMAIL')  # Email destinatario

        if not all([smtp_user, smtp_pass, recipient_email]):
            return jsonify({"error": "SMTP configuration is missing"}), 500

        # Invia email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            email_message = f"Subject: New Contact Form Message\n\nFrom: {name} <{email}>\n\n{message}"
            server.sendmail(smtp_user, recipient_email, email_message)

        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Porta configurata per Railway
    port = int(os.environ.get('PORT', 5000))  # Usa la porta specificata da Railway o 5000 come fallback
    print(f"Server in esecuzione sulla porta {port}")
    app.run(debug=True, host='0.0.0.0', port=port)
