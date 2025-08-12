<?php
$servername = "localhost";      // where MySQL runs
$username = "root";             // default for XAMPP
$password = "";                 // empty password for root in XAMPP
$dbname = "guvi_users";         //DB name


$conn = new mysqli($servername, $username, $password, $dbname);


if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
