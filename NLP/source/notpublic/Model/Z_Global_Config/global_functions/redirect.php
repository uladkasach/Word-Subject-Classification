<?php

/////////////////
/*
    Primary purpose is to die after header is sent and send proper headers easily and uniformly
*/
/////////////////

function redirect($where, $type){
    header("location: $where");
    die();
}

?>