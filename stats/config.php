<?php
declare(strict_types=1);

define('ITD_STATS_ADMIN_KEY', (string) (getenv('ITD_STATS_ADMIN_KEY') ?: ''));
define('ITD_STATS_SECRET', (string) (getenv('ITD_STATS_SECRET') ?: ''));

if (ITD_STATS_ADMIN_KEY === '' || ITD_STATS_SECRET === '') {
    itd_stats_json(['ok' => false, 'error' => 'configuration_required'], 503);
}
const ITD_STATS_MAX_EVENTS = 5000;
const ITD_STATS_STORAGE_DIR = __DIR__ . '/storage';
const ITD_STATS_EVENT_FILE = ITD_STATS_STORAGE_DIR . '/events.jsonl';

function itd_stats_json(array $payload, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('X-Robots-Tag: noindex, nofollow, noarchive');
    echo json_encode($payload, JSON_UNESCAPED_SLASHES);
    exit;
}

function itd_stats_storage_ready(): void
{
    if (!is_dir(ITD_STATS_STORAGE_DIR)) {
        mkdir(ITD_STATS_STORAGE_DIR, 0755, true);
    }
}

function itd_stats_clean_string($value, int $max = 180): string
{
    $value = is_scalar($value) ? (string) $value : '';
    $value = preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $value) ?? '';
    $value = trim(preg_replace('/\s+/u', ' ', strip_tags($value)) ?? '');
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $max);
    }
    return substr($value, 0, $max);
}

function itd_stats_hash(string $value): string
{
    return hash_hmac('sha256', $value, ITD_STATS_SECRET);
}

function itd_stats_client_ip(): string
{
    $candidates = [
        (string) ($_SERVER['HTTP_CF_CONNECTING_IP'] ?? ''),
        (string) ($_SERVER['HTTP_X_REAL_IP'] ?? ''),
        (string) ($_SERVER['REMOTE_ADDR'] ?? ''),
    ];
    $forwarded = (string) ($_SERVER['HTTP_X_FORWARDED_FOR'] ?? '');
    if ($forwarded !== '') {
        array_unshift($candidates, trim(explode(',', $forwarded)[0]));
    }
    foreach ($candidates as $candidate) {
        $candidate = trim($candidate);
        if ($candidate !== '' && filter_var($candidate, FILTER_VALIDATE_IP)) {
            return $candidate;
        }
    }
    return '';
}

function itd_stats_country_name(string $code): string
{
    $countries = [
        'XK' => 'Kosovo',
        'AL' => 'Albania',
        'DE' => 'Germany',
        'CH' => 'Switzerland',
        'AT' => 'Austria',
        'US' => 'United States',
        'GB' => 'United Kingdom',
        'IT' => 'Italy',
        'FR' => 'France',
        'NL' => 'Netherlands',
        'BE' => 'Belgium',
        'SE' => 'Sweden',
        'NO' => 'Norway',
        'DK' => 'Denmark',
        'FI' => 'Finland',
        'MK' => 'North Macedonia',
        'ME' => 'Montenegro',
        'RS' => 'Serbia',
        'BA' => 'Bosnia and Herzegovina',
        'HR' => 'Croatia',
        'SI' => 'Slovenia',
        'TR' => 'Turkey',
        'GR' => 'Greece',
        'BG' => 'Bulgaria',
        'RO' => 'Romania',
        'ES' => 'Spain',
        'PT' => 'Portugal',
        'PL' => 'Poland',
        'CZ' => 'Czechia',
        'HU' => 'Hungary',
        'IE' => 'Ireland',
        'CA' => 'Canada',
        'AU' => 'Australia',
        'EU' => 'Europe',
    ];
    return $countries[$code] ?? $code;
}

function itd_stats_detect_country_code(): string
{
    $headers = [
        'HTTP_CF_IPCOUNTRY',
        'HTTP_CLOUDFRONT_VIEWER_COUNTRY',
        'HTTP_X_COUNTRY_CODE',
        'HTTP_X_GEO_COUNTRY',
        'HTTP_X_FORWARDED_COUNTRY',
        'HTTP_X_HCDN_COUNTRY',
        'GEOIP_COUNTRY_CODE',
    ];
    foreach ($headers as $header) {
        $value = strtoupper(trim((string) ($_SERVER[$header] ?? '')));
        if (preg_match('/^[A-Z]{2}$/', $value) && !in_array($value, ['XX', 'T1', 'A1', 'A2'], true)) {
            return $value;
        }
    }
    return '';
}

function itd_stats_allowed_request(): bool
{
    $allowed = ['itdks.tech', 'www.itdks.tech'];
    $host = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
    $origin = (string) ($_SERVER['HTTP_ORIGIN'] ?? '');
    $referer = (string) ($_SERVER['HTTP_REFERER'] ?? '');

    foreach ([$origin, $referer] as $source) {
        if ($source === '') {
            continue;
        }
        $sourceHost = strtolower((string) parse_url($source, PHP_URL_HOST));
        if ($sourceHost !== '' && !in_array($sourceHost, $allowed, true) && $sourceHost !== $host) {
            return false;
        }
    }
    return true;
}

function itd_stats_detect_device(string $agent): string
{
    if (preg_match('/bot|crawl|spider|slurp|bingpreview/i', $agent)) {
        return 'bot';
    }
    if (preg_match('/mobile|android|iphone|ipod/i', $agent)) {
        return 'mobile';
    }
    if (preg_match('/ipad|tablet/i', $agent)) {
        return 'tablet';
    }
    return 'desktop';
}

function itd_stats_detect_browser(string $agent): string
{
    if (preg_match('/Edg\//i', $agent)) {
        return 'Edge';
    }
    if (preg_match('/Chrome\//i', $agent)) {
        return 'Chrome';
    }
    if (preg_match('/Safari\//i', $agent) && !preg_match('/Chrome\//i', $agent)) {
        return 'Safari';
    }
    if (preg_match('/Firefox\//i', $agent)) {
        return 'Firefox';
    }
    return 'Other';
}

function itd_stats_read_events(int $limit = ITD_STATS_MAX_EVENTS): array
{
    if (!is_file(ITD_STATS_EVENT_FILE)) {
        return [];
    }
    $lines = file(ITD_STATS_EVENT_FILE, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    if (!$lines) {
        return [];
    }
    $lines = array_slice($lines, -$limit);
    $events = [];
    foreach ($lines as $line) {
        $event = json_decode($line, true);
        if (is_array($event)) {
            $events[] = $event;
        }
    }
    return $events;
}

function itd_stats_count_map(array $items, string $key, int $limit = 8): array
{
    $counts = [];
    foreach ($items as $item) {
        $value = $item;
        foreach (explode('.', $key) as $part) {
            if (!is_array($value) || !array_key_exists($part, $value)) {
                $value = '';
                break;
            }
            $value = $value[$part];
        }
        $value = itd_stats_clean_string($value, 120);
        if ($value === '') {
            $value = 'Unknown';
        }
        $counts[$value] = ($counts[$value] ?? 0) + 1;
    }
    arsort($counts);
    return array_slice($counts, 0, $limit, true);
}
