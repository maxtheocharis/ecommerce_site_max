// frontend/src/index.js

import React from "react";
// Use the new client‐side API in React 18+
import { createRoot } from "react-dom/client";

import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

// 1. Grab the <div id="root"> from public/index.html:
const container = document.getElementById("root");

// 2. Create a root for that container:
const root = createRoot(container);

// 3. Render your App into it:
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// (Optional) performance measurement:
reportWebVitals();
