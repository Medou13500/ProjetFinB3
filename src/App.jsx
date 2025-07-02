import React from "react";
import { Routes, Route } from "react-router-dom";
import Accueil from "./components/Accueil";
import Layout from "./components/Layout";
import Formulaire from "./components/connexion";
import MotsDePasseOublie from "./components/MotsDePasseOublie";
import ListUser from "./components/ListUser";
import PrivateRoute from "./components/PrivateRoute";
import UserStats from "./components/UserStats"; //

import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Accueil />} />
        <Route path="Accueil" element={<Accueil />} />
        <Route path="Connexion" element={<Formulaire />} />
        <Route path="mdpOublie" element={<MotsDePasseOublie />} />
         <Route path="/stats/:user_id" element={<UserStats />} />
      <Route path="/ListUser" element={<PrivateRoute><ListUser /></PrivateRoute>} />
      
      </Route>
    </Routes>
  );
}

export default App;
