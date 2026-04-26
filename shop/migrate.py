import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.app import create_app

app = create_app()

with app.app_context():
    from app.models import db
    db.create_all()
    print("Database tables created successfully.")