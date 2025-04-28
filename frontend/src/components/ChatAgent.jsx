import React, { useState } from "react";

const ChatAgent = ({ onMessage }) => {
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    onMessage(message);
    setMessage("");
  };

  return (
    <div className="fixed bottom-0 left-64 right-0 bg-gray-800 border-t border-gray-700 p-4">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Posez une question à l’agent IA..."
          className="flex-1 p-2 rounded bg-gray-700 text-white placeholder-gray-400"
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Envoyer
        </button>
      </form>
    </div>
  );
};

export default ChatAgent;
