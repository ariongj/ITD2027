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

function itd_summary_percent(int $part, int $whole): int
{
    return $whole > 0 ? (int) round(($part / $whole) * 100) : 0;
}

function itd_summary_sessions(array $events, array $ctaEvents): array
{
    $sessions = [];
    foreach ($events as $event) {
        $hash = (string) ($event['session_hash'] ?? '');
        if ($hash === '') {
            continue;
        }
        $time = strtotime((string) ($event['server_time'] ?? '')) ?: 0;
        if (!isset($sessions[$hash])) {
            $sessions[$hash] = [
                'first' => $time,
                'last' => $time,
                'events' => 0,
                'pageviews' => 0,
                'ctas' => 0,
                'seconds' => 0,
                'paths' => [],
            ];
        }
        $sessions[$hash]['first'] = min($sessions[$hash]['first'], $time);
        $sessions[$hash]['last'] = max($sessions[$hash]['last'], $time);
        $sessions[$hash]['events']++;
        $sessions[$hash]['seconds'] = max($sessions[$hash]['seconds'], (int) ($event['seconds_on_page'] ?? 0));
        $path = itd_stats_clean_string($event['path'] ?? '', 220);
        if ($path !== '') {
            $sessions[$hash]['paths'][$path] = true;
        }
        if (($event['event'] ?? '') === 'page_view') {
            $sessions[$hash]['pageviews']++;
        }
        if (in_array((string) ($event['event'] ?? ''), $ctaEvents, true)) {
            $sessions[$hash]['ctas']++;
        }
    }
    return $sessions;
}

function itd_summary_session_metric(array $sessions): array
{
    $count = count($sessions);
    $withCta = 0;
    $bounces = 0;
    $seconds = 0;
    foreach ($sessions as $session) {
        if (($session['ctas'] ?? 0) > 0) {
            $withCta++;
        }
        if (($session['pageviews'] ?? 0) <= 1 && ($session['ctas'] ?? 0) === 0) {
            $bounces++;
        }
        $seconds += (int) ($session['seconds'] ?? 0);
    }
    return [
        'sessions' => $count,
        'sessions_with_cta' => $withCta,
        'conversion_rate' => itd_summary_percent($withCta, $count),
        'bounce_rate' => itd_summary_percent($bounces, $count),
        'avg_session_seconds' => $count > 0 ? (int) round($seconds / $count) : 0,
    ];
}

function itd_summary_hourly(array $events, int $from): array
{
    $hours = [];
    for ($i = 23; $i >= 0; $i--) {
        $label = gmdate('H:00', time() - ($i * 3600));
        $hours[$label] = 0;
    }
    foreach ($events as $event) {
        $time = strtotime((string) ($event['server_time'] ?? '')) ?: 0;
        if ($time < $from) {
            continue;
        }
        $label = gmdate('H:00', $time);
        if (!isset($hours[$label])) {
            $hours[$label] = 0;
        }
        $hours[$label]++;
    }
    return $hours;
}

$events = itd_stats_read_events();
$now = time();
$dayAgo = $now - 86400;
$weekAgo = $now - 604800;
$ctaEvents = ['whatsapp_click', 'booking_click', 'email_click', 'phone_click', 'form_submit_attempt', 'form_submit_success', 'package_select'];

$events24h = [];
$events7d = [];
$visitor24h = [];
$visitor7d = [];
$visitorAll = [];
$pageViews24h = 0;
$pageViews7d = 0;
$cta24h = 0;

foreach ($events as $event) {
    $time = strtotime((string) ($event['server_time'] ?? '')) ?: 0;
    $visitor = (string) ($event['visitor_hash'] ?? '');
    if ($visitor !== '') {
        $visitorAll[$visitor] = true;
    }
    if ($time >= $weekAgo) {
        $events7d[] = $event;
        if ($visitor !== '') {
            $visitor7d[$visitor] = true;
        }
        if (($event['event'] ?? '') === 'page_view') {
            $pageViews7d++;
        }
    }
    if ($time >= $dayAgo) {
        $events24h[] = $event;
        if ($visitor !== '') {
            $visitor24h[$visitor] = true;
        }
        if (($event['event'] ?? '') === 'page_view') {
            $pageViews24h++;
        }
        if (in_array((string) ($event['event'] ?? ''), $ctaEvents, true)) {
            $cta24h++;
        }
    }
}

