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
$quantity = $word_quantity = urldecode($_GET["quantity"]);
$type = urldecode($_GET["type"]);
//////////////

#print('starting!');
ini_set('memory_limit', '2048M'); #2GiB
ini_set('max_execution_time', 300); #5 min
//////////////////////////////////////////
// Interpret Input
//////////////////////////////////////////
if($type == "" || !isset($type)){
    $type = "basic";
} else if($type !== "basic" && $type !== "stop"){
    print "Error.";
    die();
}
//$quantity = preg_replace("/[^0-9.]/", '', strtolower($quantity));
$intval = floatval($quantity);
$modifier = preg_replace("/[^A-Za-z]/", '', strtolower($quantity)); // remove all nonalpha characters 
if($modifier == "k" || $modifier == "kilo"){
    $quantity = $intval * 1000;   
} else if ($modifier == "m" || $modifier == "mega" || $modifier == "million"){
    $quantity = $intval * 1000000;
} else if ($modifier == "g" || $modifier == "giga" || $modifier == "billion"){
    $quantity = $intval * 1000000000;
} else {
    $quantity = $intval;   
}


//////////////////////////////////
// Load document body
//////////////////////////////////
require_once("gen_body.php");
$data = gen_body($type, $quantity);
$document_body = $data[1];
if(!$data[0]){
    $word_quantity = "(-)" . $word_quantity; 
}
if($quantity == 0){
    print("Word count = " . $data[2]);
    die();
}

#print('here i am!');


/////////////////////////////////
// Begin document output
/////////////////////////////////
header("Content-type: text/plain");
header("Content-Disposition: attachment; filename=plants_".$word_quantity."_".$type."_export.csv");

print $document_body;

?>