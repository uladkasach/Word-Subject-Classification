<?php

//////////////////
// Purpose : explicitly define where modules are located as well as template the actuall calling of the modules
//////////////////


function initializeModelModule($type){
    //print $type;
    $defined = [
            //module name => path to module,
            "session_interface" => NOTPUBLIC_ROOT . "/Model/0_DataStructure_Interfaces/session_interface/init.php",
            "mysqli_interface" => NOTPUBLIC_ROOT . "/Model/0_DataStructure_Interfaces/mysql_interface/init.php",
        
        ];
    
    $requestedModule = $defined[$type];
    
    //var_dump( $requestedModule );
    
    if(!isset($requestedModule)){
        print "that type of module has not been defined. Error.";
        die();
    }
    
    require_once($requestedModule);
}