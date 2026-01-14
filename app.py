from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    app.logger.info("Home page requested")
    return ("Welcome to the application!", 200)

@app.route('/health', methods=['GET'])
def health():
    app.logger.info("Health check requested")
    return ("OK", 200)

@app.route('/info', methods=['GET'])
def info():
    import os
    import socket
    hostname= socket.gethostname()
    env = os.getenv('FLASK_ENV', 'development')
    app.logger.info("Info requested: hostname=%s, env=%s", hostname, env)
    return jsonify({'version' : "1.0.0", 'hostname': hostname, 'env': env })

@app.route('/visits', methods=['GET'])
def visits():
    app.logger.info("Visits page requested")
    from flask import render_template
    return render_template('visits.html')

@app.route('/src/<path:filename>', methods=['GET'])
def serve_static(filename):
    app.logger.info("Static file requested: %s", filename)
    from flask import send_from_directory
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
