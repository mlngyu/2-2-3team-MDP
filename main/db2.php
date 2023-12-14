<?php
$servername = "localhost";
$username = "imminho";
$password = "mu3102!!";
$dbname = "imminho";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection

$sql = "SELECT * FROM `imminho`.`giseubsungbae`";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Fetch the results and store them in an array
    $data = array();
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
    // Output the array
    echo json_encode($data);
} else {
    echo json_encode("nooo");
}

$conn->close();


?>