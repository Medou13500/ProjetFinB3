import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';

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

  final Random _random = Random();

  @override
  void initState() {
    super.initState();
    _startTimer();
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        _seconds++;

        // Augmentation progressive des calories
        if (_seconds % 2 == 0) _calories++;

        // Fluctuation de la vitesse max entre 8 et 14 km/h
        _vitesseMax = 8 + _random.nextDouble() * 6;

        // Vitesse moyenne qui évolue doucement
        _vitesseMoy = 5 + sin(_seconds / 10) * 1.5;
      });
    });
  }

  String _formatTime(int totalSeconds) {
    final hours = totalSeconds ~/ 3600;
    final minutes = (totalSeconds % 3600) ~/ 60;
    final seconds = totalSeconds % 60;
    return '${_twoDigits(hours)}:${_twoDigits(minutes)}:${_twoDigits(seconds)}';
  }

  String _twoDigits(int n) => n.toString().padLeft(2, '0');

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0074BD),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 40),
        child: Column(
          children: [
            Image.asset("assets/image/logoRunning.jpeg", width: 120),
            const SizedBox(height: 30),

            // Temps et Calories
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Text(
                  _formatTime(_seconds),
                  style: const TextStyle(color: Colors.white, fontSize: 28),
                ),
                Text(
                  "$_calories calories",
                  style: const TextStyle(color: Colors.white, fontSize: 28),
                ),
              ],
            ),
            const SizedBox(height: 30),

            // Vitesse max / moyenne
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                Column(
                  children: [
                    Text(
                      "Vitesse max:\n${_vitesseMax.toStringAsFixed(1)} km/h",
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Colors.white, fontSize: 22),
                    ),
                  ],
                ),
                Column(
                  children: [
                    Text(
                      "Vitesse moy:\n${_vitesseMoy.toStringAsFixed(1)} km/h",
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Colors.white, fontSize: 22),
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 30),

            // Carte (image temporaire)
            Image.asset(
              "assets/image/map_placeholder.png",
              height: 260,
              width: double.infinity,
              fit: BoxFit.cover,
            ),

            const SizedBox(height: 30),

            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.grey[300],
                foregroundColor: Colors.black,
                padding:
                    const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
              ),
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text(
                'Terminer la course',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
