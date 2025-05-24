from flask import Flask

app = Flask(__name__, static_folder='static')

# Import routes after app is created to avoid circular imports
from app import routes
