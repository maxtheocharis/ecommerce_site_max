// src/components/ProductDetail.jsx
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchProductById, addToCart } from "../api";

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadOne() {
      try {
        const data = await fetchProductById(id);
        setProduct(data);
      } catch (err) {
        console.error("Failed to load product:", err);
      } finally {
        setLoading(false);
      }
    }
    loadOne();
  }, [id]);

  if (loading) return <p>Loading…</p>;
  if (!product) return <p>Product not found.</p>;

  return (
    <div className="row">
      <div className="col-md-6">
        <img
          src={product.image}
          alt={product.name}
          className="img-fluid"
          style={{ objectFit: "cover", height: 400, width: "100%" }}
        />
      </div>
      <div className="col-md-6">
        <h1>{product.name}</h1>
        <p className="lead">${product.price.toFixed(2)}</p>
        <p>{product.description}</p>
        <button
          className="btn btn-primary"
          onClick={async () => {
            try {
              await addToCart(product.id, 1);
              alert("Added to cart!");
            } catch (err) {
              console.error("Add to cart failed:", err);
              alert("Error adding to cart");
            }
          }}
        >
          Add to Cart
        </button>
        <Link to="/" className="btn btn-outline-secondary ms-2">
          ← Back to Catalog
        </Link>
      </div>
    </div>
  );
}
