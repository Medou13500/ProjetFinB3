import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';


function MotsDePasseOublie() {
  const navigate = useNavigate();

  const Schema = Yup.object().shape({
    email: Yup.string()
      .email("Adresse email invalide")
      .required("Champ requis"),
    password: Yup.string()
      .min(8, "Min 8 caractères")
      .matches(/^[A-Z](?=.*\d)(?=.*[@$!%*?&]).*$/, "Majuscule, chiffre, caractère spécial")
      .required("Champ requis"),
  });

  return (
    <div
      className="container-fluid bg-white d-flex justify-content-center align-items-center"
      style={{
        minHeight: '100vh',
        paddingTop: '20px',
        paddingBottom: '20px',
      }}
    >
      <div
        className="text-center p-4 rounded"
        style={{
          backgroundColor: '#0DD1F6',
          width: '700px',
          height: '400px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        <h2 className="text-white mb-4">Mot de passe oublié</h2>

        <Formik
          initialValues={{ email: '', password: '' }}
          validationSchema={Schema}
          onSubmit={(values) => {
            console.log("Réinitialisation :", values);
          }}
        >
          {({ isSubmitting }) => (
            <Form>
              <div className="mb-3">
                <Field
                  name="email"
                  type="email"
                  className="form-control rounded-pill text-center bg-light border-0 w-75 mx-auto"
                  placeholder="email"
                />
                <ErrorMessage name="email" component="div" className="form-text text-danger" />
              </div>

              <div className="mb-3">
                <Field
                  name="password"
                  type="password"
                  className="form-control rounded-pill text-center bg-light border-0 w-75 mx-auto"
                  placeholder="nouveau mot de passe"
                />
                <ErrorMessage name="password" component="div" className="form-text text-danger" />
              </div>

              <div className="d-flex flex-column align-items-center gap-3 mt-4">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn bg-light text-dark rounded-pill px-5 py-2"
                >
                  Réinitialiser
                </button>

              <button
              type="button"
              onClick={() => navigate('/Connexion', { replace: true })}
              className="btn btn-outline-light rounded-pill px-4 py-2"
            >
              Retour
            </button>

              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
}

export default MotsDePasseOublie;
