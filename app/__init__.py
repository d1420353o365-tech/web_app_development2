import os
from flask import Flask
from dotenv import load_dotenv

from app.models import db

def create_app(test_config=None):
    # Load environment variables
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure Database and Secret Key
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'database.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize Plugins
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        # import models so metadata is known
        from app.models.user import User
        from app.models.note import Note
        from app.models.plan import Plan
        from app.models.quiz import Quiz, QuizQuestion, Mistake
        db.create_all()

    # Register Blueprints
    from app.routes import main, auth, note_routes, plan_routes, quiz_routes, chat_routes
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(note_routes.bp)
    app.register_blueprint(plan_routes.bp)
    app.register_blueprint(quiz_routes.bp)
    app.register_blueprint(chat_routes.bp)

    return app
