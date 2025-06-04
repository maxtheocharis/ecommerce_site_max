// src/components/CartPage.jsx
import React, { useEffect, useState } from "react";
import { fetchCart, updateCartItem } from "../api";
import { Link, useNavigate } from "react-router-dom";

export default function CartPage() {
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

  const handleUpdate = async (itemId, newQty) => {
    try {
      await updateCartItem(itemId, newQty);
      const refreshed = await fetchCart();
      setCart(refreshed);
    } catch (err) {
      console.error("Update cart item failed:", err);
    }
  };

  const total = cart.items.reduce(
    (sum, ci) => sum + ci.product.price * ci.quantity,
    0
  );

  return (
    <div>
      <h1>Your Cart</h1>
      {cart.items.length ? (
        <>
          <table className="table align-middle">
            <thead>
              <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Unit Price</th>
                <th>Subtotal</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {cart.items.map((ci) => (
                <tr key={ci.id}>
                  <td>{ci.product.name}</td>
                  <td>
                    <input
                      type="number"
                      min="0"
                      value={ci.quantity}
                      onChange={(e) =>
                        handleUpdate(ci.id, parseInt(e.target.value, 10))
                      }
                      style={{ width: "3rem" }}
                    />
                  </td>
                  <td>${ci.product.price.toFixed(2)}</td>
                  <td>${(ci.product.price * ci.quantity).toFixed(2)}</td>
                  <td>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleUpdate(ci.id, 0)}
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
            <tfoot>
              <tr>
                <th colSpan="3" className="text-end">
                  Total:
                </th>
                <th>${total.toFixed(2)}</th>
                <th></th>
              </tr>
            </tfoot>
          </table>
          <button
            className="btn btn-success me-2"
            onClick={() => navigate("/checkout")}
          >
            Proceed to Checkout
          </button>
          <Link to="/" className="btn btn-secondary">
            Continue Shopping
          </Link>
        </>
      ) : (
        <p>
          Your cart is empty. <Link to="/">Browse products</Link>.
        </p>
      )}
    </div>
  );
}
