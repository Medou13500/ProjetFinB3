import 'dart:async';
import 'dart:math';
import 'dart:math' as math show sin;
import 'package:flutter/material.dart';
import 'run_history.dart';

class RunReel extends StatefulWidget {
  const RunReel({super.key});

  @override
  State<RunReel> createState() => _RunReelState();
}

class _RunReelState extends State<RunReel> {
  late Timer _timer;
  int _seconds = 0;
  int _calories = 0;
  double _vitesseMax = 0;
  double _vitesseMoy = 0;
  final _rand = Random();

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      setState(() {
        _seconds++;
        if (_seconds % 2 == 0) _calories++;
        _vitesseMax = 8 + _rand.nextDouble() * 6;                 // 8 – 14 km/h
        _vitesseMoy = 5 + math.sin(_seconds / 10) * 1.5;          // 3.5 – 6.5 km/h
      });
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  String _fmt(int n) => n.toString().padLeft(2, '0');
  String _time() {
    final h = _seconds ~/ 3600;
    final m = (_seconds % 3600) ~/ 60;
    final s = _seconds % 60;
    return "${_fmt(h)}:${_fmt(m)}:${_fmt(s)}";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0074BD),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 40),
        child: Column(
          children: [
            Image.asset("assets/image/running.png", width: 120),
            const SizedBox(height: 30),

            // Chrono & calories
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Text(_time(),
                    style:
                        const TextStyle(color: Colors.white, fontSize: 28)),
                Text("$_calories calories",
                    style:
                        const TextStyle(color: Colors.white, fontSize: 28)),
              ],
            ),
            const SizedBox(height: 30),

            // Vitesses
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Text("Vitesse max:\n${_vitesseMax.toStringAsFixed(1)} km/h",
                    textAlign: TextAlign.center,
                    style:
                        const TextStyle(color: Colors.white, fontSize: 22)),
                Text("Vitesse moy:\n${_vitesseMoy.toStringAsFixed(1)} km/h",
                    textAlign: TextAlign.center,
                    style:
                        const TextStyle(color: Colors.white, fontSize: 22)),
              ],
            ),
            const SizedBox(height: 30),

            // Carte fictive
            Image.asset("assets/image/map_placeholder.png",
                height: 260, width: double.infinity, fit: BoxFit.cover),
            const SizedBox(height: 30),

            // Finir la course
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.grey[300],
                foregroundColor: Colors.black,
                padding:
                    const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30)),
              ),
              onPressed: () {
                final run = RunHistory(
                  duration: _time(),
                  calories: _calories,
                  vitesseMax: _vitesseMax,
                  vitesseMoy: _vitesseMoy,
                );
                Navigator.pop(context, run);       // ⬅️ renvoi l’objet
              },
              child: const Text(
                "Terminer la course",
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
