from flask import Flask
from app.routes.chatbot import chatbot_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.register_blueprint(chatbot_bp, url_prefix="/api")

    return app
