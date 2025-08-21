<?php
// db_check.php v0.1.23 (2025-08-22)
$expectedVersion = 'v0.1.7';
$dbname = getenv('DB_NAME') ?: 'cashmachiine';
$dsn = sprintf('pgsql:host=%s;port=%s;dbname=%s',
    getenv('DB_HOST') ?: 'localhost',
    getenv('DB_PORT') ?: '5432',
    $dbname);
$user = getenv('DB_USER') ?: 'postgres';
$pass = getenv('DB_PASS') ?: '';
$requiredTables = [
    'users','goals','accounts','portfolios','positions','orders',
    'executions','prices','signals','actions','risk_limits','metrics_daily',
    'backtests','risk_stress_results','notifications','alerts','strategies','strategy_reviews','audit_events','scenario_results','risk_anomalies','macro_indicators'
];
$warehouseTables = ['dw_orders','dw_positions'];
$seedTables = ['demo_users','demo_accounts'];
$priceColumns = ['symbol','venue','ts','o','h','l','c','v'];
try {
    $pdo = new PDO($dsn, $user, $pass, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
} catch (Exception $e) {
    echo "Connection failed: {$e->getMessage()}\n";
    exit(1);
}
$roleStmt = $pdo->query("SELECT 1 FROM pg_roles WHERE rolname='{$user}'");
if (!$roleStmt->fetchColumn()) {
    echo "Missing role: {$user}\n";
    exit(1);
}
$privStmt = $pdo->query("SELECT has_database_privilege('{$user}', '{$dbname}', 'CONNECT')");
if (!$privStmt->fetchColumn()) {
    echo "User {$user} lacks CONNECT privilege on {$dbname}\n";
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
$tenantTables = ['users','goals','orders','audit_events'];
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
$costTables = ['orders','executions'];
foreach ($costTables as $tbl) {
    $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='$tbl'");
    $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
    foreach (['fee','tax'] as $col) {
        if (!in_array($col, $cols)) {
            echo "Missing column in $tbl: $col\n";
            exit(1);
        }
    }
}
$stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='users'");
$cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
foreach (['kyc_level','oauth_provider','oauth_sub','totp_secret','backup_codes'] as $col) {
    if (!in_array($col, $cols)) {
        echo "Missing column in users: $col\n";
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
  $alertColumns = ['id','notification_id','created_at'];
  $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='alerts'");
  $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($alertColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in alerts: $col\n";
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
  $scenarioColumns = ['id','name','input','result','created_at'];
  $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='scenario_results'");
  $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($scenarioColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in scenario_results: $col\n";
          exit(1);
      }
  }
  $riskAnomalyColumns = ['id','metric_date','portfolio_id','metric','value','score','created_at'];
  $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='risk_anomalies'");
  $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($riskAnomalyColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in risk_anomalies: $col\n";
          exit(1);
      }
  }
  $macroColumns = ['id','indicator','source','value','ts'];
  $stmt = $pdo->query("SELECT column_name FROM information_schema.columns WHERE table_name='macro_indicators'");
  $cols = $stmt->fetchAll(PDO::FETCH_COLUMN);
  foreach ($macroColumns as $col) {
      if (!in_array($col, $cols)) {
          echo "Missing column in macro_indicators: $col\n";
          exit(1);
      }
    }
  foreach ($seedTables as $tbl) {
      $stmt = $pdo->query("SELECT to_regclass('public.$tbl')");
      if (!$stmt->fetchColumn()) {
          echo "Missing seed table: $tbl\n";
          exit(1);
      }
  }
  $demoCount = $pdo->query("SELECT COUNT(*) FROM demo_users")->fetchColumn();
  if ($demoCount == 0) {
      echo "Missing demo data in demo_users\n";
      exit(1);
  }
  $demoAcctCount = $pdo->query("SELECT COUNT(*) FROM demo_accounts")->fetchColumn();
  if ($demoAcctCount == 0) {
      echo "Missing demo data in demo_accounts\n";
      exit(1);
  }
    $adminEmail = 'admin@cashmachiine.local';
    $adminStmt = $pdo->prepare("SELECT COUNT(*) FROM users WHERE email=? AND role='admin'");
    $adminStmt->execute([$adminEmail]);
    if ($adminStmt->fetchColumn() == 0) {
        echo "Missing admin user: $adminEmail\n";
        exit(1);
    }
  $schemaVersion = getenv('DB_SCHEMA_VERSION') ?: 'unknown';
if ($schemaVersion !== $expectedVersion) {
    echo "Schema version mismatch: expected $expectedVersion, got $schemaVersion\n";
    exit(1);
}
echo "Database connection and schema ok.\n";
