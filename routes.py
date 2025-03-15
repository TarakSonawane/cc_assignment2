from flask import Blueprint, request, jsonify
from models import Product, db
from utils import upload_to_blob

product_routes = Blueprint('products', __name__)

@product_routes.route('/add', methods=['POST'])
def add_product():
    data = request.form
    image = request.files['image']
    
    image_url = upload_to_blob(image) if image else None

    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=float(data['price']),
        currency=data.get('currency', 'USD'),
        image_url=image_url
    )

    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

@product_routes.route('/list', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "currency": p.currency,
        "image_url": p.image_url
    } for p in products])

@product_routes.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"})
