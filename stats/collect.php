<?php
declare(strict_types=1);

require __DIR__ . '/config.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    itd_stats_json(['ok' => false, 'error' => 'method_not_allowed'], 405);
}

if (!itd_stats_allowed_request()) {
    itd_stats_json(['ok' => false, 'error' => 'origin_not_allowed'], 403);
}

$raw = file_get_contents('php://input');
if ($raw === false || strlen($raw) > 20000) {
    itd_stats_json(['ok' => false, 'error' => 'invalid_payload'], 400);
}

$data = json_decode($raw, true);
if (!is_array($data)) {
    itd_stats_json(['ok' => false, 'error' => 'invalid_json'], 400);
}

$eventName = itd_stats_clean_string($data['event'] ?? '', 64);
if ($eventName === '') {
    itd_stats_json(['ok' => false, 'error' => 'missing_event'], 400);
}

$path = itd_stats_clean_string($data['path'] ?? '/', 220);
if ($path === '' || $path[0] !== '/') {
    $path = '/';
}

$agent = (string) ($_SERVER['HTTP_USER_AGENT'] ?? '');
$visitorSeed = itd_stats_clean_string($data['visitor_id'] ?? '', 220);
$sessionSeed = itd_stats_clean_string($data['session_id'] ?? '', 220);
$ip = itd_stats_client_ip();
$countryCode = itd_stats_detect_country_code();
$localeCountry = strtoupper(itd_stats_clean_string($data['locale_country_hint'] ?? '', 2));
if (!preg_match('/^[A-Z]{2}$/', $localeCountry)) {
    $localeCountry = '';
}
$countryName = $countryCode !== '' ? itd_stats_country_name($countryCode) : '';
if ($countryName === '' && $localeCountry !== '') {
    $countryName = itd_stats_country_name($localeCountry) . ' (locale)';
}
$referrer = itd_stats_clean_string($data['referrer'] ?? '', 300);
$referrerHost = $referrer !== '' ? strtolower((string) parse_url($referrer, PHP_URL_HOST)) : '';
$sameSiteReferrer = in_array($referrerHost, ['itdks.tech', 'www.itdks.tech'], true);

$details = [
    'label' => itd_stats_clean_string($data['label'] ?? '', 160),
    'href' => itd_stats_clean_string($data['href'] ?? '', 220),
    'destination_host' => itd_stats_clean_string($data['destination_host'] ?? '', 120),
    'service' => itd_stats_clean_string($data['service'] ?? '', 120),
    'package' => itd_stats_clean_string($data['package'] ?? '', 120),
    'form_id' => itd_stats_clean_string($data['form_id'] ?? '', 100),
    'message' => itd_stats_clean_string($data['message'] ?? '', 160),
    'depth' => (int) ($data['depth'] ?? 0),
];

$record = [
    'server_time' => gmdate('c'),
    'event' => $eventName,
    'path' => $path,
    'title' => itd_stats_clean_string($data['title'] ?? '', 180),
    'language' => itd_stats_clean_string($data['language'] ?? '', 20),
    'page_type' => itd_stats_clean_string($data['page_type'] ?? '', 80),
    'utm_source' => itd_stats_clean_string($data['utm_source'] ?? '', 120),
    'utm_campaign' => itd_stats_clean_string($data['utm_campaign'] ?? '', 120),
    'referrer_host' => $sameSiteReferrer ? '' : itd_stats_clean_string($referrerHost, 120),
    'country_code' => $countryCode,
    'country_name' => $countryName,
    'locale_country_code' => $localeCountry,
    'locale_country_name' => $localeCountry !== '' ? itd_stats_country_name($localeCountry) : '',
    'visitor_hash' => itd_stats_hash(($visitorSeed !== '' ? $visitorSeed : $ip) . '|' . $ip),
    'session_hash' => itd_stats_hash(($sessionSeed !== '' ? $sessionSeed : $visitorSeed) . '|' . $ip),
    'device' => itd_stats_detect_device($agent),
    'browser' => itd_stats_detect_browser($agent),
    'browser_language' => itd_stats_clean_string($data['browser_language'] ?? '', 40),
    'browser_languages' => itd_stats_clean_string($data['browser_languages'] ?? '', 120),
    'timezone' => itd_stats_clean_string($data['timezone'] ?? '', 80),
    'timezone_offset' => max(-1440, min(1440, (int) ($data['timezone_offset'] ?? 0))),
    'platform' => itd_stats_clean_string($data['platform'] ?? '', 80),
    'connection_type' => itd_stats_clean_string($data['connection_type'] ?? '', 40),
    'save_data' => (bool) ($data['save_data'] ?? false),
    'color_scheme' => itd_stats_clean_string($data['color_scheme'] ?? '', 20),
    'viewport' => itd_stats_clean_string($data['viewport'] ?? '', 40),
    'screen' => itd_stats_clean_string($data['screen'] ?? '', 40),
    'seconds_on_page' => max(0, min(86400, (int) ($data['seconds_on_page'] ?? 0))),
    'details' => array_filter($details, static function ($value) {
        return $value !== '' && $value !== 0;
    }),
];

itd_stats_storage_ready();

$line = json_encode($record, JSON_UNESCAPED_SLASHES) . PHP_EOL;
$handle = fopen(ITD_STATS_EVENT_FILE, 'ab');
if (!$handle) {
    itd_stats_json(['ok' => false, 'error' => 'storage_unavailable'], 500);
}

flock($handle, LOCK_EX);
fwrite($handle, $line);
flock($handle, LOCK_UN);
fclose($handle);

if (is_file(ITD_STATS_EVENT_FILE) && filesize(ITD_STATS_EVENT_FILE) > 5242880) {
    $events = itd_stats_read_events(ITD_STATS_MAX_EVENTS);
    $trimmed = array_map(static function (array $event): string {
        return json_encode($event, JSON_UNESCAPED_SLASHES);
    }, $events);
    file_put_contents(ITD_STATS_EVENT_FILE, implode(PHP_EOL, $trimmed) . PHP_EOL, LOCK_EX);
}

itd_stats_json(['ok' => true]);
