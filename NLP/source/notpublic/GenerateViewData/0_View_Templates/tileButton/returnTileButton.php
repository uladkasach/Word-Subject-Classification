<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
///////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////
/////////////////////////////////////////////

function returnTileButton($button, $fontSize){

    if(isset($button["fontSize"])){
        $fontSize = $button["fontSize"];
    }
    
    if($button["textOverwrite"] !== true){
        $button["text"] = strtoupper($button["text"]);   
    }
    
    if($button["fillWidth"] == true){
        $fillWidth = "width:100%;";   
    }
    
    if(!isset($fontSize)){
        $fontSize = "12px";   
    }
    if(isset($button["a"])){
        $button["href"] = $button["a"];   
    }
    if($button["href"] == null){
        $button["href"] = "javascript: void(0);";
    }
    
    if($button["spec"] == "red"){
        $specModifier = "_red";   
    } else if ($button["spec"] == "gray"){
        $specModifier = "_gray";   
    }
    
    //$button["align"]
    
    
    
    if(isset($button["defaultImg"]) && isset($button["hoverImg"])){ 
        $padding = "<div style = 'width:10px;'></div>";
        if($button["fullGap"] == true){
            $padding = "<div class = 'flex1'></div>";   
        }

        /////////////////////////////////////
        // Generate default image
        /////////////////////////////////////
        ob_start();
            require("html_image_template.php");
        $buttonHTML["default"] = ob_get_contents();
        ob_end_clean();
        
        ////////////////////////////////////
        // Generate disabled image
        ////////////////////////////////////
        ob_start();
            require("html_image_disabled_template.php");
        $buttonHTML["disabled"] = ob_get_contents();
        ob_end_clean();
        
        if($button["align"] == "right"){
            $imageRight["default"] = $padding . $buttonHTML["default"];    
            $imageRight["disabled"] = $padding . $buttonHTML["disabled"];    
        } else {
            $imageLeft["default"] = $buttonHTML["default"] . $padding;
            $imageLeft["disabled"] = $buttonHTML["disabled"] . $padding;
        }
    }
    
    
    
    ob_start();
    require "html_template.php";
    $html = ob_get_contents();
    ob_end_clean();
    
    return $html;
}