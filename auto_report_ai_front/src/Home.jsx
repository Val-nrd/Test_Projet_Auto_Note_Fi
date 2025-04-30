import React from "react";

export default function Home() {
  return (
    <main className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors duration-300">
      <header className="flex items-center justify-between px-6 py-4 shadow-md bg-white dark:bg-gray-800">
        <h1 className="text-xl font-bold">Auto Report AI</h1>
        <button
          onClick={() =>
            document.documentElement.classList.toggle("dark")
          }
          className="text-sm px-4 py-2 border rounded hover:bg-gray-100 dark:hover:bg-gray-700"
        >
          🌗 Toggle Dark Mode
        </button>
      </header>

      <section className="flex flex-col items-center justify-center h-[80vh] text-center px-6">
        <h2 className="text-4xl font-bold mb-4">
          Automatisez vos analyses financières avec l’IA.
        </h2>
        <p className="text-lg mb-6 max-w-xl">
          Générez en quelques clics une analyse complète du marché, de la concurrence
          et de l’entreprise à partir de vos documents.
        </p>
        <button className="px-6 py-3 bg-black text-white dark:bg-white dark:text-black rounded-md hover:opacity-90 transition">
          🚀 Démarrer une analyse
        </button>
      </section>
    </main>
  );
}
