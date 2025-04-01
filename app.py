import re
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
from chat import get_response, get_text_from_speech
from scrape import login_and_get_data
import re, zipfile, os, tempfile
import uuid
from dotenv import load_dotenv
from google import generativeai as genai
import markdown
import bleach
from playwright.sync_api import sync_playwright
import pandas as pd
import time

app = Flask(__name__)
CORS(app)

# Disable Flask's reloader from monitoring certain file types
app.config['TEMPLATES_AUTO_RELOAD'] = False

load_dotenv()
key = os.getenv("gemini")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/")
def index_get():
    return render_template("website2.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        message = data.get("message")
        tts_flag = data.get("tts", False)

        if not message:
            raise ValueError("Invalid or missing 'message' in the request JSON.")
        
        # Attendance and assignments retrieval
        # Check if message matches credential pattern
        pattern = r"^\d{4}, .*$"
        if bool(re.match(pattern, message)):
            username, password = message.split(', ')
            login_result = login_and_get_data(username, password)
            
            if login_result == True:
                # Return a message to indicate files are ready for download
                session_id = str(uuid.uuid4())
                
                download_url = f"/download/{session_id}"
                return jsonify({
                    "answer": "Files are ready for download. Click <a href='" + download_url + "'>here</a> to download.",
                    "download_url": download_url
                })
            else:
                return jsonify({"answer": "Invalid username or password"})
        
        # Handle regular message responses
        elif "attendance" in message.lower() or "assignment" in message.lower():
            response = {"answer": "Enter your etlab username and password separated by a ',' "}
        else:
            result = get_response(message)
            # Fallback gemini AI
            if result == "I do not understand":
                
                response = model.generate_content(message)
                api_response = response.text
                html_content = markdown.markdown(api_response, extensions=['extra', 'codehilite', 'tables'])
                allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li', 'strong', 'em', 'code', 'pre', 'blockquote', 'br','table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr']
                allowed_attrs = {'a': ['href', 'title', 'target'], 'code': ['class'], 'pre': ['class']}
    
                clean_html = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attrs, strip=True)
                response = {"answer": clean_html}
                
            else:
                response = {"answer": result}
            
        return jsonify(response)

    except Exception as e:
        error_message = {"error": str(e)}
        return jsonify(error_message), 400

@app.route("/download/<session_id>", methods=["GET"])
def download_files(session_id):
    try:
        # Create zip file with the data
        attendance_file_path = "attendance_data.csv"
        assignment_file_path = "assignment_data.csv"
        internal_file_path = "internal_data.csv"
        zip_file = "data_files.zip"
        
        with zipfile.ZipFile(zip_file, "w") as zipf:
            zipf.write(attendance_file_path, os.path.basename(attendance_file_path))
            zipf.write(assignment_file_path, os.path.basename(assignment_file_path))
            zipf.write(internal_file_path, os.path.basename(internal_file_path))

        return send_file(zip_file, as_attachment=True, download_name="data_files.zip", max_age=0)
        
    except FileNotFoundError:
        return jsonify({"error": "Files not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == "__main__":
    TEMP_DIR = tempfile.gettempdir()
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Add this to prevent reloading for zip files
    extra_files = [
        file for file in os.listdir('.')
        if not file.endswith('.zip') and os.path.isfile(file)
    ]
    
    app.run(debug=False, extra_files=extra_files)