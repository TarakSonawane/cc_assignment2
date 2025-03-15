from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import urllib
import os
from azure.storage.blob import BlobServiceClient
from werkzeug.utils import secure_filename
from sqlalchemy import text  # Import text function

app = Flask(__name__)
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Fetch the Azure Storage connection string from the environment
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError("❌ AZURE_STORAGE_CONNECTION_STRING is not set! Check .env file.")

print("✅ AZURE_STORAGE_CONNECTION_STRING Loaded Successfully")

# Enable CORS for frontend (localhost:3000)
CORS(app, resources={r"/*": {"origins": "*"}})

# Define database connection parameters
db_params = urllib.parse.quote_plus(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:productcatalouge.database.windows.net,1433;"
    "Database=product_catalouge_A2;"
    "Uid=adminn;"
    "Pwd=Guitar@tarak13;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Set up SQLAlchemy URI
app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={db_params}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Azure Blob Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = "product-images"
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

# Create tables if they don’t exist
with app.app_context():
    db.create_all()

# Test database connection
with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))  # Ensure text() is used correctly
        print("✅ Database connection successful")
    except Exception as e:
        print("❌ Database connection failed:", str(e))


# Route to add a product
@app.route("/products", methods=["POST"])
def add_product():
    try:
        print("🔹 Request Data:", request.form)
        print("🔹 Files:", request.files)

        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        file = request.files.get("image")

        if not name or not price:
            return jsonify({"error": "Name and price are required"}), 400

        image_url = None
        if file:
            filename = secure_filename(file.filename)
            blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=filename)
            blob_client.upload_blob(file, overwrite=True)
            image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{filename}"

        new_product = Product(name=name, price=float(price), description=description, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product added successfully"}), 201
    except Exception as e:
        print("❌ Error adding product:", str(e))  # Print error for debugging
        return jsonify({"error": "Failed to add product", "details": str(e)}), 500


# Route to get all products
@app.route("/products", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "description": p.description,
                "image_url": p.image_url if p.image_url else ""
            } for p in products
        ])
    except Exception as e:
        print("❌ Error fetching products:", str(e))
        return jsonify({"error": "Failed to fetch products", "details": str(e)}), 500


# Route to delete a product (with image deletion)
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Delete image from Azure Blob Storage if exists
        if product.image_url:
            blob_name = product.image_url.split("/")[-1]
            blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_name)
            blob_client.delete_blob()

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        print("❌ Error deleting product:", str(e))
        return jsonify({"error": "Failed to delete product", "details": str(e)}), 500


# Route to delete all products (CAUTION: This will wipe all data)
@app.route("/products/delete_all", methods=["DELETE"])
def delete_all_products():
    try:
        num_deleted = db.session.query(Product).delete()
        db.session.commit()
        return jsonify({"message": f"Deleted {num_deleted} products"}), 200
    except Exception as e:
        print("❌ Error deleting all products:", str(e))
        return jsonify({"error": "Failed to delete all products", "details": str(e)}), 500


# Search Route (Real-time search)
@app.route("/products/search", methods=["GET"])
def search_products():
    try:
        query = request.args.get("q", "").strip()
        if not query:
            return get_products()

        products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "description": p.description,
                "image_url": p.image_url if p.image_url else ""
            } for p in products
        ])
    except Exception as e:
        print("❌ Error searching products:", str(e))
        return jsonify({"error": "Failed to search products", "details": str(e)}), 500


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
