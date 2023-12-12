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
$sql_second = "UPDATE `giseubsungbae` SET number = '$name', why = '$email' WHERE NUMBER = '$name'";
$sql = "INSERT INTO `giseubsungbae` (number, why) VALUES ('$name', '$email')";

$result = $conn->query($sql_first);

if ($result) {
    if ($result->num_rows > 0) {
        // Update existing record
        if ($conn->query($sql_second) === TRUE) {
            echo "Data updated successfully";
        } else {
            echo "Error updating record: " . $conn->error;
        }
    } else {
        // Insert new record
        if ($conn->query($sql) === TRUE) {
            echo "Data inserted successfully";
        } else {
            echo "Error inserting record: " . $conn->error;
        }
    }
} else {
    echo "Error selecting record: " . $conn->error;
}

$conn->close();
?>