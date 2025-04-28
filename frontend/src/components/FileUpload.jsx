// src/components/FileUpload.jsx

import React, { useState, useEffect } from "react";
import { useToast } from "./ToastContext";

const FileUpload = ({ onSaveAnalysis, loadedAnalysis }) => {
  const toast = useToast();
  const [files, setFiles] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [extractedText, setExtractedText] = useState("");
  const [fullAnalysis, setFullAnalysis] = useState({
    entreprise: "",
    marche: "",
    concurrence: "",
  });

  useEffect(() => {
    if (loadedAnalysis) {
      setResult({ filename: loadedAnalysis.filename });
      setExtractedText(`Analyse chargée : ${loadedAnalysis.filename}`);
      setFullAnalysis({
        entreprise: loadedAnalysis.entreprise || "",
        marche: loadedAnalysis.marche || "",
        concurrence: loadedAnalysis.concurrence || "",
      });
    } else {
      setExtractedText("");
      setFullAnalysis({ entreprise: "", marche: "", concurrence: "" });
    }
  }, [loadedAnalysis]);

  const handleUpload = async () => {
    if (!files.length) {
      toast.add("⚠️ Choisis au moins un fichier", "error");
      return;
    }
    setLoading(true);
    try {
      const formData = new FormData();
      files.forEach((file) => formData.append("files", file));

      const response = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data);
      const allText =
        data.extraits?.map((e) => e.texte).join("\n\n") || "";
      setExtractedText(allText.slice(0, 3000));
      toast.add("📤 Fichiers uploadés", "info");
    } catch (error) {
      console.error("Erreur upload :", error);
      toast.add("❌ Upload échoué", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeAll = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/analyze_all/", {
        method: "POST",
      });
      const data = await response.json();
      if (
        response.ok &&
        data.entreprise &&
        data.marche &&
        data.concurrence
      ) {
        setFullAnalysis({
          entreprise: data.entreprise,
          marche: data.marche,
          concurrence: data.concurrence,
        });
        toast.add("🧠 Analyse complète reçue", "info");
      } else {
        toast.add("❌ Résultat incomplet ou invalide", "error");
      }
    } catch (error) {
      console.error("Erreur analyse complète :", error);
      toast.add("❌ Erreur de connexion", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveFullAnalysis = () => {
    if (
      !fullAnalysis.entreprise &&
      !fullAnalysis.marche &&
      !fullAnalysis.concurrence
    ) {
      toast.add("⚠️ Rien à sauvegarder", "error");
      return;
    }
    const filenames = Array.isArray(result?.extraits)
      ? result.extraits.map((e) => e.filename)
      : [result?.filename || "Inconnu"];
    const saved = {
      id: Date.now(),
      title: "Nouvelle analyse",
      date: new Date().toLocaleString(),
      entreprise: fullAnalysis.entreprise,
      marche: fullAnalysis.marche,
      concurrence: fullAnalysis.concurrence,
      filenames,
      chatHistory: [],
    };
    onSaveAnalysis(saved);
  };

  const handleRemoveFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="text-white flex flex-col gap-4 max-w-3xl mx-auto p-4">
      <input
        type="file"
        multiple
        onChange={(e) => setFiles(Array.from(e.target.files))}
        className="bg-gray-800 p-2 rounded"
        disabled={loading}
      />

      {files.length > 0 && (
        <div className="bg-gray-800 p-3 rounded text-sm">
          <h4 className="text-white font-semibold mb-2">
            📄 Fichiers sélectionnés :
          </h4>
          <ul className="list-disc pl-5 space-y-1">
            {files.map((f, i) => (
              <li key={i} className="flex justify-between items-center">
                {f.name}
                <button
                  onClick={() => handleRemoveFile(i)}
                  className="text-red-400 text-xs ml-4 hover:underline"
                >
                  Supprimer
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      <button
        onClick={handleUpload}
        className="bg-blue-600 hover:bg-blue-700 p-2 rounded disabled:opacity-50"
        disabled={loading}
      >
        {loading ? "Chargement..." : "📤 Uploader les fichiers"}
      </button>

      {result && (
        <>
          <div className="bg-gray-900 p-4 rounded text-sm max-h-[300px] overflow-y-scroll whitespace-pre-wrap">
            {extractedText}
          </div>

          <div className="flex flex-wrap gap-2 mt-4">
            <button
              onClick={handleAnalyzeAll}
              className="bg-cyan-600 hover:bg-cyan-700 px-4 py-2 rounded disabled:opacity-50"
              disabled={loading}
            >
              🧠 Analyse complète
            </button>
            <button
              onClick={handleSaveFullAnalysis}
              className="bg-gray-700 hover:bg-gray-800 px-4 py-2 rounded"
            >
              💾 Sauvegarder l’analyse
            </button>
          </div>

          {(fullAnalysis.entreprise ||
            fullAnalysis.marche ||
            fullAnalysis.concurrence) && (
            <div className="mt-6 space-y-6 bg-gray-800 p-6 rounded-lg shadow text-white max-h-[600px] overflow-y-auto">
              {fullAnalysis.entreprise && (
                <div>
                  <h3 className="text-xl font-bold mb-2 text-blue-400">
                    🧠 Analyse d’entreprise
                  </h3>
                  <pre className="whitespace-pre-wrap">
                    {fullAnalysis.entreprise}
                  </pre>
                </div>
              )}
              {fullAnalysis.concurrence && (
                <div>
                  <h3 className="text-xl font-bold mb-2 text-purple-400">
                    ⚔️ Analyse concurrentielle
                  </h3>
                  <pre className="whitespace-pre-wrap">
                    {fullAnalysis.concurrence}
                  </pre>
                </div>
              )}
              {fullAnalysis.marche && (
                <div>
                  <h3 className="text-xl font-bold mb-2 text-orange-400">
                    🌍 Analyse du marché
                  </h3>
                  <pre className="whitespace-pre-wrap">
                    {fullAnalysis.marche}
                  </pre>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default FileUpload;
