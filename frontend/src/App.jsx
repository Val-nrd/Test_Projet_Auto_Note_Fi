// src/App.jsx

import React, { useState, useEffect } from "react";
import FileUpload from "./components/FileUpload";
import Sidebar from "./components/Sidebar";
import ChatBox from "./components/ChatBox";
import { useToast } from "./components/ToastContext";

const LOCAL_STORAGE_KEY = "savedAnalyses";

const App = () => {
  const toast = useToast();

  // ————— (état et persistance inchangés) —————
  const [savedAnalyses, setSavedAnalyses] = useState(() => {
    try {
      const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  });
  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(savedAnalyses));
  }, [savedAnalyses]);

  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [editMode, setEditMode] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);

  // nouveau : état de chargement du chat
  const [chatLoading, setChatLoading] = useState(false);

  useEffect(() => {
    setChatHistory(selectedAnalysis?.chatHistory || []);
  }, [selectedAnalysis]);

  const handleSaveAnalysis = (newAnalysis) => {
    const toSave = { ...newAnalysis, chatHistory: [] };
    setSavedAnalyses((prev) => [...prev, toSave]);
    setSelectedAnalysis(toSave);
    toast.add("✅ Analyse enregistrée", "info");
  };
  const handleSelectAnalysis = (a) => setSelectedAnalysis(a);
  const handleRenameAnalysis = (id, title) => {
    setSavedAnalyses((prev) =>
      prev.map((a) => (a.id === id ? { ...a, title } : a))
    );
    if (selectedAnalysis?.id === id) {
      setSelectedAnalysis((prev) => ({ ...prev, title }));
      toast.add("✏️ Titre modifié", "info");
    }
  };
  const handleNewAnalysis = () => {
    setSelectedAnalysis(null);
    setChatHistory([]);
  };

  // ————— Orchestration légère avec spinner & toast —————
  const handleAgentMessage = async (userMessage) => {
    setChatLoading(true);
    // 1) on stocke le message utilisateur
    const hist1 = [...chatHistory, { from: "user", text: userMessage }];
    setChatHistory(hist1);

    try {
      const edition = editMode && selectedAnalysis?.entreprise;
      const chatPayload = edition
        ? {
            message: `
Tu es un assistant d’analyse financière.
Voici la fiche entreprise à **mettre à jour** :

"""${selectedAnalysis.entreprise}"""

Demande : "${userMessage}"

→ Modifie seulement ce qui doit l’être, sans intro.
Réponds uniquement avec le texte mis à jour.
`,
          }
        : { message: userMessage };

      // appel chat
      const chatRes = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(chatPayload),
      });
      const { response: botReplyRaw } = await chatRes.json();
      const botReply = botReplyRaw || "❌ Pas de réponse.";

      // on ajoute la réponse brute
      const hist2 = [...hist1, { from: "bot", text: botReply }];
      setChatHistory(hist2);

      if (edition) {
        // orchestration
        const compRes = await fetch(
          "http://localhost:8000/analyze_company/",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: botReply }),
          }
        );
        const { company_analysis } = await compRes.json();

        const updated = {
          ...selectedAnalysis,
          entreprise: company_analysis,
          chatHistory: hist2,
        };
        setSelectedAnalysis(updated);
        setSavedAnalyses((all) =>
          all.map((a) => (a.id === updated.id ? updated : a))
        );
        toast.add("🔄 Analyse entreprise mise à jour", "info");
      }
    } catch (err) {
      console.error("Orch. légère erreur :", err);
      setChatHistory((prev) => [
        ...prev,
        { from: "bot", text: "❌ Erreur lors de la mise à jour." },
      ]);
      toast.add("❌ Erreur lors de l’appel à l’IA", "error");
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white relative">
      {showSidebar && (
        <Sidebar
          analyses={savedAnalyses}
          onSelect={handleSelectAnalysis}
          onRename={handleRenameAnalysis}
          onNewAnalysis={handleNewAnalysis}
        />
      )}

      <main
        className={`
          flex-1 transition-all duration-300
          ${showSidebar ? "ml-64" : "ml-0"}
          ${showChat ? "mr-[28rem]" : "mr-0"}
          flex flex-col
        `}
      >
        {/* Toggle sidebar */}
        <button
          onClick={() => setShowSidebar((v) => !v)}
          className="absolute top-4 left-4 z-50 p-1 border border-gray-600 rounded hover:bg-gray-700"
        >
          {showSidebar ? "<<" : ">>"}
        </button>

        {/* Header */}
        <div className="flex justify-between items-start p-6 pt-12">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              Automatisez vos analyses financières avec l’IA.
            </h1>
            <label className="inline-flex items-center text-sm text-gray-400">
              <input
                type="checkbox"
                checked={editMode}
                onChange={(e) => setEditMode(e.target.checked)}
                className="mr-2"
              />
              Mode édition automatique
            </label>
          </div>
          <button
            onClick={() => setShowChat((v) => !v)}
            className="px-3 py-2 bg-gray-700 rounded"
          >
            {showChat ? "Fermer chat" : "Ouvrir chat"}
          </button>
        </div>

        {/* Contenu */}
        <div className="flex-1 overflow-y-auto px-6 pb-6">
          <FileUpload
            key={selectedAnalysis?.id || "upload"}
            onSaveAnalysis={handleSaveAnalysis}
            loadedAnalysis={selectedAnalysis}
          />
        </div>
      </main>

      {showChat && (
        <div className="fixed top-0 right-0 h-full w-[28rem] border-l bg-gray-950 z-50">
          <ChatBox
            chatHistory={chatHistory}
            onMessage={handleAgentMessage}
            loading={chatLoading}
          />
        </div>
      )}
    </div>
  );
};

export default App;
