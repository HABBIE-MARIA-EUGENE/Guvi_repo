<?php
const REDIS_HOST = 'redis-xxxxxxxxxx-cloud.com';
const REDIS_PORT = 16181;
const REDIS_USER = 'default';
const REDIS_PASS = 'xxxxxxxxxxxxx';
const REDIS_USE_TLS = true; // rediss:// requires TLS

function connectRedis(): Redis {
    $r = new Redis();

    //  explicit SSL .
    $ctx = [
        'ssl' => [
            'SNI_enabled' => true,
            'peer_name'   => REDIS_HOST,

        ]
    ];
    $r->connect(REDIS_HOST, REDIS_PORT, 3.0, null, 0, 0, REDIS_USE_TLS ? $ctx : null);
    return $r;
}

function getRedis(): Redis {
    $r = connectRedis();

    // Trying with phpredis 5.3+ two - argument AUTH first
    try {
        $ok = $r->auth(REDIS_USER, REDIS_PASS);
        if ($ok) return $r;
    } catch (Throwable $e) {

        // continue to array/legacy form
    }

    // Try ACL array form

    try {
        $ok = $r->auth(['username' => REDIS_USER, 'password' => REDIS_PASS]);
        if ($ok) return $r;
    } catch (Throwable $e) {

        // continue to legacy single password

    }

    // Try legacy password-only (some providers still accept)
    
    $ok = $r->auth(REDIS_PASS);
    if ($ok) return $r;

    throw new RuntimeException('AUTH failed: server did not accept provided credentials.');
}
