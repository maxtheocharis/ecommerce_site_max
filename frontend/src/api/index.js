// src/api/index.js
import axios from "axios";
import Cookies from "js-cookie";

// Point this at wherever your Django‐DRF backend is running:
export const BASE_URL = "http://192.168.2.23:8000/api";

// Fetch the list of all products:
export async function fetchProducts() {
  const resp = await axios.get(`${BASE_URL}/products/`, {
    withCredentials: true,
  });
  return resp.data; 
}

// Fetch a single product by its ID:
export async function fetchProductById(id) {
  const resp = await axios.get(`${BASE_URL}/products/${id}/`, {
    withCredentials: true,
  });
  return resp.data;
}

// Fetch the current user’s cart (read‐only):
export async function fetchCart() {
  const resp = await axios.get(`${BASE_URL}/cart/`, {
    withCredentials: true,
  });
  return resp.data;
}

// Update a specific cart‐item’s quantity (PUT /api/cart/items/<itemId>/):
export async function updateCartItem(itemId, quantity) {
  const csrftoken = Cookies.get("csrftoken");
  const resp = await axios.put(
    `${BASE_URL}/cart/items/${itemId}/`,
    { quantity },
    {
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      withCredentials: true,
    }
  );
  return resp.data;
}

// Add a new item to the cart (POST /api/cart/items/):
export async function addToCart(productId, quantity) {
  const csrftoken = Cookies.get("csrftoken");
  const resp = await axios.post(
    `${BASE_URL}/cart/items/`,
    { product: productId, quantity },
    {
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      withCredentials: true,
    }
  );
  return resp.data;
}
