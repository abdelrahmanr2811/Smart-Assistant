import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/network/api_client.dart';
import '../models/kpi_model.dart';

class KpiState {
  final KpiModel? kpis;
  final bool isLoading;
  final String? errorMessage;

  KpiState({
    this.kpis,
    this.isLoading = false,
    this.errorMessage,
  });

  KpiState copyWith({
    KpiModel? kpis,
    bool? isLoading,
    String? errorMessage,
  }) {
    return KpiState(
      kpis: kpis ?? this.kpis,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage,
    );
  }
}

class KpiNotifier extends StateNotifier<KpiState> {
  final ApiClient _apiClient;

  KpiNotifier(this._apiClient) : super(KpiState()) {
    fetchKpis();
  }

  Future<void> fetchKpis() async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    try {
      final res = await _apiClient.getKpiSummary();
      if (res.statusCode == 200) {
        final model = KpiModel.fromJson(res.data);
        state = state.copyWith(kpis: model, isLoading: false);
      }
    } catch (e) {
      // Fallback default KPIs for offline demo
      state = state.copyWith(
        isLoading: false,
        kpis: KpiModel(
          projectName: 'New Administrative Capital Tower - Package B',
          period: 'October 2026 Baseline',
          plannedValue: 425000.0,
          earnedValue: 405000.0,
          actualCost: 410000.0,
          spi: 0.953,
          cpi: 0.988,
          scheduleVariance: -20000.0,
          costVariance: -5000.0,
          scheduleStatus: 'On Track (Minor Variance)',
          costStatus: 'On Budget',
          commentary: 'Project schedule is progressing on track with critical path foundation pouring active.',
        ),
      );
    }
  }
}

final kpiProvider = StateNotifierProvider<KpiNotifier, KpiState>((ref) {
  return KpiNotifier(ApiClient());
});
