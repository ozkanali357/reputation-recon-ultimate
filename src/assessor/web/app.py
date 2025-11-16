from flask import Flask
from flask_cors import CORS
from assessor.web.api import api

app = Flask(__name__)
CORS(app)  # Enable React frontend

# Register API blueprint
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)