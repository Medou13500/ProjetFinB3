import 'package:flutter/material.dart';
import 'screen/homePage.dart'; // ✅ Vérifie bien que c'est "screen/" et non "screens/"

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
      home: const HomePage(),
    );
  }
}
