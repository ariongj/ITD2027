<?php
declare(strict_types=1);

const ITD_CHAT_MAX_PAYLOAD_BYTES = 16000;
const ITD_CHAT_MAX_MESSAGE_CHARS = 1400;
const ITD_CHAT_MAX_HISTORY_ITEMS = 8;
const ITD_CHAT_RATE_WINDOW_SECONDS = 60;
const ITD_CHAT_RATE_MAX_REQUESTS = 12;
const ITD_CHAT_LOG_RETENTION_SECONDS = 1209600;
const ITD_CHAT_LOG_MAX_RECORDS = 1200;
const ITD_CHAT_STORAGE_DIR = __DIR__ . '/stats/storage';
const ITD_CHAT_LOG_FILE = ITD_CHAT_STORAGE_DIR . '/chat.jsonl';
const ITD_CHAT_RATE_FILE = ITD_CHAT_STORAGE_DIR . '/chat-rate.json';
const ITD_CHAT_DEFAULT_MODEL = 'gpt-6-luna';

function itd_chat_json(array $payload, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('X-Robots-Tag: noindex, nofollow, noarchive');
    echo json_encode($payload, JSON_UNESCAPED_SLASHES);
    exit;
}

function itd_chat_storage_ready(): void
{
    if (!is_dir(ITD_CHAT_STORAGE_DIR)) {
        mkdir(ITD_CHAT_STORAGE_DIR, 0755, true);
    }
}

function itd_chat_clean($value, int $max = 240): string
{
    $value = is_scalar($value) ? (string) $value : '';
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/u', ' ', $value) ?? '';
    $value = trim(preg_replace('/[ \t]+/u', ' ', strip_tags($value)) ?? '');

    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $max);
    }

    return substr($value, 0, $max);
}

function itd_chat_starts_with(string $value, string $prefix): bool
{
    return $prefix === '' || strpos($value, $prefix) === 0;
}

function itd_chat_ends_with(string $value, string $suffix): bool
{
    if ($suffix === '') {
        return true;
    }
    return substr($value, -strlen($suffix)) === $suffix;
}

function itd_chat_host_without_port(string $host): string
{
    $host = strtolower(trim($host));
    if (itd_chat_starts_with($host, '[')) {
        $end = strpos($host, ']');
        return $end === false ? $host : substr($host, 1, $end - 1);
    }
    return explode(':', $host)[0] ?? $host;
}

function itd_chat_allowed_request(): bool
{
    $allowedHosts = ['itdks.tech', 'www.itdks.tech', 'localhost', '127.0.0.1', '::1'];
    $requestHost = itd_chat_host_without_port((string) ($_SERVER['HTTP_HOST'] ?? ''));

    if ($requestHost !== '' && !in_array($requestHost, $allowedHosts, true)) {
        return false;
    }

    foreach (['HTTP_ORIGIN', 'HTTP_REFERER'] as $header) {
        $source = (string) ($_SERVER[$header] ?? '');
        if ($source === '') {
            continue;
        }
        $sourceHost = itd_chat_host_without_port((string) parse_url($source, PHP_URL_HOST));
        if ($sourceHost !== '' && $sourceHost !== $requestHost && !in_array($sourceHost, $allowedHosts, true)) {
            return false;
        }
    }

    return true;
}

function itd_chat_ip_in_cidr(string $ip, string $cidr): bool
{
    $cidr = trim($cidr);
    if ($cidr === '') {
        return false;
    }

    if (strpos($cidr, '/') === false) {
        return hash_equals($cidr, $ip);
    }

    [$network, $prefixText] = explode('/', $cidr, 2);
    $ipBytes = @inet_pton($ip);
    $networkBytes = @inet_pton(trim($network));
    if ($ipBytes === false || $networkBytes === false || strlen($ipBytes) !== strlen($networkBytes)) {
        return false;
    }

    $maxBits = strlen($ipBytes) * 8;
    if (!preg_match('/^\d+$/D', $prefixText)) {
        return false;
    }
    $prefix = (int) $prefixText;
    if ($prefix < 0 || $prefix > $maxBits) {
        return false;
    }

    $fullBytes = intdiv($prefix, 8);
    if ($fullBytes > 0 && substr($ipBytes, 0, $fullBytes) !== substr($networkBytes, 0, $fullBytes)) {
        return false;
    }

    $remainingBits = $prefix % 8;
    if ($remainingBits === 0) {
        return true;
    }

    $mask = (0xFF << (8 - $remainingBits)) & 0xFF;
    return (ord($ipBytes[$fullBytes]) & $mask) === (ord($networkBytes[$fullBytes]) & $mask);
}

