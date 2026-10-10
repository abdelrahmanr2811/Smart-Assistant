class KpiModel {
  final String projectName;
  final String period;
  final double plannedValue;
  final double earnedValue;
  final double actualCost;
  final double spi;
  final double cpi;
  final double scheduleVariance;
  final double costVariance;
  final String scheduleStatus;
  final String costStatus;
  final String commentary;

  KpiModel({
    required this.projectName,
    required this.period,
    required this.plannedValue,
    required this.earnedValue,
    required this.actualCost,
    required this.spi,
    required this.cpi,
    required this.scheduleVariance,
    required this.costVariance,
    required this.scheduleStatus,
    required this.costStatus,
    required this.commentary,
  });

  factory KpiModel.fromJson(Map<String, dynamic> json) {
    return KpiModel(
      projectName: json['project_name'] ?? 'Construction Project',
      period: json['period'] ?? 'Baseline',
      plannedValue: (json['planned_value'] as num?)?.toDouble() ?? 0.0,
      earnedValue: (json['earned_value'] as num?)?.toDouble() ?? 0.0,
      actualCost: (json['actual_cost'] as num?)?.toDouble() ?? 0.0,
      spi: (json['schedule_performance_index'] as num?)?.toDouble() ?? 1.0,
      cpi: (json['cost_performance_index'] as num?)?.toDouble() ?? 1.0,
      scheduleVariance: (json['schedule_variance'] as num?)?.toDouble() ?? 0.0,
      costVariance: (json['cost_variance'] as num?)?.toDouble() ?? 0.0,
      scheduleStatus: json['schedule_status'] ?? 'On Track',
      costStatus: json['cost_status'] ?? 'On Budget',
      commentary: json['commentary'] ?? '',
    );
  }
}