$sessionMetrics24h = itd_summary_session_metric(itd_summary_sessions($events24h, $ctaEvents));
$sessionMetrics7d = itd_summary_session_metric(itd_summary_sessions($events7d, $ctaEvents));

$latest = array_slice(array_reverse($events), 0, 120);
$latest = array_map(static function (array $event): array {
    return [
        'time' => $event['server_time'] ?? '',
        'event' => $event['event'] ?? '',
        'path' => $event['path'] ?? '',
        'title' => $event['title'] ?? '',
        'language' => $event['language'] ?? '',
        'browser_language' => $event['browser_language'] ?? '',
        'page_type' => $event['page_type'] ?? '',
        'country' => $event['country_name'] ?? '',
        'country_code' => $event['country_code'] ?? '',
        'timezone' => $event['timezone'] ?? '',
        'device' => $event['device'] ?? '',
        'browser' => $event['browser'] ?? '',
        'platform' => $event['platform'] ?? '',
        'connection_type' => $event['connection_type'] ?? '',
        'label' => $event['details']['label'] ?? '',
        'service' => $event['details']['service'] ?? '',
        'depth' => $event['details']['depth'] ?? '',
        'referrer_host' => $event['referrer_host'] ?? '',
        'utm_source' => $event['utm_source'] ?? '',
        'utm_campaign' => $event['utm_campaign'] ?? '',
        'seconds_on_page' => $event['seconds_on_page'] ?? 0,
    ];
}, $latest);

itd_stats_json([
    'ok' => true,
    'generated_at' => gmdate('c'),
    'totals' => [
        'events_all' => count($events),
        'visitors_all' => count($visitorAll),
        'events_24h' => count($events24h),
        'events_7d' => count($events7d),
        'visitors_24h' => count($visitor24h),
        'visitors_7d' => count($visitor7d),
        'pageviews_24h' => $pageViews24h,
        'pageviews_7d' => $pageViews7d,
        'cta_24h' => $cta24h,
        'sessions_24h' => $sessionMetrics24h['sessions'],
        'sessions_7d' => $sessionMetrics7d['sessions'],
        'conversion_rate_24h' => $sessionMetrics24h['conversion_rate'],
        'conversion_rate_7d' => $sessionMetrics7d['conversion_rate'],
        'bounce_rate_24h' => $sessionMetrics24h['bounce_rate'],
        'avg_session_seconds_24h' => $sessionMetrics24h['avg_session_seconds'],
    ],
    'top' => [
        'pages_24h' => itd_stats_count_map(array_filter($events24h, static function ($event) {
            return ($event['event'] ?? '') === 'page_view';
        }), 'path'),
        'events_24h' => itd_stats_count_map($events24h, 'event'),
        'cta_24h' => itd_stats_count_map(array_filter($events24h, static function ($event) use ($ctaEvents) {
            return in_array((string) ($event['event'] ?? ''), $ctaEvents, true);
        }), 'event'),
        'countries_7d' => itd_stats_count_map($events7d, 'country_name'),
        'timezones_7d' => itd_stats_count_map($events7d, 'timezone'),
        'devices_7d' => itd_stats_count_map($events7d, 'device'),
        'browsers_7d' => itd_stats_count_map($events7d, 'browser'),
        'platforms_7d' => itd_stats_count_map($events7d, 'platform'),
        'languages_7d' => itd_stats_count_map($events7d, 'browser_language'),
        'page_types_7d' => itd_stats_count_map($events7d, 'page_type'),
        'referrers_7d' => itd_stats_count_map(array_filter($events7d, static function ($event) {
            return ($event['referrer_host'] ?? '') !== '';
        }), 'referrer_host'),
        'utm_sources_7d' => itd_stats_count_map(array_filter($events7d, static function ($event) {
            return ($event['utm_source'] ?? '') !== '';
        }), 'utm_source'),
        'utm_campaigns_7d' => itd_stats_count_map(array_filter($events7d, static function ($event) {
            return ($event['utm_campaign'] ?? '') !== '';
        }), 'utm_campaign'),
        'connections_7d' => itd_stats_count_map($events7d, 'connection_type'),
    ],
    'hourly_24h' => itd_summary_hourly($events24h, $dayAgo),
    'latest' => $latest,
]);