function itd_chat_is_trusted_proxy(string $remoteAddress): bool
{
    if ($remoteAddress === '' || !filter_var($remoteAddress, FILTER_VALIDATE_IP)) {
        return false;
    }

    $configured = itd_chat_env_value('ITD_TRUSTED_PROXY_CIDRS');
    if ($configured === '') {
        return false;
    }

    $cidrs = preg_split('/[\s,]+/', $configured, -1, PREG_SPLIT_NO_EMPTY) ?: [];
    foreach ($cidrs as $cidr) {
        if (itd_chat_ip_in_cidr($remoteAddress, $cidr)) {
            return true;
        }
    }

    return false;
}

function itd_chat_client_ip(): string
{
    $remoteAddress = trim((string) ($_SERVER['REMOTE_ADDR'] ?? ''));
    if (!filter_var($remoteAddress, FILTER_VALIDATE_IP)) {
        $remoteAddress = '';
    }

    if (!itd_chat_is_trusted_proxy($remoteAddress)) {
        return $remoteAddress;
    }

    $candidates = [
        (string) ($_SERVER['HTTP_CF_CONNECTING_IP'] ?? ''),
        (string) ($_SERVER['HTTP_X_REAL_IP'] ?? ''),
        trim(explode(',', (string) ($_SERVER['HTTP_X_FORWARDED_FOR'] ?? ''))[0] ?? ''),
    ];
    foreach ($candidates as $candidate) {
        $candidate = trim($candidate);
        if ($candidate !== '' && filter_var($candidate, FILTER_VALIDATE_IP)) {
            return $candidate;
        }
    }

    return $remoteAddress;
}

function itd_chat_env_value(string $name): string
{
    $direct = getenv($name);
    if (is_string($direct) && trim($direct) !== '') {
        return trim($direct);
    }

    foreach ([$_ENV[$name] ?? '', $_SERVER[$name] ?? ''] as $candidate) {
        if (is_string($candidate) && trim($candidate) !== '') {
            return trim($candidate);
        }
    }

    foreach ([__DIR__ . '/.env.local', __DIR__ . '/.env'] as $path) {
        if (!is_file($path) || !is_readable($path)) {
            continue;
        }
        $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        if (!$lines) {
            continue;
        }
        foreach ($lines as $line) {
            $line = trim($line);
            if ($line === '' || $line[0] === '#') {
                continue;
            }
            if (!preg_match('/^' . preg_quote($name, '/') . '\s*=\s*(.+)$/', $line, $matches)) {
                continue;
            }
            $value = trim($matches[1]);
            if ((itd_chat_starts_with($value, '"') && itd_chat_ends_with($value, '"')) || (itd_chat_starts_with($value, "'") && itd_chat_ends_with($value, "'"))) {
                $value = substr($value, 1, -1);
            }
            return trim($value);
        }
    }

    return '';
}

function itd_chat_rate_allowed(string $clientKey): bool
{
    itd_chat_storage_ready();
    $now = time();
    $windowStart = $now - ITD_CHAT_RATE_WINDOW_SECONDS;
    $bucketKey = hash('sha256', $clientKey !== '' ? $clientKey : (string) ($_SERVER['HTTP_USER_AGENT'] ?? 'unknown'));
    $handle = fopen(ITD_CHAT_RATE_FILE, 'c+');
    if (!$handle) {
        return true;
    }

    flock($handle, LOCK_EX);
    $raw = stream_get_contents($handle);
    $buckets = $raw !== '' ? json_decode($raw, true) : [];
    if (!is_array($buckets)) {
        $buckets = [];
    }

    foreach ($buckets as $key => $timestamps) {
        if (!is_array($timestamps)) {
            unset($buckets[$key]);
            continue;
        }
        $buckets[$key] = array_values(array_filter($timestamps, static function ($timestamp) use ($windowStart): bool {
            return is_int($timestamp) && $timestamp >= $windowStart;
        }));
        if ($buckets[$key] === []) {
            unset($buckets[$key]);
        }
    }

    $current = $buckets[$bucketKey] ?? [];
    $allowed = count($current) < ITD_CHAT_RATE_MAX_REQUESTS;
    if ($allowed) {
        $current[] = $now;
        $buckets[$bucketKey] = $current;
    }

    ftruncate($handle, 0);
    rewind($handle);
    fwrite($handle, json_encode($buckets, JSON_UNESCAPED_SLASHES));
    fflush($handle);
    flock($handle, LOCK_UN);
    fclose($handle);

    return $allowed;
}

function itd_chat_read_knowledge(): string
{
    foreach ([__DIR__ . '/llms-full.txt', __DIR__ . '/llms.txt'] as $path) {
        if (!is_file($path) || !is_readable($path)) {
            continue;
        }
        $content = file_get_contents($path);
        if (is_string($content) && trim($content) !== '') {
            $content = trim($content);
            if (function_exists('mb_substr')) {
                return mb_substr($content, 0, 12000);
            }
            return substr($content, 0, 12000);
        }
    }

    return '';
}

