<?php 
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
//////////////
initializeScriptType("VIEW");
///////////////////////////////////////////// 
?>

<html>
    <head>
        <!-- load header and always required globals -->
        <title>403 - Access Denied</title>
        <?php require_once( PUBLIC_ROOT . "/0_Global/header/header.php"); ?>
        
    </head>
    
    <div style = 'position:absolute; top:0; left:0; right:0; bottom:0;' class = 'flexme'>

        <div style = 'margin:auto;'>
<?php

    $data = [
        "imageSRC" => "/img/maybelater2.gif",
        "heading" => [
            "text" => "Maybe Later",
            "overlap" => false,
            ],
        "description" => "Sorry, you dont have permission to access this page. Try again later after you sign in or gain permission.",
        "buttons" => [
                [
                    "text" => "Back",
                    "onclick" => "",
                    "a" => "javascript:history.back()",
                    "align" => "right",
                ],
                [
                    "text" => "Home Page",
                    "onclick" => "",
                    "a" => "/",
                    "align" => "right",
                ],
            ],
    ];

    print returnImageTile($data);

?>
        </div>


    </div>
    
</html>