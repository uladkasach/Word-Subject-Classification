<?php 
    require_once(PUBLIC_ROOT . "/0_Global/inputs/text/include.php");
    initializeViewModule('returnDivider');
    initializeViewModule('returnTileButton');

    require_once(NOTPUBLIC_ROOT."/GenerateViewData/parse/remaining.php");
    //SELECT TABLE_NAME, TABLE_ROWS FROM `information_schema`.`tables` WHERE `table_schema` = 'NLP' AND `TABLE_NAME` = 'Source_HTML'

?>
<script src = '/parse/view/handler/handler.js'></script>
<script src = '/parse/view/handler/init.js'></script>

<div style = 'width:100%;' id = '' class = ''>
    <div style = 'margin-top:15px;'></div>
    <div style = 'margin:auto; max-width:700px; min-width:300px; width:100%; ' class = ' '>
        <div class = 'cardContainer flexme' style = 'text-align:center; font-size:14px; width:100%; margin:auto; min-height:50px;'>
            <div id = '' style = 'padding:15px 30px; width:100%; margin:auto;' class = '   '>
                <div style = 'height:5px;'></div>
                
                <div class = 'flexme' style = 'width:100%;'>
                    <div class = 'flex1 flexme' style = ''>
                        <div style = 'margin:auto; margin-left:0px;'>
                            <?php
                                $data = [
                                    "id" => "parse-basic",
                                    "text" => "Basic Parse",
                                    "onclick" => "parseHandler.submitParsingOf(\"basic\");",
                                    ];
                                print returnTileButton($data);
                            ?>
                        </div>
                    </div>
                    <div style = 'width:10px;'></div>
                    <div class = 'flex1'>
                        <?php
                            $details = array(
                                "id" => "remaining_unparsed-basic",
                                "label" => "Remaining",
                                "subLabel" => "",
                                "prefix" => "",
                                "placeholder" => "",
                                "required" => true,
                            );
                            print returnTextInput($details, true);
                        ?>
                        <script>
                            window["textHandlers"]["remaining_unparsed-basic"].DOM.inputElement.disabled = 'true';
                            window["textHandlers"]["remaining_unparsed-basic"].DOM.inputElement.value = <?php print $left_count["basic"]; ?>;
                            window["textHandlers"]["remaining_unparsed-basic"].determineStatusOnBlur();
                        </script>
                    </div>
                    <div style = 'width:10px;'></div>
                    <div class = 'flex1'>
                        <?php
                            $details = array(
                                "id" => "desired_parsed",
                                "label" => "Desired Amt to be Parsed",
                                "subLabel" => "",
                                "prefix" => "",
                                "placeholder" => "",
                                "required" => true,
                            );
                            print returnTextInput($details, true);
                        ?>
                        <script>
                            window["textHandlers"]["desired_parsed"].enforce.digits_only = true;
                        </script>
                    </div>
                </div>
                <div style = 'height:25px;'></div>
                <div style = 'height:25px;'></div>
                <div style = 'height:5px;'></div>
            </div>
        </div>
     </div>
</div>
