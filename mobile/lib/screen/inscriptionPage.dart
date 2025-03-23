import 'package:flutter/material.dart';

class InscriptionPage extends StatelessWidget {
  final String message;

  InscriptionPage({super.key, required this.message});

  final _formKey = GlobalKey<FormState>();

  final TextEditingController nomController = TextEditingController();
  final TextEditingController prenomController = TextEditingController();
  final TextEditingController ageController = TextEditingController();
  final TextEditingController poidsController = TextEditingController();
  final TextEditingController tailleController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController =
      TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0074BD),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset(
                  "assets/image/logoRunning.jpeg",
                  width: 120,
                ),
                const SizedBox(height: 20),

                _buildInputField(
                  hintText: 'Nom',
                  controller: nomController,
                ),
                const SizedBox(height: 12),

                _buildInputField(
                  hintText: 'Prénom',
                  controller: prenomController,
                ),
                const SizedBox(height: 12),

                _buildInputField(
                  hintText: 'Âge',
                  controller: ageController,
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 12),

                _buildInputField(
                  hintText: 'Poids',
                  controller: poidsController,
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 12),

                _buildInputField(
                  hintText: 'Taille',
                  controller: tailleController,
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 12),

                _buildInputField(
                  hintText: 'Email',
                  controller: emailController,
                  keyboardType: TextInputType.emailAddress,
                ),
                const SizedBox(height: 12),

                _buildInputField(
                  hintText: 'Mot de passe',
                  controller: passwordController,
                  obscureText: true,
                ),
                const SizedBox(height: 12),

                _buildInputField(
                  hintText: 'Confirmation mot de passe',
                  controller: confirmPasswordController,
                  obscureText: true,
                ),
                const SizedBox(height: 20),

                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.grey[300],
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 40, vertical: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(50), // ✅ Arrondi à 50
                    ),
                  ),
                  onPressed: () => _submitForm(context),
                  child: const Text(
                    'Envoyer',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildInputField({
    required String hintText,
    required TextEditingController controller,
    TextInputType keyboardType = TextInputType.text,
    bool obscureText = false,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(
          width: 300,
          height: 40,
          child: TextFormField(
            controller: controller,
            keyboardType: keyboardType,
            obscureText: obscureText,
            style: const TextStyle(
              color: Colors.black,
              fontSize: 14,
              fontWeight: FontWeight.bold,
            ),
            decoration: InputDecoration(
              hintText: hintText,
              isDense: true,
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 15,
                vertical: 8,
              ),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(25),
                borderSide: const BorderSide(
                  color: Colors.transparent,
                ),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(25),
                borderSide: const BorderSide(
                  color: Colors.blue,
                  width: 1.5,
                ),
              ),
              errorBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(25),
                borderSide: const BorderSide(
                  color: Colors.red,
                  width: 1.0,
                ),
              ),
              focusedErrorBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(25),
                borderSide: const BorderSide(
                  color: Colors.red,
                  width: 1.0,
                ),
              ),
              filled: true,
              fillColor: Colors.grey[300],
              hintStyle: const TextStyle(
                color: Colors.black,
                fontSize: 14,
                fontWeight: FontWeight.bold,
              ),
            ),
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Ce champ est obligatoire';
              }
              if (hintText == 'Email' && !value.contains('@')) {
                return 'Entrez un email valide';
              }
              if (hintText == 'Mot de passe' && value.length < 6) {
                return 'Mot de passe trop court';
              }
              if (hintText == 'Confirmation mot de passe' &&
                  value != passwordController.text) {
                return 'Les mots de passe ne correspondent pas';
              }
              return null;
            },
          ),
        ),
        const SizedBox(height: 4),
      ],
    );
  }

  void _submitForm(BuildContext context) {
    if (_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Formulaire soumis !')),
      );
    }
  }
}
