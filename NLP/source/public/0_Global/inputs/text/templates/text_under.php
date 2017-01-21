<?php

function returnTextInput_textUnder($data){
    /*
    $id = "payment_method_card";
    $label = "Paid by Card";
    $prefix = "$";
    */
    $id = $data["id"];
    $label = $data["label"];
    $prefix = $data["prefix"];
    $width = $data["width"];   
    if(!isset($data["width"])){
        $width = "125px;";
    } 
    
    ob_start();
?>
    <div id = '<?php print $id; ?>_mainHolder' style = 'width:100%; border:0px;  padding:5px 0px; width:<?php print $width; ?>  ' class = ''>
        <div id = '<?php print $id; ?>_inputHolder'  style = 'padding:5px 0px; width:100%; ' class = ''>
            <div style = ' width:100%;' class = 'flexme '>
                <?php if(isset($prefix)): ?>
                    <div style = '' class = 'flexme'>
                        <div id = '<?php print $id; ?>_placeHolder' 
                             style = 'margin:auto; margin-left:0px;'> 
                                <?php print $prefix; ?> 
                        </div>
                    </div>
                <?php endif; ?>
                <input id = '<?php print $id; ?>_inputElement' 
                       type = 'text' 
                       class = 'flex1 <?php //print $inputElementClass; ?>' <?php //print $placeholderHTML; ?> 
                       style = ' font-size:16px; color:black; width:100%; background-color:inherit; border:0px; '>
            </div>
        </div>
        <div style = 'height:5px;'></div>
        <div id = '<?php print $id; ?>_labelHolder' class = 'flexme <?php //print $labelHolderClass; ?>'style = 'width:100%;'>
            <div class = 'labelManager_title' style ='margin:auto; margin-left:0px; font-size:14px; ' >
                <?php print $label; ?>
            </div>
        </div>
    </div>

<script>
(function(theID){
    //console.log(theID);

    ////////////////
    // Instantiate this Label
    ////////////////
    var labelHandler = new global_textLabelHandler();
    labelHandler.element = document.getElementById(theID + "_"+"labelHolder");
    labelHandler.initialize();

    ////////////////
    // Instantiate this Object
    ////////////////
    var thisHandler = new global_textHandler();
    thisHandler.DOM = { 
        inputElement : document.getElementById(theID + "_"+"inputElement"), 
        inputHolder : document.getElementById(theID + "_"+"inputHolder"),
        placeHolder : document.getElementById(theID + "_"+"placeHolder"),
    };
    thisHandler.labelManager = labelHandler;
    thisHandler.required = true;
    thisHandler.initialize();

    ////////////////
    // Add Text Handler to Label Manager 
    ////////////////
    labelHandler.textHandlers.push(thisHandler);

    ////////////////
    // Set Classes to Elements
    ////////////////
    document.getElementById(theID + "_" + "inputElement").className += " " + thisHandler.classes.inputElement.default;
    document.getElementById(theID + "_" + "inputHolder").className += " " + thisHandler.classes.inputHolder.default;
    document.getElementById(theID + "_" + "placeHolder").className += " " + thisHandler.classes.placeHolder.default;

    ////////////////
    // Globalize Elements
    ////////////////
    if(window["textHandlers"] == undefined){
        window["textHandlers"] = {};   
    }
    if(window["textHandlersOrdered"] == undefined){
        window["textHandlersOrdered"] = [];   
    }
    if(window["labelManagers"] == undefined){
        window["labelManagers"] = {};   
    }
    if(window["labelManagersOrdered"] == undefined){
        window["labelManagersOrdered"] = [];   
    }
    window["textHandlers"][theID] = thisHandler;
    window["textHandlersOrdered"].push(thisHandler);
    window["labelManagers"][theID] = labelHandler;
    window["labelManagersOrdered"].push(labelHandler);



    //console.log(window["textHandlers"]);
})("<?php print $id; ?>");
</script>

<?php 
    $html = ob_get_contents();
    ob_end_clean();
    
    return $html;
}

?>