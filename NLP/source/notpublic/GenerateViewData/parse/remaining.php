<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////////////////////////////////// 
initializeModelModule("mysqli_interface");
/////////////////////////////////////////////
$left_count = [];


//////////////////
// Get total count for the source_html
//////////////////
$table_names = 'Source_HTML';
$mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
$stmt = $mysqli->prepare("SELECT SourceID FROM `Source_HTML`");
print   $mysqli->error;
$stmt->bind_param("s", $table_names);
$stmt->execute();
$stmt->store_result();
$numRows = $stmt->num_rows;
//print "rows : " . $num_of_rows;
$stmt->bind_result($name, $rows);  
while($stmt->fetch()){ }
$stmt->free_result();
$stmt->close();
$total_source_count = $numRows;
//var_dump($total_source_count);


/////////////////
// Determine amount left for basic parsing
/////////////////
$parseType = 'basic';
$mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
$stmt = $mysqli->prepare("SELECT URL FROM Parsed_Data WHERE ParseType = ?");
print   $mysqli->error;
$stmt->bind_param("s", $parseType);
$stmt->execute();
$stmt->store_result();
$numRows = $stmt->num_rows;
//print "rows : " . $num_of_rows;
$stmt->bind_result($url);  
while($stmt->fetch()){};
$stmt->free_result();
$stmt->close();
$total_basic_parse_count = $numRows;
$left_basic_parse = $total_source_count - $total_basic_parse_count;
$left_count["basic"] = $left_basic_parse;

//var_dump($left_count);



