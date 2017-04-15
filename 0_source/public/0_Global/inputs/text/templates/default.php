<?php
    
    /*
    $details = array(
        "id" => "",
        "label" => "",
        "prefix" => "",
        "placeholder" => "",
    );
    returnTextInput($details);
    */


function returnTextInput($details, $boolHandler){
    $id = $details["id"];
    $label = $details["label"];
    $subLabel = $details["subLabel"];
    $prefix = $details["prefix"];
    $placeholder = $details["placeholder"];
    $required = $details["required"];
    $validationFunction = $details["validationFunction"];
    $layout = $details["layout"];
    $text_align = $details["text_align"];
    
    if(isset($text_align)){
        $text_align_string = " text-align:" . $text_align . ";";   
    }
    
    ////////////////////////////
    // Used For Rows Layout
    ////////////////////////////
        $widths = $details["widths"];
        if(isset($widths["label"])){
            $labelWidth = " width:" . $widths["label"] . "; ";   
        }
        if(isset($widths["input"])){
            $inputWidth = " width:" . $widths["input"] . "; ";   
        }
        ////////////////////////
    
    if($boolHandler !== true){
        // If not using text_handler, provide default nice style to the input - defined in default.css
        $inputElementClass = "";
        $inputHolderClass = "";
        $labelHolderClass = "";
    }
    
    if(isset($placeholder)){
        $placeholderHTML = " placeholder=  '".$placeholder."' ";   
    }
    
    ob_start();
    ?>
    
    <div id = '<?php print $id; ?>_mainHolder' style = 'width:100%; border:0px;  padding:5px 0px;  ' class = ''>
        <div id = '<?php print $id; ?>_labelHolder' class = 'flexme <?php print $labelHolderClass; ?>'style = 'width:100%;'>
            <div class = 'labelManager_title' style ='margin:auto; margin-left:0px;  font-size:14px; ' >
                <?php print $label; ?>
            </div>
            <div  style ='margin:auto; margin-right:0px;  font-size:10px; ' >
                <?php print $subLabel; ?>
            </div>
        </div>
        <div style = 'height:5px;'></div>
        <div id = '<?php print $id; ?>_inputHolder'  style = 'padding:5px 15px; ' class = '<?php print $inputHolderClass; ?>'>
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
                       class = 'flex1 <?php print $inputElementClass; ?>' <?php print $placeholderHTML; ?> 
                       style = ' font-size:14px; color:black; width:100%; background-color:inherit; border:0px; '>
            </div>
        </div>
    </div>

    <?php if($boolHandler == true): ?>
    <!-- if using text_handler js -->
        <script>
            //////////////
            // Anonymous Function in order to maintain private scope on thisHandler and theID, as well as to free() them
            //////////////
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
                thisHandler.DOM.inputElement = document.getElementById(theID + "_"+"inputElement");
                thisHandler.DOM.inputHolder = document.getElementById(theID + "_"+"inputHolder");
                thisHandler.DOM.placeHolder = document.getElementById(theID + "_"+"placeHolder");
                thisHandler.labelManager = labelHandler;
                <?php if($required == true): ?>
                    thisHandler.required = true;
                <?php endif; ?>
                <?php if(isset($validationFunction)): ?>
                    thisHandler.inputValidationFunction = <?php print $validationFunction; ?>;
                <?php endif; ?>
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
    <?php endif; ?>

    <?php
    $html = ob_get_contents();
    ob_end_clean();
    return $html;

}

