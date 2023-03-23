from flask import render_template
from models import db, Product

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)
