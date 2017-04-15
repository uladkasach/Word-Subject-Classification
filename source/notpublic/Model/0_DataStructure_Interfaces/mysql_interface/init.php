<?php

$databaseName = "NLP";
$users = [
        "NLP_main" => "ProcessTheNLP",
    ];

require("class.php");
$mysqliManager = new MySQLManager();
$mysqliManager->defineUsers($users);
$mysqliManager->defineDatabaseName($databaseName);
$GLOBALS["MYSQLI_MANAGER"] = $mysqliManager;
/*
    $mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
*/