import 'package:flutter/material.dart';

class InscriptionPage extends StatelessWidget {
  final String message;

  const InscriptionPage({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Inscription')),
      body: Center(
        child: Text(message),
      ),
    );
  }
}
