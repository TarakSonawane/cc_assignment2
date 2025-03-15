import React, { useState, useEffect } from "react";
import { fetchProducts, searchProducts } from "../api";
import ProductList from "./ProductList";
import SearchBar from "./SearchBar";
import AddProduct from "./AddProduct";

const ProductPage = () => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    setLoading(true);
    const allProducts = await fetchProducts();
    setProducts(allProducts);
    setFilteredProducts(allProducts);
    setLoading(false);
  };

  const handleSearch = async (query) => {
    if (query.trim() === "") {
      setFilteredProducts(products);
    } else {
      const results = await searchProducts(query);
      setFilteredProducts(results.length ? results : []);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">Product Catalogue</h1>
      <AddProduct onProductAdded={loadProducts} />
      <SearchBar onSearch={handleSearch} />
      {loading ? (
        <p className="text-center text-gray-600 mt-4">Loading...</p>
      ) : (
        <ProductList products={filteredProducts} onDelete={loadProducts} />
      )}
    </div>
  );
};

export default ProductPage;
