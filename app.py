import os
import json
import subprocess
from flask import Flask, render_template, request, jsonify, Response, send_from_directory

app = Flask(__name__, static_folder=None)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
LOG_FILE = os.path.join(BASE_DIR, "scraper.log")
SCRAPER_SCRIPT = os.path.join(BASE_DIR, "daily_scraper.py")
VENV_PYTHON = os.path.join(BASE_DIR, ".venv", "bin", "python")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tracker_data.js')
def serve_tracker_data():
    return send_from_directory(BASE_DIR, 'tracker_data.js')

@app.route('/search_links.html')
def serve_search_links():
    return send_from_directory(BASE_DIR, 'search_links.html')

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    if request.method == 'POST':
        data = request.json
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "success"})
    
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/api/scrape', methods=['POST'])
def start_scrape():
    # Clear the log file so we start fresh for SSE
    if os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
        
    # Start the scraper in the background
    subprocess.Popen([VENV_PYTHON, SCRAPER_SCRIPT])
    return jsonify({"status": "started"})

@app.route('/api/progress')
def progress():
    def generate():
        # Stream the log file as SSE
        # We'll read the log file, and look for % PROGRESS lines
        if not os.path.exists(LOG_FILE):
            open(LOG_FILE, 'w').close()
            
        with open(LOG_FILE, 'r') as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    import time
                    time.sleep(0.5)
                    continue
                
                # Check for progress percentage emitted by daily_scraper.py
                # Format: [PROGRESS] 50% - Scraping Airbnb
                if "[PROGRESS]" in line:
                    yield f"data: {line}\n\n"
                    if "100%" in line:
                        break
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
