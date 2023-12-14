<?php
// Establish database connection
$servername = "localhost";
$username = "imminho";
$password = "mu3102!!";
$dbname = "imminho";

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get data from AJAX request
$name = $_POST['name'];
$email = $_POST['email'];

// Insert data into the database
$sql_first = "SELECT * FROM `giseubsungbae` WHERE NUMBER = '$name'";
$sql_second = "DELETE FROM `giseubsungbae` WHERE NUMBER = '$name'";

$result = $conn->query($sql_first);

if ($result) {
    if ($result->num_rows > 0) {
        // Delete existing record
        if ($conn->query($sql_second) === TRUE) {
            echo "Data deleted successfully";
        } else {
            echo "Error deleting record: " . $conn->error;
        }
    } else {
        echo "Record not found";
    }
} else {
    echo "Error selecting record: " . $conn->error;
}

$conn->close();
?>