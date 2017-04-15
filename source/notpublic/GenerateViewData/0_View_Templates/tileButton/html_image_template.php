
<?php //if( isset($button["defaultImg"]) && isset($button["hoverImg"]) && $button["align"] == "right" ) : ?>


<?php


?>

<div class = 'flexme' style = 'min-width:24px; max-height:100%;'>
    <div style = 'margin:auto;'>
        <img  class = 'hoverhide' src = '<?php print $button["defaultImg"]; ?>' style = 'width:26px; <?php print $button["imageExtra"]; ?>; <?php print $button["imageMargins"]; ?>'>
        <img  class = 'hovershow' src = '<?php print $button["hoverImg"]; ?>' style = 'width:26px; <?php print $button["imageExtra"]; ?>; <?php print $button["imageMargins"]; ?>'>
    </div>
</div>