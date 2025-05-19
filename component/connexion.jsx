import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

function Formulaire() {
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
    <div className="container-fluid min-vh-100  d-flex justify-content-center align-items-center bg-white">
      <div className="bg-info text-center p-4 rounded" style={{ width: '700px', height: "400px" }}>
        <h2 className="text-white mb-4">Connexion</h2>

        <Formik
          initialValues={{ email: '', password: '' }}
          validationSchema={Schema}
          onSubmit={(values) => {
            console.log(values);
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

                <ErrorMessage name="password" component="div" className="form-text text-danger" />
              </div>
              <Field
                name="password"
                type="password"
                className="form-control rounded-pill text-center bg-light border-0 w-75 mx-auto"
                placeholder="mot de passe"
                />


                        <div className="d-flex flex-column align-items-center gap-4 mb-2 mt-3">
            <button
                type="submit"
                disabled={isSubmitting}
                className="btn bg-light text-dark rounded-pill px-5 py-2 mt-4"
            >
                Envoyer
            </button>

            <a
                href="#"
                className="btn bg-light text-dark rounded-pill px-5 py-2"
            >
                mot de passe oublié
            </a>
            </div>

            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
}

export default Formulaire;
