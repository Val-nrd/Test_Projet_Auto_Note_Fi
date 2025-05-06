// src/components/ToastContext.jsx

import React, { createContext, useContext, useState, useCallback } from "react";

// 1. Création du contexte
const ToastContext = createContext();

// 2. Hook pour consommer le contexte
export const useToast = () => {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return ctx;
};

// 3. Provider qui stocke et affiche les toasts
export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const add = useCallback((message, type = "info") => {
    const id = Date.now();
    setToasts((all) => [...all, { id, message, type }]);
    // suppression automatique après 3s
    setTimeout(() => {
      setToasts((all) => all.filter((t) => t.id !== id));
    }, 3000);
  }, []);

  return (
    <ToastContext.Provider value={{ add }}>
      {children}
      <div className="fixed bottom-4 right-4 flex flex-col gap-2 z-50">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={`
              px-4 py-2 rounded shadow text-white
              ${t.type === "error" ? "bg-red-500" : "bg-green-500"}
            `}
          >
            {t.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
