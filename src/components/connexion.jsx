import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { signInWithEmailAndPassword, getIdToken } from "firebase/auth";
import { auth } from "../firebase";
import { useAuth } from "./AuthContext";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Formulaire() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const Schema = Yup.object().shape({
    email: Yup.string().email("Adresse email invalide").required("Champ requis"),
    password: Yup.string().min(6).matches(/\d/, "Doit contenir un chiffre").required("Champ requis"),
  });

  return (
    <div className="container-fluid bg-white d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
      <div className="text-center p-4 rounded" style={{ backgroundColor: '#0DD1F6', width: '700px', height: '400px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <h2 className="text-white mb-4">Connexion</h2>
        <Formik
          initialValues={{ email: '', password: '' }}
          validationSchema={Schema}
          onSubmit={async (values, { setSubmitting, setErrors }) => {
            try {
              const userCredential = await signInWithEmailAndPassword(auth, values.email, values.password);
              const token = await getIdToken(userCredential.user);
              login(token);
              toast.success("Connexion réussie !");
              setTimeout(() => navigate("/ListUser"), 1000);
            } catch (error) {
              if (error.code === "auth/user-not-found") {
                setErrors({ email: "Utilisateur non trouvé" });
              } else if (error.code === "auth/wrong-password") {
                setErrors({ password: "Mot de passe incorrect" });
              } else {
                setErrors({ email: "Erreur de connexion" });
              }
            } finally {
              setSubmitting(false);
            }
          }}
        >
          {({ isSubmitting }) => (
            <Form>
              <div className="mb-3">
                <Field name="email" type="email" className="form-control rounded-pill text-center bg-light border-0 w-100 mx-auto" placeholder="email" />
                <ErrorMessage name="email" component="div" className="form-text text-danger" />
              </div>
              <div className="mb-3">
                <Field name="password" type="password" className="form-control rounded-pill text-center bg-light border-0 w-100 mx-auto" placeholder="mot de passe" />
                <ErrorMessage name="password" component="div" className="form-text text-danger" />
              </div>
              <div className="d-flex flex-column align-items-center gap-3 mt-4">
                <button type="submit" disabled={isSubmitting} className="btn bg-white text-dark rounded-pill px-5 py-2">Envoyer</button>
                <button type="button" onClick={() => navigate('/mdpOublie')} className="btn bg-white text-dark rounded-pill px-5 py-2">
                  mot de passe oublié
                </button>
              </div>
            </Form>
          )}
        </Formik>
        <ToastContainer position="top-center" />
      </div>
    </div>
  );
}

export default Formulaire;
