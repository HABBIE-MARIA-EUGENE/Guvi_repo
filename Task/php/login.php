<?php
header('Content-Type: application/json');
require_once 'db_config.php';
require __DIR__ . '/../../vendor/autoload.php';




use Predis\Client as RedisClient;

$email = $_POST['email'] ?? '';
$password = $_POST['password'] ?? '';

if (empty($email) || empty($password)) {
    echo json_encode(['status' => 'error', 'message' => 'Missing credentials']);
    exit;
}

$stmt = $conn->prepare("SELECT password FROM users WHERE email = ?");
$stmt->bind_param("s", $email);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows === 1) {
    $stmt->bind_result($hashed_pw);
    $stmt->fetch();

    if (password_verify($password, $hashed_pw)) {
        try {
            $redis = new RedisClient([
                'scheme' => 'tcp',
                'host'   => 'redis-17845.c261.us-east-1-4.ec2.redns.redis-cloud.com',
                'port'   => 17845,
                'password' => 'sQSp8ptFjvGwolUqwtKQxu9AXPrpjEoU'
            ]);

            // test connection
            $redis->ping();

            $redis->set($email, true);
            $redis->expire($email, 3600); // 1 hour

            echo json_encode([
                'status' => 'success',
                'email' => $email,
                'message' => 'login successful'
            ]);
        } catch (Exception $e) {
            echo json_encode(['status' => 'error', 'message' => 'Redis error: ' . $e->getMessage()]);
        }
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Incorrect password']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Email not found']);
}

$stmt->close();
$conn->close();
