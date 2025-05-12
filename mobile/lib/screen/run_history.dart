class RunHistory {
  final String duration; // ex : "00:32:15"
  final int calories; // ex : 187
  final double vitesseMax; // km/h
  final double vitesseMoy; // km/h

  RunHistory({
    required this.duration,
    required this.calories,
    required this.vitesseMax,
    required this.vitesseMoy,
  });
}
