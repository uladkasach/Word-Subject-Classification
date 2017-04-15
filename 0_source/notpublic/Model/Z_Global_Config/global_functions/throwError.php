<?php
 
function throwError($type, $displayPageBool){
    
    $errors = [
        "404" => [
            "PATH" => "/0_Global/40_/404/index.php",
            "HEADER" => "HTTP/1.0 404 Not Found",
          ],
        "403"  => [
            "PATH" => "/0_Global/40_/403/index.php",
            "HEADER" => "HTTP/1.0 403 Forbidden",
          ],
        ];
    
    //var_dump($type);
    $keys = array_keys($errors);
    $results = in_array($type, $keys);
    
    if(count($results) == 0){
        print "That error type is not defined";
        die();
    }
    
    ob_start();
    var_dump($displayPageBool);
    $displayPageBoolDump = ob_get_contents();
    ob_end_clean();
    
    
    ///////////////////////
    // Log the Error
    ///////////////////////
    $string = "Error has been thrown. Display page? " . $displayPageBoolDump;
    sendALog($string, "Error Thrown");
    
    
    ///////////////////////
    // Display Error Page, if error was thrown on a display page
    ///////////////////////
    if($displayPageBool && $errors[$type]["PATH"] !== null){
        require_once($_SERVER["DOCUMENT_ROOT"] . $errors[$type]["PATH"] );
    }
    
    ///////////////////////
    // Send Forbidden header and terminate
    ///////////////////////
    
    header($errors[$type]["HEADER"]);
    die();
}