// src/main.jsx

import React from "react";
import ReactDOM from "react-dom/client";

// **Import du CSS global (Tailwind)**
import "./index.css";

import App from "./App";
import { ToastProvider } from "./components/ToastContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  <ToastProvider>
    <App />
  </ToastProvider>
);

