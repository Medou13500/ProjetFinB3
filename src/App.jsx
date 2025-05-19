import React from "react";
import { Routes, Route } from "react-router-dom";
import Accueil from "../component/Accueil";
import Layout from "../component/Layout";
import Formulaire from "../component/connexion";
import './App.css';
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="Accueil" element={<Accueil />} />
           <Route path="Connexion" element={<Formulaire />} />
      </Route>
    </Routes>
  );
}

export default App;