function itd_chat_language_name(string $language): string
{
    $language = strtolower($language);
    if (itd_chat_starts_with($language, 'de')) {
        return 'German';
    }
    if (itd_chat_starts_with($language, 'en')) {
        return 'English';
    }
    return 'Albanian';
}

function itd_chat_build_history($history): array
{
    if (!is_array($history)) {
        return [];
    }

    $items = [];
    foreach (array_slice($history, -ITD_CHAT_MAX_HISTORY_ITEMS) as $item) {
        if (!is_array($item)) {
            continue;
        }
        $role = (string) ($item['role'] ?? '');
        if (!in_array($role, ['user', 'assistant'], true)) {
            continue;
        }
        $content = itd_chat_clean($item['content'] ?? '', 700);
        if ($content === '') {
            continue;
        }
        $items[] = ['role' => $role, 'content' => $content];
    }

    return $items;
}

function itd_chat_extract_text(array $response): string
{
    if (isset($response['output_text']) && is_string($response['output_text'])) {
        return trim($response['output_text']);
    }

    $parts = [];
    foreach (($response['output'] ?? []) as $output) {
        if (!is_array($output)) {
            continue;
        }
        foreach (($output['content'] ?? []) as $content) {
            if (!is_array($content)) {
                continue;
            }
            if (isset($content['text']) && is_string($content['text'])) {
                $parts[] = $content['text'];
            }
        }
    }

    return trim(implode("\n", $parts));
}

function itd_chat_sanitize_log_record(array $record): array
{
    foreach (['message', 'reply'] as $field) {
        if (isset($record[$field]) && is_string($record[$field])) {
            $lengthKey = $field . '_chars';
            $record[$lengthKey] = function_exists('mb_strlen')
                ? mb_strlen($record[$field])
                : strlen($record[$field]);
        }
        unset($record[$field]);
    }
    return $record;
}

function itd_chat_log(array $record): void
{
    itd_chat_storage_ready();
    $record = itd_chat_sanitize_log_record($record);
    $record['server_time'] = gmdate('c');

    $handle = fopen(ITD_CHAT_LOG_FILE, 'c+');
    if (!$handle) {
        return;
    }

    flock($handle, LOCK_EX);
    $raw = stream_get_contents($handle);
    $cutoff = time() - ITD_CHAT_LOG_RETENTION_SECONDS;
    $kept = [];
    foreach (preg_split('/\R/', $raw, -1, PREG_SPLIT_NO_EMPTY) ?: [] as $line) {
        $existing = json_decode($line, true);
        if (!is_array($existing)) {
            continue;
        }
        $timestamp = strtotime((string) ($existing['server_time'] ?? ''));
        if ($timestamp === false || $timestamp < $cutoff) {
            continue;
        }
        $kept[] = json_encode(itd_chat_sanitize_log_record($existing), JSON_UNESCAPED_SLASHES);
    }

    $kept[] = json_encode($record, JSON_UNESCAPED_SLASHES);
    $kept = array_slice($kept, -ITD_CHAT_LOG_MAX_RECORDS);

    ftruncate($handle, 0);
    rewind($handle);
    fwrite($handle, implode(PHP_EOL, $kept) . PHP_EOL);
    fflush($handle);
    flock($handle, LOCK_UN);
    fclose($handle);
}

if (defined('ITD_CHAT_LIBRARY_ONLY') && ITD_CHAT_LIBRARY_ONLY) {
    return;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    itd_chat_json(['ok' => false, 'error' => 'method_not_allowed'], 405);
}

if (!itd_chat_allowed_request()) {
    itd_chat_json(['ok' => false, 'error' => 'origin_not_allowed'], 403);
}

$raw = file_get_contents('php://input');
if ($raw === false || strlen($raw) > ITD_CHAT_MAX_PAYLOAD_BYTES) {
    itd_chat_json(['ok' => false, 'error' => 'invalid_payload'], 400);
}

$data = json_decode($raw, true);
if (!is_array($data)) {
    itd_chat_json(['ok' => false, 'error' => 'invalid_json'], 400);
}

$message = itd_chat_clean($data['message'] ?? '', ITD_CHAT_MAX_MESSAGE_CHARS);
if ($message === '') {
    itd_chat_json(['ok' => false, 'error' => 'missing_message'], 400);
}

$ip = itd_chat_client_ip();
if (!itd_chat_rate_allowed($ip)) {
    itd_chat_json([
        'ok' => false,
        'error' => 'rate_limited',
        'reply' => 'Too many messages in a short time. Please try again in a minute.',
    ], 429);
}

