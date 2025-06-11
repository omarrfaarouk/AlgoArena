from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb+srv://omarrfaarouk:K4hVgre9qTOW795V@cluster0.yuivpin.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    mongo.init_app(app)
    
    from . import routes
    app.register_blueprint(routes.bp)
    
    with app.app_context():
        try:
            mongo.db.command('ping')
            print("✅ Successfully connected to Atlas!")
        except Exception as e:
            print("❌ Atlas connection failed:", e)
    
    
    return app