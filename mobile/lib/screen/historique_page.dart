import 'package:flutter/material.dart';
import 'run_history.dart';

class HistoriquePage extends StatelessWidget {
  final List<RunHistory> historiques;

  const HistoriquePage({super.key, required this.historiques});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Historique de course'),
        backgroundColor: const Color(0xFF0074BD),
      ),
      body: historiques.isEmpty
          ? const Center(
              child: Text(
                "Aucune course enregistrée pour le moment.",
                style: TextStyle(fontSize: 16),
              ),
            )
          : ListView.builder(
              itemCount: historiques.length,
              itemBuilder: (_, i) {
                final run = historiques[i];
                return Card(
                  margin:
                      const EdgeInsets.symmetric(horizontal: 15, vertical: 10),
                  child: ListTile(
                    leading: const Icon(Icons.directions_run),
                    title: Text("Durée : ${run.duration}"),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text("Calories : ${run.calories} kcal"),
                        Text("Vitesse max : ${run.vitesseMax.toStringAsFixed(1)} km/h"),
                        Text("Vitesse moy : ${run.vitesseMoy.toStringAsFixed(1)} km/h"),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
