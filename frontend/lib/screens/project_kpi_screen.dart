import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../core/theme/app_theme.dart';
import '../providers/kpi_provider.dart';
import '../widgets/kpi_metric_card.dart';

class ProjectKpiScreen extends ConsumerWidget {
  const ProjectKpiScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final kpiState = ref.watch(kpiProvider);
    final currencyFmt = NumberFormat.currency(symbol: '\$', decimalDigits: 0);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Project Controls & EVM Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh KPIs',
            onPressed: () => ref.read(kpiProvider.notifier).fetchKpis(),
          ),
        ],
      ),
      body: kpiState.isLoading
          ? const Center(child: CircularProgressIndicator(color: AppTheme.accent))
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAlignment.start,
                children: [
                  // Project Header Card
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFF1E3A8A), Color(0xFF1E293B)],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(18),
                      border: Border.all(color: const Color(0xFF3B82F6).withOpacity(0.4)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              kpiState.kpis?.projectName ?? 'Construction Project',
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(
                                color: AppTheme.accent.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: AppTheme.accent, width: 0.8),
                              ),
                              child: Text(
                                kpiState.kpis?.period ?? 'Current Baseline',
                                style: const TextStyle(fontSize: 12, color: AppTheme.accent, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Text(
                          kpiState.kpis?.commentary ?? 'Primavera P6 baseline active. Earned value tracking in progress.',
                          style: const TextStyle(fontSize: 13.5, color: Color(0xFFCBD5E1), height: 1.4),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),
                  const Text(
                    'Performance Indices (EVM)',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.darkTextPrimary),
                  ),
                  const SizedBox(height: 12),

                  // 2-Column KPI grid
                  GridView.count(
                    crossAxisCount: MediaQuery.of(context).size.width > 900 ? 4 : (MediaQuery.of(context).size.width > 600 ? 2 : 1),
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 14,
                    mainAxisSpacing: 14,
                    childAspectRatio: 1.6,
                    children: [
                      // SPI
                      KpiMetricCard(
                        title: 'Schedule Index (SPI = EV/PV)',
                        value: (kpiState.kpis?.spi ?? 1.0).toStringAsFixed(3),
                        subtitle: kpiState.kpis?.scheduleStatus,
                        icon: Icons.speed,
                        statusColor: (kpiState.kpis?.spi ?? 1.0) >= 1.0 ? AppTheme.success : AppTheme.accent,
                        badgeText: (kpiState.kpis?.spi ?? 1.0) >= 1.0 ? 'Ahead' : 'Delayed',
                      ),
                      // CPI
                      KpiMetricCard(
                        title: 'Cost Index (CPI = EV/AC)',
                        value: (kpiState.kpis?.cpi ?? 1.0).toStringAsFixed(3),
                        subtitle: kpiState.kpis?.costStatus,
                        icon: Icons.monetization_on_outlined,
                        statusColor: (kpiState.kpis?.cpi ?? 1.0) >= 1.0 ? AppTheme.success : AppTheme.accent,
                        badgeText: (kpiState.kpis?.cpi ?? 1.0) >= 1.0 ? 'Under Budget' : 'Over Budget',
                      ),
                      // Planned Value
                      KpiMetricCard(
                        title: 'Planned Value (PV)',
                        value: currencyFmt.format(kpiState.kpis?.plannedValue ?? 0),
                        subtitle: 'Baseline Target to Date',
                        icon: Icons.calendar_today,
                        statusColor: AppTheme.primary,
                      ),
                      // Earned Value
                      KpiMetricCard(
                        title: 'Earned Value (EV)',
                        value: currencyFmt.format(kpiState.kpis?.earnedValue ?? 0),
                        subtitle: 'Value of Work Performed',
                        icon: Icons.task_alt,
                        statusColor: AppTheme.info,
                      ),
                    ],
                  ),

                  const SizedBox(height: 20),
                  const Text(
                    'Cost & Schedule Variances',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.darkTextPrimary),
                  ),
                  const SizedBox(height: 12),

                  GridView.count(
                    crossAxisCount: MediaQuery.of(context).size.width > 700 ? 3 : 1,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 14,
                    mainAxisSpacing: 14,
                    childAspectRatio: 1.8,
                    children: [
                      // Actual Cost
                      KpiMetricCard(
                        title: 'Actual Cost (AC)',
                        value: currencyFmt.format(kpiState.kpis?.actualCost ?? 0),
                        subtitle: 'Incurred Expenditures',
                        icon: Icons.receipt_long,
                        statusColor: AppTheme.accentOrange,
                      ),
                      // Schedule Variance
                      KpiMetricCard(
                        title: 'Schedule Variance (SV = EV - PV)',
                        value: currencyFmt.format(kpiState.kpis?.scheduleVariance ?? 0),
                        subtitle: (kpiState.kpis?.scheduleVariance ?? 0) >= 0 ? 'Favorable Variance' : 'Critical Path Delay',
                        icon: Icons.compare_arrows,
                        statusColor: (kpiState.kpis?.scheduleVariance ?? 0) >= 0 ? AppTheme.success : AppTheme.danger,
                      ),
                      // Cost Variance
                      KpiMetricCard(
                        title: 'Cost Variance (CV = EV - AC)',
                        value: currencyFmt.format(kpiState.kpis?.costVariance ?? 0),
                        subtitle: (kpiState.kpis?.costVariance ?? 0) >= 0 ? 'Under Budget' : 'Cost Overrun',
                        icon: Icons.account_balance_wallet,
                        statusColor: (kpiState.kpis?.costVariance ?? 0) >= 0 ? AppTheme.success : AppTheme.danger,
                      ),
                    ],
                  ),
                ],
              ),
            ),
    );
  }
}
