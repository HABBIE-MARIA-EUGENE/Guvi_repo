<?php
// php/login.php
header('Content-Type: application/json');

// Only POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status'=>'error','message'=>'Method not allowed']);
    exit;
}

// DB: creates $pdo (MySQL, for auth table with email+password_hash)
require __DIR__ . '/db.php';

// Redis for session storage
require __DIR__ . '/config_redis.php';

$email = trim($_POST['email'] ?? '');
$pwd   = $_POST['password'] ?? '';

// Basic validation
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['status'=>'error','message'=>'Invalid email']);
    exit;
}
if ($pwd === '') {
    echo json_encode(['status'=>'error','message'=>'Password required']);
    exit;
}

try {
    // 1) Fetch user by email
    $stmt = $pdo->prepare('SELECT id, password FROM users WHERE email = ?');
    $stmt->execute([$email]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$user || !password_verify($pwd, $user['password'])) {
        // Do NOT leak whether email exists
        echo json_encode(['status'=>'error','message'=>'Invalid credentials']);
        exit;
    }

    // 2) Create a random session token
    $sessionId = 'sess_' . bin2hex(random_bytes(16));

    // 3) Save session -> userId in Redis with TTL (e.g., 1 hour)
    $redis = getRedis();
    // store user id as string
    $redis->setex($sessionId, 3600, (string)$user['id']);

    // 4) Return JSON with session for your login.js
    echo json_encode([
        'status'  => 'ok',
        'session' => $sessionId,
        'userId'  => (int)$user['id']
    ]);
    exit;

} catch (Throwable $e) {
    // Log $e->getMessage() to server logs if needed
    http_response_code(500);
    echo json_encode(['status'=>'error','message'=>'Server error during login']);
    exit;
}
