<?php
// db_check.php v0.1.10 (2025-08-19)
$expectedVersion = 'v0.1.7';
$dsn = sprintf('pgsql:host=%s;port=%s;dbname=%s',
    getenv('DB_HOST') ?: 'localhost',
    getenv('DB_PORT') ?: '5432',
    getenv('DB_NAME') ?: 'cashmachiine');
$user = getenv('DB_USER') ?: 'postgres';
$pass = getenv('DB_PASS') ?: '';
$requiredTables = [
    'users','goals','accounts','portfolios','positions','orders',
    'executions','prices','signals','actions','risk_limits','metrics_daily',
    'backtests','risk_stress_results','notifications','strategies','strategy_reviews'
];
$warehouseTables = ['dw_orders','dw_positions'];
$priceColumns = ['symbol','venue','ts','o','h','l','c','v'];
try {
    $pdo = new PDO($dsn, $user, $pass, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
} catch (Exception $e) {
    echo "Connection failed: {$e->getMessage()}\n";
    exit(1);
}
foreach ($requiredTables as $tbl) {
    $stmt = $pdo->query("SELECT to_regclass('public.$tbl')");
    if (!$stmt->fetchColumn()) {
        echo "Missing table: $tbl\n";
        exit(1);
    }
}
foreach ($warehouseTables as $tbl) {
    $stmt = $pdo->query("SELECT to_regclass('warehouse.$tbl')");
    if (!$stmt->fetchColumn()) {
        echo "Missing warehouse table: $tbl\n";
        exit(1);
    }
}
$tenantTables = ['users','goals','orders'];
foreach ($tenantTables as $tbl) {
    $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='$tbl'");
    $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
    if (!in_array('tenant_id', $cols)) {
        echo "Missing column in $tbl: tenant_id\n";
        exit(1);
    }
}
$currencyTables = ['accounts','orders','positions','executions'];
foreach ($currencyTables as $tbl) {
    $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='$tbl'");
    $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
    if (!in_array('currency', $cols)) {
        echo "Missing column in $tbl: currency\n";
        exit(1);
    }
}
$stmt = $pdo->query("SELECT extname FROM pg_extension WHERE extname='timescaledb'");
if (!$stmt->fetchColumn()) {
    echo "Missing extension: timescaledb\n";
    exit(1);
}
$stmt = $pdo->query("SELECT 1 FROM timescaledb_information.hypertables WHERE hypertable_name='prices'");
if (!$stmt->fetchColumn()) {
    echo "prices table is not a hypertable\n";
    exit(1);
}
$stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='prices'");
$cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
foreach ($priceColumns as $col) {
    if (!in_array($col, $cols)) {
        echo "Missing column in prices: $col\n";
        exit(1);
    }
}

$metricsColumns = ['date','requests','errors'];
$stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='metrics_daily'");
$cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
foreach ($metricsColumns as $col) {
    if (!in_array($col, $cols)) {
        echo "Missing column in metrics_daily: $col\n";
        exit(1);
    }
}

$backtestColumns = ['id','cfg_json','start','end','kpis_json','report_path'];
$stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='backtests'");
$cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($backtestColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in backtests: $col\n";
          exit(1);
      }
  }
  $stressColumns = ['id','scenario','metric','created_at'];
  $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='risk_stress_results'");
  $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($stressColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in risk_stress_results: $col\n";
          exit(1);
      }
  }
  $notificationColumns = ['id','user_id','channel','payload','created_at'];
  $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='notifications'");
  $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($notificationColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in notifications: $col\n";
          exit(1);
      }
  }
  $strategyColumns = ['id','name','description','file_path','uploaded_at'];
  $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='strategies'");
  $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($strategyColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in strategies: $col\n";
          exit(1);
      }
  }
  $reviewColumns = ['id','strategy_id','rating','comment','created_at'];
  $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='strategy_reviews'");
  $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($reviewColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in strategy_reviews: $col\n";
          exit(1);
      }
  }
$schemaVersion = getenv('DB_SCHEMA_VERSION') ?: 'unknown';
if ($schemaVersion !== $expectedVersion) {
    echo "Schema version mismatch: expected $expectedVersion, got $schemaVersion\n";
    exit(1);
}
echo "Database connection and schema ok.\n";
