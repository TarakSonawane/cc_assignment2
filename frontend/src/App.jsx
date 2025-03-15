import React, { useState, useEffect } from "react";
import ProductList from "./components/ProductList";
import AddProduct from "./components/AddProduct";
import SearchBar from "./components/SearchBar";
import { fetchProducts } from "./api";

const App = () => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]); // Search results
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    setLoading(true);
    const data = await fetchProducts();
    setProducts(data);
    setFilteredProducts(data); // Initialize search results with all products
    setLoading(false);
  };

  const handleSearch = async (query) => {
    if (query.trim() === "") {
      setFilteredProducts(products); // Reset search results when query is empty
    } else {
      const results = products.filter((product) =>
        product.name.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredProducts(results);
    }
  };

  

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">Product Catalogue</h1>
      <SearchBar onSearch={handleSearch} />
      <AddProduct onProductAdded={loadProducts} />
      {loading ? (
        <p className="text-center text-gray-600 mt-4">Loading...</p>
      ) : (
        <ProductList products={filteredProducts} onDelete={loadProducts} />
      )}
    </div>
  );
};

export default App;
