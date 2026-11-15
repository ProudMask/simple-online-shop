from flask import Blueprint, render_template
from models import db, Product

shop = Blueprint('shop', __name__)


@shop.get('/')
def index():
    products = db.session.execute(db.select(Product).order_by(Product.name, Product.id)).scalars().all()
    return render_template('index.html', products=products)
