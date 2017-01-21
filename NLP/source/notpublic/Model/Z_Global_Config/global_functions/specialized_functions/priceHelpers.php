<?php


function returnWithZerosOnPrice($total){
    $total = explode(".", $total);
    $total[1] .= "";
    while(strlen($total[1]) < 2){
        $total[1] .= "0";   
    }
    $total[1] = substr($total[1], 0, 2);
    $total = implode(".", $total);
    return $total;
}