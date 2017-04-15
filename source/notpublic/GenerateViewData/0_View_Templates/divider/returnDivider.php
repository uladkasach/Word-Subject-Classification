<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
///////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////
/////////////////////////////////////////////

function returnDivider($data){

    $heading = $data;
    
    ob_start();
    require "html_template.php";
    $html = ob_get_contents();
    ob_end_clean();
    
    return $html;
}