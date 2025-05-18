
import 'dart:async';
import 'dart:math';
import 'dart:math' as math show sin;
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'run_history.dart';

class RunReel extends StatefulWidget {
  const RunReel({super.key});

  @override
  State<RunReel> createState() => _RunReelState();
}

class _RunReelState extends State<RunReel> {
  late Timer _timer;
  final _rand = Random();
  final MapController _mapController = MapController();

  int _sec = 0;
  int _cal = 0;
  double _vMax = 0, _vAvg = 0;
  double _distance = 0; // Ajout pour calcul de distance

  LatLng _pos = LatLng(43.5287, 5.4456); // Aix-en-Provence
  List<LatLng> _simulatedPath = [];
  List<LatLng> _visitedPath = [];
  int _pathIndex = 0;
  final Distance _distanceCalc = Distance();

  @override
  void initState() {
    super.initState();
    _generateSimulatedPath();
    _visitedPath.add(_pos);
    _startTimer();
    _startSimulation();
  }

  void _startTimer() {
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (!mounted) return;
      setState(() {
        _sec++;
        if (_sec % 2 == 0) _cal++;
        _vMax = 8 + _rand.nextDouble() * 6;
        _vAvg = 5 + math.sin(_sec / 10) * 1.5;
      });
    });
  }

  void _generateSimulatedPath() {
    _simulatedPath = List.generate(4000, (i) {
      final d = i * 0.00005;
      return LatLng(_pos.latitude + d, _pos.longitude + d);
    });
  }

  void _startSimulation() {
    Timer.periodic(const Duration(milliseconds: 500), (timer) {
      if (!mounted || _pathIndex >= _simulatedPath.length) {
        timer.cancel();
        return;
      }

      final nextPos = _simulatedPath[_pathIndex++];
      final segmentDistance = _distanceCalc(_pos, nextPos);
      _distance += segmentDistance / 1000; // Convertir en km

      _pos = nextPos;
      _visitedPath.add(_pos);

      _mapController.move(_pos, 15.0);

      if (mounted) setState(() {});
    });
  }

  String _t(int n) => n.toString().padLeft(2, '0');
  String _time() {
    final h = _sec ~/ 3600, m = (_sec % 3600) ~/ 60, s = _sec % 60;
    return "${_t(h)}:${_t(m)}:${_t(s)}";
  }

  @override
  void dispose() {
    _timer.cancel();
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
                child: Image.asset("assets/image/running.png", width: 100),
              ),
              const SizedBox(height: 30),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Text(_time(), style: const TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.w600)),
                  Text("$_cal calories", style: const TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.w600)),
                ],
              ),
              const SizedBox(height: 30),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Text("Vitesse max:\n${_vMax.toStringAsFixed(1)} km/h", textAlign: TextAlign.center, style: const TextStyle(color: Colors.white, fontSize: 20)),
                  Text("Vitesse moy:\n${_vAvg.toStringAsFixed(1)} km/h", textAlign: TextAlign.center, style: const TextStyle(color: Colors.white, fontSize: 20)),
                ],
              ),
              const SizedBox(height: 30),
              SizedBox(
                height: 260,
                width: double.infinity,
                child: FlutterMap(
                  mapController: _mapController,
                  options: MapOptions(
                    center: _pos,
                    zoom: 15.0,
                    interactiveFlags: InteractiveFlag.none,
                    keepAlive: true,
                  ),
                  children: [
                    TileLayer(
                      urlTemplate: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
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
                          builder: (ctx) => Center(
                            child: Container(
                              width: 12,
                              height: 12,
                              decoration: const BoxDecoration(color: Colors.blue, shape: BoxShape.circle),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 30),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.grey[300],
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                ),
                onPressed: () {
                  final run = RunHistory(
                    distance: _distance,
                    duration: _time(),
                    calories: _cal,
                    vitesseMax: _vMax,
                    vitesseMoy: _vAvg,
                  );
                  Navigator.pop(context, run);
                },
                child: const Text("Terminer la course", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
