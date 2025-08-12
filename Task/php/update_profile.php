<?php
require __DIR__ . '/../../vendor/autoload.php';
use MongoDB\Client;

header('Content-Type: application/json');

$email = $_POST['email'] ?? '';
$age = $_POST['age'] ?? '';
$dob = $_POST['dob'] ?? '';
$contact = $_POST['contact'] ?? '';

if (empty($email)) {
    echo json_encode(['status' => 'error', 'message' => 'Missing email']);
    exit;
}

try {
    $client = new Client("mongodb+srv://meugenem1409:fSEUdgzWUC7b3XwA@cluster0.b1rtq6b.mongodb.net/?retryWrites=true&w=majority");
    $collection = $client->myapp->profiles;

    // Upsert = update if exists, else insert
    $collection->updateOne(
        ['email' => $email],
        ['$set' => [
            'age' => $age,
            'dob' => $dob,
            'contact' => $contact
        ]],
        ['upsert' => true]
    );

    echo json_encode(['status' => 'success', 'message' => 'Profile updated successfully']);

} catch (Exception $e) {
    echo json_encode(['status' => 'error', 'message' => 'MongoDB error: ' . $e->getMessage()]);
}
?>
