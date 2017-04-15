<a id = '<?php print $button["id"]; ?>-button'
   href = '<?php print $button["href"]; ?>'
   class = 'flexme unselectable hoverImgChange tileButtonText<?php print $specModifier; ?>' 
   style = '  <?php print $fillWidth; ?>; padding:0px 16px; border-radius:2px; height:36px;  <?php print $marginAdjustment; ?>; font-size:<?php print $fontSize; ?>;  font-weight:bold;'
   onclick = '<?php print $button["onclick"]; ?>'
   target = '<?php print $button["target"]; ?>' 
   <?php if(isset($button["download"])):?>
        download = '<?php print $button["download"]; ?>'
   <?php endif; ?>
   >
   <div class = 'flexme' style = '<?php print $fillWidth; ?>;'>
       
       
        <div id = '<?php print $button["id"]; ?>-buttonDefaultText' class = '' style = 'margin:auto; <?php print $fillWidth; ?>;' >
            <div style = 'width:100%;' class = 'flexme '>
                <?php print $imageLeft["default"]; ?>
                <div class = 'flexme ' style = ''>
                    <div style = 'margin:auto;  '>
                        <?php print ($button["text"]); ?>
                    </div>
                </div>
                <?php print $imageRight["default"]; ?>
            </div>
        </div>
       
        <div id = '<?php print $button["id"]; ?>-buttonDisabledText' title = '<?php print $button["disabledTitle"]; ?>' class = 'disnon' style = 'margin:auto; <?php print $fillWidth; ?>;' >
            <div style = 'width:100%;' class = 'flexme'>
                <?php print $imageLeft["disabled"]; ?>
                <div class = 'flexme' style = ''>
                    <div style = 'margin:auto;> '>
                        <?php print ($button["text"]); ?>
                    </div>
                </div>
                <?php print $imageRight["disabled"]; ?>
            </div>
        </div>
       
        <div id = '<?php print $button["id"]; ?>-buttonSelectedText' style = 'margin:auto; ' class = 'disnon'>
                <?php print ($button["text"]); ?>
        </div>
       
        <div style = 'margin:auto; position:relative;' class = 'disnon' id = '<?php print $button["id"]; ?>-buttonloadingImageHolder'>
            <div class = 'flexme' style = 'position:absolute; width:100%;'>
                <div style = 'margin:auto;'>
                    <div class="spinner_smaller" style = ''>
                      <div class="dot1"></div>
                      <div class="dot2"></div>
                    </div>
                </div>
            </div>
            <div id = '' class = '' style = 'margin:auto; <?php print $fillWidth; ?>; visibility:hidden;' >
                <div style = 'width:100%;' class = 'flexme'>
                    <?php print $imageLeft["default"]; ?>
                    <div class = 'flexme' style = ''>
                        <div style = 'margin:auto;> '>
                            <?php print ($button["text"]); ?>
                        </div>
                    </div>
                    <?php print $imageRight["default"]; ?>
                </div>
            </div>
        </div>
   </div>
</a>

<?php
if(isset($button["id"])):
   ?>
<?php require_once("init.php"); ?>    
  

<script>
    if(window["buttonHandler"] == undefined){
        window["buttonHandler"] = {};   
    }
    var theID = "<?php print $button["id"]; ?>";
    (function(id){
        thisButton_handler = new global_buttonHandler();
        thisButton_handler.classes = {default : "tileButtonText<?php print $specModifier; ?>", static : "titleButtonText_selected", disabled : "tileButtonText_disabled", root : "flexme unselectable hoverImgChange "};
        thisButton_handler.DOM = {
            main : document.getElementById(id+"-button"), 
            defaultText : document.getElementById(id+"-buttonDefaultText"),
            selectedText : document.getElementById(id+"-buttonSelectedText"),
            disabledText : document.getElementById(id+"-buttonDisabledText"),
            loadingImageHolder : document.getElementById(id+"-buttonloadingImageHolder"),
        };
        thisButton_handler.devmode = false;
        if(window["buttonHandler"] == undefined){
            window["buttonHandler"] = {};   
        }
        window["buttonHandler"][id] = thisButton_handler;
    })(theID);
    <?php if($button["disabled"] == true): ?>
        window["buttonHandler"][theID].displayDisabled();
    <?php endif; ?>
    
</script>



    <?php
endif; 
?>