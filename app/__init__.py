from flask import Flask
from config import Config

serverApplication = Flask(__name__)
serverApplication.config.from_object(Config)

from app import routes