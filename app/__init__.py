from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Initialize extensions
mongo = PyMongo()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure MongoDB
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    # Test connection immediately
    with app.app_context():
        try:
            # Verify both server and database access
            mongo.db.command('ping')
            print("✅ MongoDB Atlas connection successful!")
            print(f"Connected to database: {mongo.db.name}")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {type(e).__name__}: {str(e)}")
            print("Verify:")
            print("1. Internet connection")
            print("2. IP is whitelisted in Atlas")
            print("3. Credentials in .env are correct")
    
    # Register blueprints
    from .routes import bp as submissions_bp
    app.register_blueprint(submissions_bp)
    
    return app