<?php
$servername = "localhost";
$username = "imminho";
$password = "mu3102!!";
$dbname = "imminho";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

$afmax = $_POST['afmax'];

// Check connection
$sql_first = "DELETE FROM `imminho`.`test2`";
$sql = "INSERT INTO `imminho`.`test2` (afmax) VALUES ('$afmax')";
$result = $conn->query($sql_first);
$result = $conn->query($sql);
$conn->close();


?>