import 'package:flutter/material.dart';
import '../screen/inscriptionPage.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF0074BD),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image.asset(
            "assets/image/logoRunning.jpeg",
            width: 120,
          ),
          SizedBox(height: 20),
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 30),
            child: Text(
              "Bienvenue sur le tableau de bord.\n\n"
              "Ici, vous pouvez suivre vos projets, analyser vos performances et atteindre de nouveaux objectifs.",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 20,
                fontFamily: "Inter",
                color: Colors.white,
                decoration: TextDecoration.none,
              ),
            ),
          ),
          SizedBox(height: 30),
          // ✅ Bouton Inscription corrigé
          TextButton(
            style: TextButton.styleFrom(
              foregroundColor: Colors.black,
              backgroundColor: Colors.grey[300],
              fixedSize: Size(237, 50),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.zero,
              ),
            ),
            onPressed: () {
              Navigator.pushNamed(
                  context, '/inscription'); // ✅ Redirection par route nommée
            },
            child: Text(
              'Inscription',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ),
          SizedBox(height: 15),
          // ✅ Bouton Connexion
          TextButton(
            style: TextButton.styleFrom(
              foregroundColor: Colors.black,
              backgroundColor: Colors.grey[300],
              fixedSize: Size(237, 50),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.zero,
              ),
            ),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) =>
                      InscriptionPage(message: "Page d'inscription"),
                ),
              );
            },
            child: Text(
              'Connexion',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );
  }
}
