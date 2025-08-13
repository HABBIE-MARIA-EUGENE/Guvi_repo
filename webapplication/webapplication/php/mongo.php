<?php

// REQUIREMENTS:
//  composer require mongodb/mongodb
//  Enable PHP extension: extension=php_mongodb.dll (Windows/XAMPP) or .so for Linux
require_once dirname(__DIR__, 2) . '/vendor/autoload.php';

use MongoDB\Client;

function getMongo(): Client {
  // Atlas URI and credentials

  $uri = 'mongodb+srv://<us>:<pw>@cluster0.b1rtq6b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0';
  return new Client($uri, ['ssl' => true]);

}
