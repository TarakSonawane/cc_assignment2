import React, { useState, useEffect } from "react";
import axios from "axios";
import ProductList from "../components/ProductList";
import ProductForm from "../components/ProductForm";

const API_URL = "backend-cc-tarak-c5bahfa3hngrdpbf.centralindia-01.azurewebsites.net/api/products";

function Home() {
  const [products, setProducts] = useState([]);
  const [editingProduct, setEditingProduct] = useState(null);
  
  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(API_URL);
      setProducts(response.data);
    } catch (error) {
      console.error("Error fetching products", error);
    }
  };

  const handleAddProduct = async (product) => {
    try {
      await axios.post(API_URL, product);
      fetchProducts();
    } catch (error) {
      console.error("Error adding product", error);
    }
  };

  const handleUpdateProduct = async (product) => {
    try {
      await axios.put(`${API_URL}/${product.id}`, product);
      fetchProducts();
      setEditingProduct(null);
    } catch (error) {
      console.error("Error updating product", error);
    }
  };

  const handleDeleteProduct = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchProducts();
    } catch (error) {
      console.error("Error deleting product", error);
    }
  };

  return (
    <div className="p-4">
      <ProductForm 
        onAddProduct={handleAddProduct} 
        onUpdateProduct={handleUpdateProduct} 
        editingProduct={editingProduct}
      />
      <ProductList 
        products={products} 
        onDelete={handleDeleteProduct} 
        onEdit={setEditingProduct} 
      />
    </div>
  );
}

export default Home;
