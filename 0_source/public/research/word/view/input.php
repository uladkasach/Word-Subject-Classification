<?php 
    require_once(PUBLIC_ROOT . "/0_Global/inputs/text/include.php");
    initializeViewModule('returnDivider');
    initializeViewModule('returnTileButton');
?>
<script src = '/research/word/view/handler/handler.js'></script>
<script src = '/research/word/view/handler/init.js'></script>

<div style = 'width:100%;' id = 'research_word_selection' class = ''>
    <div style = 'margin-top:15px;'></div>
    <div style = 'margin:auto; max-width:700px; min-width:300px; width:100%; ' class = ' '>
        <div class = 'cardContainer flexme' style = 'text-align:center; font-size:14px; width:100%; margin:auto; min-height:50px;'>
            <div id = '' style = 'padding:15px 30px; width:100%; margin:auto;' class = '   '>
                <div style = 'height:5px;'></div>
                <div class = '' style = 'width:100%;'>

                        <?php
                            $details = array(
                                "id" => "research_word",
                                "label" => "Word To Research",
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
                            "id" => "submit_request",
                            "text" => "Research the Word",
                            "onclick" => "researchHandler.submitRequest();",
                            ];
                        print returnTileButton($data);
                    ?>
                </div>
            </div>
        </div>
     </div>
</div>


<div style = 'width:100%;' id = 'research_link_display' class = 'disnon'>
    <div style = 'margin-top:15px;'></div>
    <div style = 'margin:auto; max-width:700px; min-width:300px; width:100%; ' class = ' '>
        <div class = 'cardContainer flexme' style = 'text-align:center; font-size:14px; width:100%; margin:auto; min-height:50px;'>
            <div id = '' style = 'padding:15px 30px; width:100%; margin:auto;' class = '   '>
                <div style = 'width:100%; height:130px;'>
                    <div style = 'height:5px;'></div>
                    <div class = '' style = 'width:100%;'>
                        <span id = 'research_link_display_title' style = 'margin-left:0px; font-size:16; font-weight:bold;'> Plant - Wikipedia </span>
                    </div>
                    <div style = 'height:5px;'></div>
                    <div class = '' style = 'width:100%;'>
                       <i> <a href = '' id = 'research_link_display_link' target = '_blank' style = 'margin-left:0px; font-size:14px; color:#0084ed;'> https://en.wikipedia.org/wiki/Plant </a></i>
                    </div>
                    <div style = 'height:5px;'></div>
                    <div class = '' style = 'width:100%;'>
                        <span id = 'research_link_display_snippet' style = 'margin-left:0px; font-size:14px;'> Plants are mainly multicellular, predominantly photosynthetic eukaryotes of the \nkingdom Plantae. The term is today generally limited to the green plants, which ... </span>
                    </div>
                    <div style = 'height:25px;'></div>
                </div>
                <div class = 'flexme' style = ''>
                    <?php
                        $data = [
                            "id" => "research_link_display_skip",
                            "text" => "Skip",
                            "onclick" => "researchHandler.importTheLink(false);",
                            ];
                        print returnTileButton($data);
                    ?>
                    <div style = 'width:15px;'></div>
                    <?php
                        $data = [
                            "id" => "research_link_display_import",
                            "text" => "Import",
                            "onclick" => "researchHandler.importTheLink(true);",
                            ];
                        print returnTileButton($data);
                    ?>
                </div>
            </div>
        </div>
     </div>
</div>

