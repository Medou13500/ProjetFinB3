import 'package:flutter/material.dart';
import 'run_reel.dart';
import 'run_history.dart';
import 'historique_page.dart';

class StartRun extends StatefulWidget {
  final String email;
  const StartRun({super.key, required this.email});

  @override
  State<StartRun> createState() => _StartRunState();
}

class _StartRunState extends State<StartRun> {
  final List<RunHistory> _historiques = [];

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
                Image.asset("assets/image/logoRunning.jpeg", width: 120),
                TextButton(
                  style: TextButton.styleFrom(
                    backgroundColor: Colors.grey[300],
                    foregroundColor: Colors.black,
                    padding:
                        const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30)),
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            HistoriquePage(historiques: _historiques),
                      ),
                    );
                  },
                  child: const Text('Historique de course',
                      style: TextStyle(fontWeight: FontWeight.bold)),
                ),
              ],
            ),
            const SizedBox(height: 50),

            // Message de bienvenue
            Text("Bienvenue ${widget.email}",
                style: const TextStyle(fontSize: 20, color: Colors.white)),
            const SizedBox(height: 40),

            // Bouton Commencer
            Center(
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.grey[300],
                  foregroundColor: Colors.black,
                  padding:
                      const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30)),
                ),
                onPressed: () async {
                  final result = await Navigator.push<RunHistory>(
                    context,
                    MaterialPageRoute(builder: (_) => const RunReel()),
                  );
                  if (result != null) {
                    setState(() => _historiques.add(result));
                  }
                },
                child: const Text('Commencer la course',
                    style:
                        TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
