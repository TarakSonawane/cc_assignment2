// src/api.js
const API_URL = "http://127.0.0.1:5000"; // Change this if your backend URL is different

// Fetch all products
export const fetchProducts = async () => {
  try {
    const response = await fetch(`${API_URL}/products`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching products:", error);
    return [];
  }
};

// Add a new product (💡 This function was missing)
export const addProduct = async (product) => {
  const formData = new FormData();
  formData.append("name", product.name);
  formData.append("price", product.price);
  formData.append("description", product.description);
  if (product.image) {
    formData.append("image", product.image);
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/products", {
      method: "POST",
      body: formData,
    });

    const data = await response.json(); // Ensure response is processed
    return { success: response.ok, data };
  } catch (error) {
    console.error("Error adding product:", error);
    return { success: false };
  }
};



// Delete a product
export const deleteProduct = async (id) => {
  try {
    const response = await fetch(`${API_URL}/products/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      console.error("Error deleting product:", await response.text());
      return { success: false };
    }

    return { success: true };
  } catch (error) {
    console.error("Error deleting product:", error);
    return { success: false };
  }
};



