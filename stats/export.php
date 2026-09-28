<?php
declare(strict_types=1);

require __DIR__ . '/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    itd_stats_json(['ok' => false, 'error' => 'method_not_allowed'], 405);
}

$providedKey = (string) ($_GET['key'] ?? ($_SERVER['HTTP_X_ITD_STATS_KEY'] ?? ''));
if (!hash_equals(ITD_STATS_ADMIN_KEY, $providedKey)) {
    itd_stats_json(['ok' => false, 'error' => 'unauthorized'], 401);
}

$events = itd_stats_read_events();

header('Content-Type: text/csv; charset=utf-8');
header('Content-Disposition: attachment; filename="itd-stats-export-' . gmdate('Y-m-d') . '.csv"');
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
header('X-Robots-Tag: noindex, nofollow, noarchive');

$out = fopen('php://output', 'wb');
fputcsv($out, [
    'time',
    'event',
    'path',
    'title',
    'country',
    'country_code',
    'locale_country',
    'locale_country_code',
    'timezone',
    'language',
    'browser_language',
    'device',
    'browser',
    'platform',
    'connection_type',
    'referrer_host',
    'utm_source',
    'utm_campaign',
    'seconds_on_page',
    'label',
    'service',
    'depth',
]);

foreach ($events as $event) {
    fputcsv($out, [
        $event['server_time'] ?? '',
        $event['event'] ?? '',
        $event['path'] ?? '',
        $event['title'] ?? '',
        $event['country_name'] ?? '',
        $event['country_code'] ?? '',
        $event['locale_country_name'] ?? '',
        $event['locale_country_code'] ?? '',
        $event['timezone'] ?? '',
        $event['language'] ?? '',
        $event['browser_language'] ?? '',
        $event['device'] ?? '',
        $event['browser'] ?? '',
        $event['platform'] ?? '',
        $event['connection_type'] ?? '',
        $event['referrer_host'] ?? '',
        $event['utm_source'] ?? '',
        $event['utm_campaign'] ?? '',
        $event['seconds_on_page'] ?? '',
        $event['details']['label'] ?? '',
        $event['details']['service'] ?? '',
        $event['details']['depth'] ?? '',
    ]);
}

fclose($out);