$apiKey = itd_chat_env_value('OPENAI_API_KEY');
if ($apiKey === '') {
    $apiKey = itd_chat_env_value('ITD_OPENAI_API_KEY');
}

if ($apiKey === '') {
    itd_chat_json([
        'ok' => false,
        'error' => 'missing_api_key',
        'reply' => 'The AI chat is almost ready, but the server key is not configured yet. Please contact us on WhatsApp at +383 49 573 570.',
    ], 503);
}

if (!function_exists('curl_init')) {
    itd_chat_json([
        'ok' => false,
        'error' => 'curl_unavailable',
        'reply' => 'The AI chat needs server cURL enabled before it can answer. Please contact us on WhatsApp at +383 49 573 570.',
    ], 503);
}

$language = itd_chat_clean($data['language'] ?? '', 20);
$targetLanguage = itd_chat_language_name($language);
$page = itd_chat_clean($data['page'] ?? '/', 220);
$sessionId = itd_chat_clean($data['session_id'] ?? '', 120);
$history = itd_chat_build_history($data['history'] ?? []);
$knowledge = itd_chat_read_knowledge();
$model = itd_chat_env_value('ITD_OPENAI_MODEL');
if ($model === '') {
    $model = ITD_CHAT_DEFAULT_MODEL;
}

$instructions = implode("\n", [
    'You are the website sales and support assistant for IT Department, a technology company in Prishtina, Kosovo.',
    'Answer in ' . $targetLanguage . ' unless the visitor clearly asks for another language.',
    'Use the website knowledge below as the source of truth. If a detail is missing, say the team can confirm it.',
    'Help with sales qualification, service explanations, AI agents, websites, software, IT support, infrastructure, cybersecurity, branding and digital marketing.',
    'For sales leads, ask one useful follow-up question or suggest WhatsApp, email or booking a call.',
    'For support requests, ask for the affected system, urgency and contact preference.',
    'Do not invent fixed prices, guarantees, timelines or availability.',
    'Keep replies concise, friendly and practical. Prefer 2 short paragraphs or fewer.',
    'Contact options: WhatsApp/phone +383 49 573 570, email info@itdks.tech, booking https://calendly.com/arion-gjonbalaj/30min.',
    '',
    'Website knowledge:',
    $knowledge,
]);

$input = [];

foreach ($history as $item) {
    $input[] = $item;
}

$input[] = [
    'role' => 'user',
    'content' => "Current page: {$page}\nVisitor message: {$message}",
];

$payload = [
    'model' => $model,
    'instructions' => $instructions,
    'input' => $input,
    'max_output_tokens' => 520,
    'store' => false,
];
if ($model === 'gpt-6-luna') {
    $payload['reasoning'] = ['effort' => 'none'];
}

$ch = curl_init('https://api.openai.com/v1/responses');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CONNECTTIMEOUT => 8,
    CURLOPT_TIMEOUT => 24,
    CURLOPT_HTTPHEADER => [
        'Authorization: Bearer ' . $apiKey,
        'Content-Type: application/json',
    ],
    CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_SLASHES),
]);

$result = curl_exec($ch);
$curlError = curl_error($ch);
$status = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);

if ($result === false || $status < 200 || $status >= 300) {
    itd_chat_log([
        'ok' => false,
        'error' => $curlError !== '' ? 'curl_error' : 'openai_error',
        'status' => $status,
        'page' => $page,
        'language' => $language,
        'session_hash' => hash('sha256', $sessionId),
        'ip_hash' => hash('sha256', $ip . '|itd-chat'),
        'message' => $message,
    ]);

    itd_chat_json([
        'ok' => false,
        'error' => 'ai_unavailable',
        'reply' => 'The AI assistant could not answer right now. Please message us on WhatsApp at +383 49 573 570 and we will help you directly.',
    ], 502);
}

$response = json_decode($result, true);
if (!is_array($response)) {
    itd_chat_json(['ok' => false, 'error' => 'invalid_ai_response'], 502);
}

$reply = itd_chat_extract_text($response);
if ($reply === '') {
    $reply = 'I can help with websites, software, AI agents and IT support. Could you share what you need and the best way for our team to contact you?';
}

$reply = itd_chat_clean($reply, 1800);

itd_chat_log([
    'ok' => true,
    'model' => $model,
    'page' => $page,
    'language' => $language,
    'session_hash' => hash('sha256', $sessionId),
    'ip_hash' => hash('sha256', $ip . '|itd-chat'),
    'message' => $message,
    'reply' => $reply,
]);

itd_chat_json([
    'ok' => true,
    'reply' => $reply,
]);
