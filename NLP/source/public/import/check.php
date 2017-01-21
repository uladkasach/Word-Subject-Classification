<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////////////////////////////////// 
initializeModelModule("mysqli_interface");
/////////////////////////////////////////////

    $mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
    $stmt = $mysqli->prepare("SELECT HTML FROM Source_HTML ORDER BY SourceID DESC LIMIT 1");
    print   $mysqli->error;
    //$stmt->bind_param("si", $type, $amount);
    $stmt->execute();
    $stmt->store_result();
    $numRows = $stmt->num_rows;
    $stmt->bind_result($html);  
    while($stmt->fetch()){
        print $html;
        die();
    }
    $stmt->free_result();
    $stmt->close();