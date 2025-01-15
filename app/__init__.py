from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    
    app.config.from_object('app.configs.Config')
    app.json.sort_keys = False
    
    from .routes import api_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app