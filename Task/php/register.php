<?php

if ($_SERVER["REQUEST_METHOD"] == "POST" ) {
    require_once "db_config.php";
    require __DIR__ . '/../../vendor/autoload.php';


    $email = $_POST['email'];
    $password = $_POST['password'];


    $hashed_pw = password_hash($password, PASSWORD_DEFAULT);


    $stmt = $conn->prepare("INSERT INTO users (email, password) VALUES(?,?)");
    $stmt->bind_param("ss", $email, $hashed_pw);

    
    
    if ($stmt->execute()) {
        echo "Registered successfully";

    } else {
        echo "Error: " . $stmt->error;
    }
    
    
    $stmt->close();
    $conn->close();


}
?>