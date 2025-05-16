class RunHistory {
  final double distance;       // en km
  final String duration;       // format "00:32:15"
  final int calories;          // kcal
  final double vitesseMax;     // en km/h
  final double vitesseMoy;     // en km/h

  RunHistory({
    required this.distance,
    required this.duration,
    required this.calories,
    required this.vitesseMax,
    required this.vitesseMoy,
  });
}
