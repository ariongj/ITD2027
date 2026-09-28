<?php
declare(strict_types=1);

define('ITD_CHAT_LIBRARY_ONLY', true);
require dirname(__DIR__) . '/chat.php';

function expect_same($expected, $actual, string $label): void
{
    if ($expected !== $actual) {
        fwrite(STDERR, "{$label}: expected " . var_export($expected, true) . ', got ' . var_export($actual, true) . PHP_EOL);
        exit(1);
    }
}

putenv('ITD_TRUSTED_PROXY_CIDRS');
$_SERVER['REMOTE_ADDR'] = '198.51.100.24';
$_SERVER['HTTP_X_FORWARDED_FOR'] = '203.0.113.9';
$_SERVER['HTTP_CF_CONNECTING_IP'] = '203.0.113.10';
expect_same('198.51.100.24', itd_chat_client_ip(), 'Untrusted forwarding headers are ignored');

putenv('ITD_TRUSTED_PROXY_CIDRS=198.51.100.0/24');
expect_same('203.0.113.10', itd_chat_client_ip(), 'Trusted proxy may provide the client address');

$_SERVER['HTTP_CF_CONNECTING_IP'] = 'not-an-ip';
expect_same('203.0.113.9', itd_chat_client_ip(), 'Invalid preferred proxy address falls back safely');

expect_same(true, itd_chat_ip_in_cidr('198.51.100.24', '198.51.100.0/24'), 'IPv4 CIDR match');
expect_same(false, itd_chat_ip_in_cidr('198.51.101.24', '198.51.100.0/24'), 'IPv4 CIDR mismatch');
expect_same(true, itd_chat_ip_in_cidr('2001:db8::20', '2001:db8::/32'), 'IPv6 CIDR match');

$sanitized = itd_chat_sanitize_log_record([
    'message' => 'secret',
    'reply' => 'private reply',
    'ok' => true,
]);
expect_same(false, array_key_exists('message', $sanitized), 'Visitor message text is removed');
expect_same(false, array_key_exists('reply', $sanitized), 'Assistant reply text is removed');
expect_same(6, $sanitized['message_chars'] ?? null, 'Visitor message length is retained');
expect_same(13, $sanitized['reply_chars'] ?? null, 'Assistant reply length is retained');

putenv('ITD_TRUSTED_PROXY_CIDRS');
fwrite(STDOUT, "chat-security: PASS" . PHP_EOL);
