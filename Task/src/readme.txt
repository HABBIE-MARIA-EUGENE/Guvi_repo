$redis = new RedisClient([
    'scheme' => 'tcp',
    'host'   => 'redis-17845.c261.us-east-1-4.ec2.redns.redis-cloud.com',
    'port'   => 17845,
    'password' => 'sQSp8ptFjvGwolUqwtKQxu9AXPrpjEoU'
]);


$client = new Client("mongodb+srv://meugenem1409:fSEUdgzWUC7b3XwA@cluster0.b1rtq6b.mongodb.net/?retryWrites=true&w=majority");
$collection = $client->myapp->profiles;