import React from "react";
import { deleteProduct } from "../api";

const ProductList = ({ products, onDelete }) => {
  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this product?")) {
      const response = await deleteProduct(id);
      if (response.success) {
        onDelete(); // Refresh product list
      } else {
        alert("Failed to delete product.");
      }
    }
  };

  

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
      {products.map((product) => (
        <div key={product.id} className="bg-white p-4 rounded-lg shadow-md">
          {product.image_url && (
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-32 object-cover rounded-md"
            />
          )}
          <h3 className="text-lg font-bold mt-2">{product.name}</h3>
          <p className="text-gray-700">₹{product.price}</p>
          <p className="text-sm text-gray-500">{product.description}</p>
          <button
            className="bg-red-500 text-white px-3 py-1 mt-2 rounded hover:bg-red-600"
            onClick={() => handleDelete(product.id)}
          >
            Delete
          </button>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
