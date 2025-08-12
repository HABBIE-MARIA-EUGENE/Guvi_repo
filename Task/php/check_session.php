<?php
require __DIR__ . '/../../vendor/autoload.php';

use Predis\Client as RedisClient;
use MongoDB\Client as MongoClient;

header('Content-Type: application/json');


$redis = new RedisClient([
    'scheme' => 'tcp',
    'host'   => 'redis-17845.c261.us-east-1-4.ec2.redns.redis-cloud.com',
    'port'   => 17845,
    'password' => 'sQSp8ptFjvGwolUqwtKQxu9AXPrpjEoU'
]);


$email = $_POST['email'] ?? '';

if (empty($email)) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Missing email']);
    exit;
}


if (!$redis->exists($email)) {
    http_response_code(401);
    echo json_encode(['status' => 'error', 'message' => 'Session verification failed']);
    exit;
}


try {
    $uri = "mongodb+srv://meugenem1409:fSEUdgzWUC7b3XwA@cluster0.b1rtq6b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
    $client = new MongoClient($uri);
    $collection = $client->myapp->profiles;

    // Case-insensitive email match
    $profile = $collection->findOne([
        'email' => ['$regex' => '^' . preg_quote($email) . '$', '$options' => 'i']
    ]);

    // return success, even if profile not found
    echo json_encode([
        'status' => 'success',
        'email' => $email,
        'profile' => [
            'age' => $profile['age'] ?? '',
            'dob' => $profile['dob'] ?? '',
            'contact' => $profile['contact'] ?? ''
        ]
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['status' => 'error', 'message' => 'MongoDB error: ' . $e->getMessage()]);
}
?>
