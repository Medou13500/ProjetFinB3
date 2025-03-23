import 'package:flutter/material.dart';
import 'screen/homePage.dart';
import 'screen/inscriptionPage.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Mon App',
      initialRoute: '/',
      routes: {
        '/': (context) => const HomePage(),
        '/inscription': (context) =>
            InscriptionPage(message: "Page d'inscription"),
      },
    );
  }
}
