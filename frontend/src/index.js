// src/index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.js';
import './styles/globals.css';
import reportWebVitals from './reportWebVitals';

const container = document.getElementById('root');
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Se você quiser medir a performance da sua aplicação, passe uma função
// para registrar os resultados (por exemplo: reportWebVitals(console.log))
// ou envie para um endpoint de analytics. Saiba mais: https://bit.ly/CRA-vitals
reportWebVitals();