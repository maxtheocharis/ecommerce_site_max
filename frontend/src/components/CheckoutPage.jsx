// src/components/CheckoutPage.jsx
import React, { useEffect, useState } from "react";
import { fetchCart } from "../api";
import { useNavigate } from "react-router-dom";

export default function CheckoutPage() {
  const [cart, setCart] = useState({ items: [] });
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function loadCart() {
      try {
        const data = await fetchCart();
        setCart(data);
      } catch (err) {
        console.error("Failed to load cart:", err);
      } finally {
        setLoading(false);
      }
    }
    loadCart();
  }, []);

  if (loading) return <p>Loading…</p>;

  // Compute total on the client:
  const total = cart.items.reduce(
    (sum, ci) => sum + ci.product.price * ci.quantity,
    0
  );

  const handleConfirmOrder = () => {
    // In a real app you would POST to /api/orders/ here.
    // For now, just show a thank‐you page or redirect:
    alert("Order confirmed! Thank you for shopping.");
    navigate("/");
  };

  return (
    <div>
      <h1>Checkout</h1>

      {cart.items.length > 0 ? (
        <>
          <table className="table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Unit Price</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              {cart.items.map((ci) => (
                <tr key={ci.id}>
                  <td>{ci.product.name}</td>
                  <td>{ci.quantity}</td>
                  <td>${ci.product.price.toFixed(2)}</td>
                  <td>${(ci.product.price * ci.quantity).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr>
                <th colSpan="3" className="text-end">
                  Total:
                </th>
                <th>${total.toFixed(2)}</th>
              </tr>
            </tfoot>
          </table>

          <button
            className="btn btn-success"
            onClick={handleConfirmOrder}
          >
            Confirm Order
          </button>
        </>
      ) : (
        <p>Your cart is empty.</p>
      )}
    </div>
  );
}
