from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return ("Welcome to the application!", 200)

@app.route('/health', methods=['GET'])
def health():
    return ("OK", 200)

@app.route('/info', methods=['GET'])
def info():
    import os
    import socket
    hostname= socket.gethostname()
    env = os.getenv('FLASK_ENV', 'development')
    return (f"Version: 1.0.0, Hostname: {hostname}, Environment: {env}", 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
