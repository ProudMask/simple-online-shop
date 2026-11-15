"""Local account and product-catalog demonstration."""
import hmac
import os
from pathlib import Path
import secrets
from flask import Flask, abort, request, session
from models import db, Category, Product


def create_app(config=None):
    # Existing HTML files intentionally stay in the repository root.
    app = Flask(__name__, template_folder='.')
    app.config.update(SECRET_KEY=os.getenv('SECRET_KEY') or secrets.token_hex(32), SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///shop_demo.sqlite3'), SQLALCHEMY_TRACK_MODIFICATIONS=False, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', MAX_CONTENT_LENGTH=16384)
    if config:
        app.config.update(config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    from auth import auth
    from views import shop
    app.register_blueprint(auth)
    app.register_blueprint(shop)

    @app.before_request
    def protect_forms():
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_hex(32)
        if request.method == 'POST' and not hmac.compare_digest(request.form.get('csrf_token', '').encode(), session['csrf_token'].encode()):
            abort(400, 'Invalid form token. Reload the page.')

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        print('Database tables ready.')

    @app.cli.command('seed-demo')
    def seed_demo():
        db.create_all()
        category = db.session.execute(db.select(Category).filter_by(name='Demo Abayas')).scalar_one_or_none()
        if category is None:
            category = Category(name='Demo Abayas')
            db.session.add(category)
            db.session.flush()
        for name, price in [('Demo Classic Abaya', '180.00'), ('Demo Everyday Abaya', '150.00')]:
            if db.session.execute(db.select(Product).filter_by(name=name, category_id=category.id)).scalar_one_or_none() is None:
                db.session.add(Product(name=name, description='Synthetic catalog item for demonstration.', price=price, category_id=category.id))
        db.session.commit()
        print('Two synthetic demo products ready; no accounts were created.')

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
