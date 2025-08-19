<?php
// db_check.php v0.1.2 (2025-08-19)
$expectedVersion = 'v0.1.0';
$dsn = sprintf('pgsql:host=%s;port=%s;dbname=%s',
    getenv('DB_HOST') ?: 'localhost',
    getenv('DB_PORT') ?: '5432',
    getenv('DB_NAME') ?: 'cashmachiine');
$user = getenv('DB_USER') ?: 'postgres';
$pass = getenv('DB_PASS') ?: '';
$requiredTables = [
    'users','goals','accounts','portfolios','positions','orders',
    'executions','prices','signals','actions','risk_limits','metrics_daily','backtests'
];
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
$schemaVersion = getenv('DB_SCHEMA_VERSION') ?: 'unknown';
if ($schemaVersion !== $expectedVersion) {
    echo "Schema version mismatch: expected $expectedVersion, got $schemaVersion\n";
    exit(1);
}
echo "Database connection and schema ok.\n";
