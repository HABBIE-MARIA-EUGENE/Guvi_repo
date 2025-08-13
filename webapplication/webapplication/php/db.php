<?php

$DB_HOST = '127.0.0.1';   // use 127.0.0.1 to avoid socket issues
$DB_PORT = '3306';        
$DB_NAME = 'guvi_v3';    
$DB_USER = 'root';
$DB_PASS = '';

// pdo conn.
try {

    // Build DSN correctly (interpolate variables,note:  no spaces around '=')

    $dsn = "mysql:host=$DB_HOST;port=$DB_PORT;dbname=$DB_NAME;charset=utf8mb4";

    $pdo = new PDO(
        $dsn,
        $DB_USER,
        $DB_PASS,
        [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,  // to throw exceptions
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false                    //  prep. statements
        ]
    );

    //Note :  no echo/output on success; just having $pdo available is enough

} catch (PDOException $e) {

    // Return JSON 

    http_response_code(500);
    header('Content-Type: application/json');

    //Note: 
    echo json_encode([
        'status'  => 'error',
        'message' => 'DB connection failed'
        // 'debug' => $e->getMessage() 
    ]);
    exit;
}
