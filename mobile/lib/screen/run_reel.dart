import 'dart:async';
import 'dart:math';
import 'dart:math' as math show sin;
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:geolocator/geolocator.dart';
import 'run_history.dart';

class RunReel extends StatefulWidget {
  const RunReel({super.key});

  @override
  State<RunReel> createState() => _RunReelState();
}

class _RunReelState extends State<RunReel> {
  late Timer _timer;
  final _rand = Random();
  final MapController _mapController = MapController(); // Contrôle de la carte

  int _sec = 0;
  int _cal = 0;
  double _vMax = 0, _vAvg = 0;

  LatLng _pos = LatLng(
    43.5287,
    5.4456,
  ); // Position de départ (Aix-en-Provence !)
  List<LatLng> _simulatedPath = []; // Trajet simulé
  List<LatLng> _visitedPath = []; // Chemin parcouru
  int _pathIndex = 0;

  @override
  void initState() {
    super.initState();
    _startTimer(); // Lance le chronomètre
    _generateSimulatedPath(); // Génére un faux parcours
    _startSimulation(); // Commence à simuler les déplacements
  }

  //!Chronomètre et mise à jour des valeurs simulées (calories, vitesses)
  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (!mounted) return;
      setState(() {
        _sec++; // 1 seconde de plus
        if (_sec % 2 == 0) _cal++; // Calories toutes les 2 secondes
        _vMax = 8 + _rand.nextDouble() * 6; // Vitesse max aléatoire
        _vAvg = 5 + math.sin(_sec / 10) * 1.5; // Vitesse moyenne ondulée
      });
    });
  }

  //! Crée un chemin fictif de 20 km
  void _generateSimulatedPath() {
    _simulatedPath = List.generate(4000, (i) {
      final d = i * 0.00005; // ~5m par étape
      return LatLng(_pos.latitude + d, _pos.longitude + d);
    });
  }

  // ! Simule le déplacement du coureur toutes les 0.5s et recentre la carte
  void _startSimulation() {
    Timer.periodic(const Duration(milliseconds: 500), (timer) {
      if (!mounted || _pathIndex >= _simulatedPath.length) {
        timer.cancel(); // Stoppe la simulation à la fin du parcours
        return;
      }
      setState(() {
        _pos = _simulatedPath[_pathIndex++]; // Avance sur le parcours
        _visitedPath.add(_pos); // Ajoute au chemin parcouru
        _mapController.move(_pos, _mapController.zoom); // Recentre la carte
      });
    });
  }

  //! Formate les secondes en HH:MM:SS
  String _t(int n) => n.toString().padLeft(2, '0');
  String _time() {
    final h = _sec ~/ 3600, m = (_sec % 3600) ~/ 60, s = _sec % 60;
    return "${_t(h)}:${_t(m)}:${_t(s)}";
  }

  @override
  void dispose() {
    _timer.cancel(); // Stoppe le timer quand on quitte l'écran
    super.dispose();
  }

  @override
  Widget build(BuildContext ctx) {
    return Scaffold(
      backgroundColor: const Color(0xFF0074BD),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              Center(
                child: Image.asset(
                  "assets/image/running.png",
                  width: 100,
                ), // Illustration en haut
              ),
              const SizedBox(height: 30),
              //! Temps écoulé et calories brûlées
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Text(
                    _time(),
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 26,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  Text(
                    "$_cal calories",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 26,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 30),
              // ! Vitesse max / moyenne
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Text(
                    "Vitesse max:\n${_vMax.toStringAsFixed(1)} km/h",
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white, fontSize: 20),
                  ),
                  Text(
                    "Vitesse moy:\n${_vAvg.toStringAsFixed(1)} km/h",
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white, fontSize: 20),
                  ),
                ],
              ),
              const SizedBox(height: 30),
              //! Carte avec suivi dynamique du curseur + tracé du parcours
              SizedBox(
                height: 260,
                width: double.infinity,
                child: FlutterMap(
                  mapController: _mapController,
                  options: MapOptions(
                    center: _pos,
                    zoom: 15.0,
                    interactiveFlags: InteractiveFlag.all,
                  ),
                  children: [
                    TileLayer(
                      urlTemplate:
                          'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                      subdomains: ['a', 'b', 'c'],
                    ),
                    PolylineLayer(
                      polylines: [
                        Polyline(
                          points: _visitedPath,
                          strokeWidth: 4,
                          color: Colors.blue,
                        ),
                      ],
                    ),
                    MarkerLayer(
                      markers: [
                        Marker(
                          point: _pos,
                          builder:
                              (ctx) => Center(
                                child: Container(
                                  width: 12,
                                  height: 12,
                                  decoration: BoxDecoration(
                                    color: Colors.blue,
                                    shape: BoxShape.circle,
                                  ),
                                ),
                              ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 30),
              //! Bouton pour terminer la course
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.grey[300],
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(
                    horizontal: 30,
                    vertical: 15,
                  ),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                ),
                onPressed: () {
                  final run = RunHistory(
                    duration: _time(),
                    calories: _cal,
                    vitesseMax: _vMax,
                    vitesseMoy: _vAvg,
                  );
                  Navigator.pop(
                    context,
                    run,
                  ); //! Retourne les infos de la course
                },
                child: const Text(
                  "Terminer la course",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
