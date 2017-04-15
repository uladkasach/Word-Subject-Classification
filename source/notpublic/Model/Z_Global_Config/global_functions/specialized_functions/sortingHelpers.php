<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
///////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////
initializeSpecializedFunction("arrayHelpers");

require_once("sortingHelpers/ArrayInsertionSorter.php");
function returnArraySortedByInsertion($array, $order, $key){
    return $GLOBALS["ArrayInsertionSorter"]->returnArraySortedByInsertion($array, $order, $key);
}