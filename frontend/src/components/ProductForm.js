import React, { useState, useEffect } from "react";

function ProductForm({ onAddProduct, onUpdateProduct, editingProduct }) {
  const [form, setForm] = useState({ name: "", price: "" });

  useEffect(() => {
    if (editingProduct) {
      setForm(editingProduct);
    }
  }, [editingProduct]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (editingProduct) {
      onUpdateProduct(form);
    } else {
      onAddProduct(form);
    }
    setForm({ name: "", price: "" });
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded mb-4">
      <h2 className="text-xl mb-2">{editingProduct ? "Edit Product" : "Add Product"}</h2>
      <input
        type="text"
        name="name"
        placeholder="Product Name"
        className="w-full p-2 border rounded mb-2"
        value={form.name}
        onChange={handleChange}
        required
      />
      <input
        type="number"
        name="price"
        placeholder="Price"
        className="w-full p-2 border rounded mb-2"
        value={form.price}
        onChange={handleChange}
        required
      />
      <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
        {editingProduct ? "Update" : "Add"}
      </button>
    </form>
  );
}

export default ProductForm;
