// src/App.js
import React, { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

import Navbar from "./components/Navbar";
import ProductList from "./components/ProductList";
import ProductDetail from "./components/ProductDetail";
import CartPage from "./components/CartPage";
import CheckoutPage from "./components/CheckoutPage";

import { fetchProducts } from "./api";

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    async function loadAllProducts() {
      try {
        const data = await fetchProducts();
        setProducts(data);
      } catch (err) {
        console.error("Failed to load products:", err);
      }
    }
    loadAllProducts();
  }, []);

  return (
    <BrowserRouter>
      <Navbar />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<ProductList products={products} />} />
          <Route path="/product/:id" element={<ProductDetail />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
