import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [imageSrc, setImageSrc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a description for the room.');
      return;
    }
    setLoading(true);
    setError('');
    setImageSrc(null);

    try {
      // FIX 1: Use full URL for localhost (unless you set up a proxy)
      const res = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          prompt: prompt,
          // You can pass style/width/height here if you want to expand later
          width: 1024,
          height: 1024
        }),
      });

      if (!res.ok) {
        const text = await res.json();
        throw new Error(text.detail || 'Generation failed');
      }

      const data = await res.json();

      // FIX 2: Backend returns a full Data URI, so just use it directly
      setImageSrc(data.image);

    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to connect to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <header className="header">
        <h1>Safahomes AI</h1>
        <p>Interior & Exterior Design Generator</p>
      </header>

      <div className="input-container">
        <input
          className="prompt-input"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g. Modern living room with large windows and wood floor..."
          onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
        />
        <button
          className="generate-btn"
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? 'Designing...' : 'Generate'}
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="image-display-area">
        {loading && <div className="loading-spinner">Generating your design... (This may take 10-20s)</div>}
        
        {!loading && imageSrc && (
          <div className="result-card">
            <img src={imageSrc} alt="Generated Design" className="generated-image" />
            <br />
            <a href={imageSrc} download="safahomes_design.png" className="download-btn">
              Download Image
            </a>
          </div>
        )}

        {!loading && !imageSrc && !error && (
          <div className="placeholder">
            Enter a prompt above to visualize your home design.
          </div>
        )}
      </div>
    </div>
  );
}

export default App;