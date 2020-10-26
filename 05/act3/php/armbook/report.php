<?php

include_once("common.php");

if ($_SERVER['REQUEST_METHOD'] !== "POST") {
    die("You need to make a POST request, bucaroo");
}

$info = file_get_contents("php://input");

if ($stmt = $mysqli->prepare("INSERT INTO reports (info) VALUES (?)")) {
    // string type
    if ($stmt->bind_param("s", $info)) {
        if ($stmt->execute()) {
            die("Added report to database");
        }
    }
}

die("Error, did not add to database");
?>
