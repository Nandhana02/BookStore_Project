from flask import Flask
from config import Config
from extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints (later we will add routes)
    from blueprints.auth import auth_bp
    from blueprints.user import user_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    return app

def seed_books(app):
    from extensions import db
    from models.book import Book

    with app.app_context():
        if Book.query.first():
            return  # Books already exist, do nothing

        sample_books = [
            Book(
                title="Flask for Beginners",
                author="John Doe",
                category="Programming",
                price=10.0,
                quantity=10,
                description="Introduction to Flask framework."
            ),
            Book(
                title="Python Crash Course",
                author="Eric Matthes",
                category="Programming",
                price=25.0,
                quantity=8,
                description="Hands-on introduction to Python."
            ),
            Book(
                title="Clean Code",
                author="Robert C. Martin",
                category="Software Engineering",
                price=30.0,
                quantity=5,
                description="Best practices for writing clean code."
            ),
            Book(
                title="Design Patterns",
                author="Erich Gamma",
                category="Software Engineering",
                price=35.0,
                quantity=6,
                description="Classic design patterns explained."
            ),
            Book(
                title="Data Structures in Python",
                author="Mark Allen Weiss",
                category="Computer Science",
                price=28.0,
                quantity=7,
                description="Efficient data structures using Python."
            ),
            Book(
                title="Machine Learning Basics",
                author="Andrew Ng",
                category="AI & ML",
                price=40.0,
                quantity=4,
                description="Fundamentals of machine learning."
            ),
            Book(
                title="Deep Learning with Python",
                author="François Chollet",
                category="AI & ML",
                price=45.0,
                quantity=3,
                description="Deep learning using Keras."
            ),
            Book(
                title="Database System Concepts",
                author="Silberschatz",
                category="Databases",
                price=38.0,
                quantity=6,
                description="Core database concepts."
            ),
            Book(
                title="Operating System Concepts",
                author="Abraham Silberschatz",
                category="Operating Systems",
                price=42.0,
                quantity=5,
                description="Processes, memory, and scheduling."
            ),
            Book(
                title="Computer Networks",
                author="Andrew S. Tanenbaum",
                category="Networking",
                price=33.0,
                quantity=6,
                description="Networking fundamentals."
            ),
        ]

        db.session.bulk_save_objects(sample_books)
        db.session.commit()



app = create_app()
seed_books(app)

if __name__ == "__main__":
    app.run(debug=True)
