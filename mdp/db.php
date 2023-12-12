<?php
$servername = "localhost";
$username = "imminho";
$password = "mu3102!!";
$dbname = "imminho";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection

$sql = "SELECT * FROM `imminho`.`test` LIMIT 1;";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    // Output data of the latest test value
    $row = $result->fetch_assoc();
    $output = $row["test"];
    echo $output;
} else {
    echo "No test values found";
}
$conn->close();


?>