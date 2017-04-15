<?php

$databaseName = "NLP";
require("users.secure.php");

require("class.php");
$mysqliManager = new MySQLManager();
$mysqliManager->defineUsers($users);
$mysqliManager->defineDatabaseName($databaseName);
$GLOBALS["MYSQLI_MANAGER"] = $mysqliManager;
/*
    $mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
*/