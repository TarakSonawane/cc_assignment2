import React from "react";
import { deleteProduct } from "../api";

const ProductItem = ({ product, onDelete }) => {
  const handleDelete = async () => {
    await deleteProduct(product.id);
    onDelete();
  };

  return (
    <div className="p-2 border rounded mb-2 flex justify-between">
      <span>{product.name} - ${product.price}</span>
      <button onClick={handleDelete} className="bg-red-500 text-white p-1">
        Delete
      </button>
    </div>
  );
};

export default ProductItem;
