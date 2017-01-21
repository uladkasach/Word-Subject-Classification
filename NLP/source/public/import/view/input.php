<?php 
    require_once(PUBLIC_ROOT . "/0_Global/inputs/text/include.php");
    initializeViewModule('returnDivider');
    initializeViewModule('returnTileButton');
?>
<script src = '/import/view/handler/handler.js'></script>
<script src = '/import/view/handler/init.js'></script>

<div style = 'width:100%;' id = '' class = ''>
    <div style = 'margin-top:15px;'></div>
    <div style = 'margin:auto; max-width:700px; min-width:300px; width:100%; ' class = ' '>
        <div class = 'cardContainer flexme' style = 'text-align:center; font-size:14px; width:100%; margin:auto; min-height:50px;'>
            <div id = '' style = 'padding:15px 30px; width:100%; margin:auto;' class = '   '>
                <div style = 'height:5px;'></div>
                <div class = '' style = 'width:100%;'>

                        <?php
                            $details = array(
                                "id" => "source_url",
                                "label" => "Source URL",
                                "subLabel" => "",
                                "prefix" => "",
                                "placeholder" => "",
                                "required" => true,
                            );
                            print returnTextInput($details, true);
                        ?>
                </div>
                <div style = 'height:25px;'></div>
                <div class = 'flexme' style = ''>
                    <?php
                        $data = [
                            "id" => "submit_source",
                            "text" => "Submit Source",
                            "onclick" => "sourceSubmissionHandler.submit();",
                            ];
                        print returnTileButton($data);
                    ?>
                </div>
                <script>
                    //window["buttonHandler"]["completeRegistration"].displayLoading();
                </script>
                <div style = 'height:5px;'></div>
                <a href = '/import/check.php' target = '_blank'> Check last import html </a>
            </div>
        </div>
     </div>
</div>
