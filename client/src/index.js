import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css'; // Use App.css, which you already created
import App from './App';

// Find the 'root' div in the HTML file
const rootElement = document.getElementById('root');

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("Could not find 'root' element. Make sure public/index.html exists!");
}