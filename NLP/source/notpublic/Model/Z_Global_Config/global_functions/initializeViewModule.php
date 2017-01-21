<?php

//////////////////
// Purpose : explicitly define where modules are located as well as template the actuall calling of the modules
//////////////////

function initializeViewModule($type){
    //print $type;
    $defined = [
            //module name => path to module,
            "returnDivider" => NOTPUBLIC_ROOT . "/GenerateViewData/0_View_Templates/divider/returnDivider.php",
            "returnTileButton" => NOTPUBLIC_ROOT . "/GenerateViewData/0_View_Templates/tileButton/returnTileButton.php",
        ];
    
    $requestedModule = $defined[$type];
    
    //var_dump( $requestedModule );
    
    if(!isset($requestedModule)){
        print "that type of module has not been defined. Error.";
        die();
    }
    
    require_once($requestedModule);
}
