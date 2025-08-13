<?php
// php/mongo.php
// requires composer package "mongodb/mongodb": "^2.1"
require_once __DIR__ . '/../vendor/autoload.php'; // Composer autoload

use MongoDB\Client;

function getMongo(): Client {
    // Replace with your MongoDB Atlas URI and DB user/pass
    $uri = 'mongodb+srv://<USER>:<PASS>@<cluster>.mongodb.net/?retryWrites=true&w=majority';
    return new Client($uri, [
        'ssl' => true,
    ]);
}
