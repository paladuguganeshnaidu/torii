from flask import Flask, request, jsonify, send_from_directory, Response, render_template
from database import init_db
import os
import json

# Import tool functions
from tools.email_analyzer import analyze_email_tool
from tools.url_scanner import scan_url_tool
from tools.password_cracker import crack_hash_tool
from tools.sms_spam_detector import test_sms_tool
from tools.malware_analyzer import analyze_file_tool
from tools.web_recon import recon_target_tool
try:
    import importlib
    _flask_cors = importlib.import_module('flask_cors')
    CORS = getattr(_flask_cors, 'CORS')
except Exception:
    # Fallback no-op CORS for environments where flask_cors isn't installed (prevents import errors)
    def CORS(app, resources=None):
        return app
import importlib.util
import pathlib
from auth import auth_bp
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_folder='../frontend')
# Enable CORS for API routes (dev convenience; restrict in production)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = os.environ.get('TORII_SECRET', 'dev-secret')
app.register_blueprint(auth_bp, url_prefix='/auth')

# Logging configuration with rotation
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, 'app.log')
handler = RotatingFileHandler(LOG_PATH, maxBytes=1_000_000, backupCount=5)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def _log_request():
    try:
        app.logger.info('REQ %s %s', request.method, request.path)
    except Exception:
        pass

# Initialize database
init_db()

@app.route('/')
def index():
    return render_template('index.html', current_tool=None, tool_title='Welcome', tool_description='Select a tool')


@app.route('/tool/<tool_name>', methods=['GET', 'POST'])
def tool_page(tool_name):
    # Map tool_name to functions and metadata
    mapping = {
        'email': (analyze_email_tool, 'Email Analyzer', 'Upload .eml files for analysis'),
        'url': (scan_url_tool, 'URL Scanner', 'Scan one or more URLs'),
        'pass': (crack_hash_tool, 'Password Cracker', 'Attempt to crack a hash'),
        'sms': (test_sms_tool, 'SMS Spam Tester', 'Test message text for spam likelihood'),
        'malware': (analyze_file_tool, 'Malware Analyzer', 'Upload files for scanning'),
        'recon': (recon_target_tool, 'Web Recon', 'Recon target domains and hosts')
    }
    if tool_name not in mapping:
        return render_template('index.html', current_tool=None, tool_title='Not found', tool_description='Tool not found', result={'error': 'tool not found'})

    func, title, desc = mapping[tool_name]
    result = None
    if request.method == 'POST':
        try:
            result = func(request)
        except Exception as e:
            result = {'error': str(e)}

    return render_template('index.html', current_tool=tool_name, tool_title=title, tool_description=desc, result=result)


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

# API Endpoints
@app.route('/api/analyze_email', methods=['POST'])
def analyze_email_api():
    result = analyze_email_tool(request)
    # Return HTML so iframe can show it when forms target the iframe
    return Response('<pre>{}</pre>'.format(json.dumps(result, indent=2)), mimetype='text/html')

@app.route('/api/scan_url', methods=['POST'])
def scan_url_api():
    result = scan_url_tool(request)
    return Response('<pre>{}</pre>'.format(json.dumps(result, indent=2)), mimetype='text/html')

@app.route('/api/crack_hash', methods=['POST'])
def crack_hash_api():
    result = crack_hash_tool(request)
    return Response('<pre>{}</pre>'.format(json.dumps(result, indent=2)), mimetype='text/html')

@app.route('/api/test_sms', methods=['POST'])
def test_sms_api():
    result = test_sms_tool(request)
    return Response('<pre>{}</pre>'.format(json.dumps(result, indent=2)), mimetype='text/html')

@app.route('/api/analyze_file', methods=['POST'])
def analyze_file_api():
    result = analyze_file_tool(request)
    return Response('<pre>{}</pre>'.format(json.dumps(result, indent=2)), mimetype='text/html')

@app.route('/api/recon_target', methods=['POST'])
def recon_target_api():
    result = recon_target_tool(request)
    return Response('<pre>{}</pre>'.format(json.dumps(result, indent=2)), mimetype='text/html')

# Steganography API (module filename has hyphen, so import dynamically)
@app.route('/api/detect_stego', methods=['POST'])
def detect_stego_api():
    try:
        tools_dir = pathlib.Path(__file__).parent / 'tools'
        mod_path = tools_dir / 'stenography-checker.py'
        spec = importlib.util.spec_from_file_location('stego_mod', str(mod_path))
        stego_mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader, 'Cannot load steganography module'
        spec.loader.exec_module(stego_mod)
        result = stego_mod.detect_stego_tool(request)
    except Exception as e:
        result = {'error': str(e)}
    return Response('<pre>{}</pre>'.format(json.dumps(result, indent=2)), mimetype='text/html')

if __name__ == '__main__':
    app.run(debug=True)