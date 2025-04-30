import React, { useState, useEffect } from "react";

const Sidebar = ({ analyses, onSelect, onRename, onNewAnalysis }) => {
  const [editingId, setEditingId] = useState(null);
  const [newTitle, setNewTitle] = useState("");

  useEffect(() => {
    setEditingId(null);
    setNewTitle("");
  }, [analyses]);

  const startEditing = (id, currentTitle) => {
    setEditingId(id);
    setNewTitle(currentTitle);
  };

  const saveTitle = (id) => {
    const trimmed = newTitle.trim();
    if (trimmed) {
      onRename(id, trimmed);
    }
    setEditingId(null);
    setNewTitle("");
  };

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-gray-800 text-white p-4 border-r border-gray-700 overflow-y-auto z-40">
      <button
        onClick={onNewAnalysis}
        className="w-full mb-4 px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
      >
        ➕ Nouvelle analyse
      </button>

      <h2 className="text-xl font-bold mb-4">📁 Mes Analyses</h2>
      <ul className="space-y-2">
        {analyses.map((a) => (
          <li
            key={a.id}
            className="bg-gray-700 p-3 rounded hover:bg-gray-600 cursor-pointer"
            onClick={() => editingId !== a.id && onSelect(a)}
          >
            {editingId === a.id ? (
              <input
                className="w-full bg-white text-black px-2 py-1 rounded"
                value={newTitle}
                autoFocus
                onChange={(e) => setNewTitle(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") saveTitle(a.id);
                  else if (e.key === "Escape") {
                    setEditingId(null);
                    setNewTitle("");
                  }
                }}
                onBlur={() => saveTitle(a.id)}
              />
            ) : (
              <div className="flex justify-between items-center">
                <span>{a.title}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    startEditing(a.id, a.title);
                  }}
                  className="text-sm text-blue-400 hover:text-blue-200"
                >
                  ✏️
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
