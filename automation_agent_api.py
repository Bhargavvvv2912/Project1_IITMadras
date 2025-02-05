import os
import subprocess
import requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Environment Variables
USER_EMAIL = os.getenv("USER_EMAIL", "21f1006473@ds.study.iitm.ac.in")
DATAGEN_URL = os.getenv("DATAGEN_URL", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py")
DATAGEN_SCRIPT = "datagen.py"
PORT = int(os.getenv("PORT", 8000))

def ensure_uv_installed():
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        subprocess.run(["pip", "install", "uv"], check=True)

def download_and_run_datagen():
    response = requests.get(DATAGEN_URL)
    if response.status_code == 200:
        with open(DATAGEN_SCRIPT, "w") as f:
            f.write(response.text)
        subprocess.run(["python", DATAGEN_SCRIPT, USER_EMAIL], check=True)
        return True
    return False

@app.route("/run", methods=["POST"])
def run_task():
    task = request.args.get("task")
    if not task:
        return jsonify({"error": "Missing task description"}), 400
    
    if "install uv" in task.lower() or "run datagen.py" in task.lower():
        ensure_uv_installed()
        success = download_and_run_datagen()
        if success:
            return jsonify({"message": "datagen.py executed successfully"}), 200
        else:
            return jsonify({"error": "Failed to download datagen.py"}), 500
    
    return jsonify({"error": "Task not recognized"}), 400

@app.route("/read", methods=["GET"])
def read_file():
    file_path = request.args.get("path")
    if not file_path or not os.path.exists(file_path):
        return "", 404
    return send_file(file_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
