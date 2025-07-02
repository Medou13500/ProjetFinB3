// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth, setPersistence, browserLocalPersistence } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyC79Rhe2OwqpEgrt3uACIM0s73xWs63bDw",
  authDomain: "projetrunning-e2d1d.firebaseapp.com",
  projectId: "projetrunning-e2d1d",
  storageBucket: "projetrunning-e2d1d.appspot.com",
  messagingSenderId: "92541257881",
  appId: "1:92541257881:web:XXXX" // remplace par ton vrai ID si nécessaire
};

// Initialise Firebase
const app = initializeApp(firebaseConfig);

// Initialise Auth
const auth = getAuth(app);

// ✅ Utilise localStorage pour garder la session
setPersistence(auth, browserLocalPersistence);

export { auth };
