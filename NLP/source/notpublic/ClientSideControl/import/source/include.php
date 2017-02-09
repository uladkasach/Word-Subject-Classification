<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////////////////////////////////// 
initializeModelModule("mysqli_interface");
/////////////////////////////////////////////


/////////////////////////////////////////
// Retreive Input
/////////////////////////////////////////
//////////////
if(!isset($rescan_override)){ // see public/load_html/
    $source_url = urldecode($_POST["source_url"]);
} else {
    $source_url = $rescan_override["url"];   
}
//var_dump($source_url);
//////////////


//////////////////
// Verify URL not already scanned
//////////////////
if(!isset($rescan_override)){ // see public/load_html/
    $already_found = false;
    $mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
    $stmt = $mysqli->prepare("SELECT SourceID FROM Source_HTML WHERE URL = ?");
    //print "SELECT Title, FilePath, DateTimeAdded, Views, Downloads FROM Schedules WHERE LocationID = '".$locationID."' AND Alive = '1'";
    print   $mysqli->error ;
    $stmt->bind_param("s", $source_url);
    $stmt->execute();
    $stmt->store_result();
    $numRows = $stmt->num_rows;
    //print "rows : " . $num_of_rows;
    $stmt->bind_result($id);  
    while($stmt->fetch()){ 
        $already_found = true;
    }
    $stmt->free_result();
    $stmt->close();
    if($already_found){
        print "[[==]]ALREADY[[==]]";
        die();
    }
}


//////////////////
// Get HTML
/////////////////
require_once("retreive_html.php");
$html = retreive_html($source_url);
if($html == false){
    print "[[==]]ERR[[==]]";
    die();
}
//var_dump($html);


//////////////////
// Save HTML
/////////////////
$mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
$when = date('Y-m-d H:i:s');
if(!isset($rescan_override)){ // see public/load_html/
    $stmt = $mysqli->prepare("INSERT INTO Source_HTML (`URL`, `DateTimeRecorded`, `HTML`) VALUES (?, ?, ?)");
    echo $mysqli->error;
    $stmt->bind_param("sss", $source_url, $when, $html);
} else {
    $stmt = $mysqli->prepare("UPDATE `Source_HTML` SET `HTML`= ? WHERE SourceID = ?");
    echo $mysqli->error;
    $stmt->bind_param("ss", $html, $rescan_override["id"]);
}
//print "INSERT INTO Users (`DateTimeAdded`, `Email`) VALUES ('$when', '$email')";
$exec = $stmt->execute();
$stmt->close();
////////////////////////
var_dump($exec);
//print "here i am!";
if(!$exec){
    print "[[==]]ERR[[==]]";
    die();
}


print "[[==]]SCS[[==]]";
