import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'run_reel.dart';
import 'historique_page.dart';
import 'run_history.dart';

class StartRun extends StatefulWidget {
  final String email;
  const StartRun({super.key, required this.email});

  @override
  State<StartRun> createState() => _StartRunState();
}

class _StartRunState extends State<StartRun> {
  final List<RunHistory> _historiques = [];
  final List<FlSpot> _performanceData = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0074BD),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 40),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Logo + bouton historique
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Image.asset("assets/image/running.png", width: 120),
                TextButton(
                  style: TextButton.styleFrom(
                    backgroundColor: Colors.grey[300],
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => HistoriquePage(historiques: _historiques),
                      ),
                    );
                  },
                  child: const Text(
                    'Historique de course',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 40),

            // Bienvenue
            Text(
              "Bienvenue ${widget.email}",
              style: const TextStyle(fontSize: 20, color: Colors.white),
            ),
            const SizedBox(height: 20),

            // Graphique dynamique
            if (_performanceData.isNotEmpty)
              SizedBox(
                height: 200,
                child: LineChart(
                  LineChartData(
                    gridData: FlGridData(show: false),
                    titlesData: FlTitlesData(show: false),
                    borderData: FlBorderData(show: false),
                    lineBarsData: [
                      LineChartBarData(
                        isCurved: true,
                        color: Colors.white,
                        barWidth: 3,
                        dotData: FlDotData(show: true),
                        belowBarData: BarAreaData(show: false),
                        spots: _performanceData,
                      ),
                    ],
                  ),
                ),
              )
            else
              const Text(
                'Aucune donnée de performance.',
                style: TextStyle(color: Colors.white),
              ),

            const SizedBox(height: 40),

            // Bouton Commencer la course
            Center(
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.grey[300],
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                ),
                onPressed: () async {
                  final result = await Navigator.push<RunHistory>(
                    context,
                    MaterialPageRoute(builder: (_) => const RunReel()),
                  );

                  if (result != null) {
                    setState(() {
                      _historiques.add(result);

                      // ⚠️ On affiche ici la distance de chaque course dans le graphique
                      _performanceData.add(
                        FlSpot(
                          _performanceData.length.toDouble(),
                          result.distance, // ou result.vitesse, result.calories
                        ),
                      );
                    });
                  }
                },
                child: const Text(
                  'Commencer la course',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
