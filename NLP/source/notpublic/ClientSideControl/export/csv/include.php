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
$requested_quantity = urldecode($_POST["quantity"]);
//////////////


//////////////////
// Verify URL not already scanned
//////////////////
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
$stmt = $mysqli->prepare("INSERT INTO Source_HTML (`URL`, `DateTimeRecorded`, `HTML`) VALUES (?, ?, ?)");
//print "INSERT INTO Users (`DateTimeAdded`, `Email`) VALUES ('$when', '$email')";
echo $mysqli->error;
$stmt->bind_param("sss", $source_url, $when, $html);
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
