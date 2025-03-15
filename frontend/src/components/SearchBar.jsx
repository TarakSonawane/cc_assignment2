import React, { useState } from "react";

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleInputChange = (event) => {
    const newQuery = event.target.value;
    setQuery(newQuery);
    if (onSearch) {
      onSearch(newQuery); // Call onSearch on every change
    }
  };

  return (
    <div className="mb-4">
      <input
        type="text"
        value={query}
        onChange={handleInputChange} // Live search on change
        placeholder="Search products..."
        className="border p-2 rounded w-full"
      />
    </div>
  );
};

export default SearchBar;
