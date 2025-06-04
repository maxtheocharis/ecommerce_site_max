// src/components/ProductList.jsx
import React from "react";
import { Link } from "react-router-dom";
import { addToCart } from "../api";

export default function ProductList({ products }) {
  return (
    <div className="row">
      {products.map((p) => (
        <div key={p.id} className="col-md-4 mb-4">
          <div className="card">
            <img
              src={p.image}
              className="card-img-top"
              alt={p.name}
              style={{ height: 200, objectFit: "cover" }}
            />
            <div className="card-body">
              <h5 className="card-title">{p.name}</h5>
              <p className="card-text">${p.price.toFixed(2)}</p>
              <Link
                to={`/product/${p.id}`}
                className="btn btn-outline-secondary btn-sm me-2"
              >
                View
              </Link>
              <button
                className="btn btn-sm btn-primary"
                onClick={async () => {
                  try {
                    await addToCart(p.id, 1);
                    alert("Added to cart!");
                  } catch (err) {
                    console.error("Add to cart failed:", err);
                    alert("Error adding to cart");
                  }
                }}
              >
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
