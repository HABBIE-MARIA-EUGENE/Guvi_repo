$redis = new RedisClient([
    'scheme' => 'tcp',
    'host'   => 'redis-redis-cloud.com',
    'port'   => 17845,
    'password' => ''
]);


$client = new Client("mongodb+srv://xxxxxxxxxxxxxxx@cluster0.b1rtq6b.mongodb.net/?retryWrites=true&w=majority");

$collection = $client->myapp->profiles;
