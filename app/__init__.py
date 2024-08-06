from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set the secret key

from app import routes