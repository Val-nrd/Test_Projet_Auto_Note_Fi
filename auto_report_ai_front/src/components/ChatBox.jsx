// src/components/ChatBox.jsx
import React, { useState, useRef } from "react";

const ChatBox = ({ chatHistory, onMessage, loading }) => {
  const [input, setInput] = useState("");
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    onMessage(input);
    setInput("");
  };

  return (
    <div className="flex flex-col h-full bg-gray-950 text-white">
      {/* messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {chatHistory?.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded max-w-xl ${
              msg.from === "user"
                ? "bg-blue-700 ml-auto"
                : "bg-gray-800 mr-auto"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* saisie */}
      <form
        onSubmit={handleSubmit}
        className="p-4 border-t border-gray-800 flex flex-col gap-2"
      >
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Posez une question à l’IA..."
          rows={3}
          className="w-full bg-gray-900 text-white p-2 rounded border border-gray-700 focus:outline-none resize-none"
          disabled={loading}
        />

        <button
          type="submit"
          className="self-end flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm disabled:opacity-50"
          disabled={loading}
        >
          {loading && (
            <span className="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
          )}
          Envoyer
        </button>
      </form>
    </div>
  );
};

export default ChatBox;
