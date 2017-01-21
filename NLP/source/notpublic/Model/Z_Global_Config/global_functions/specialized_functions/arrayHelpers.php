<?php


function stripKeysFromArray($data){
    $newData = [];
    $keys = array_keys($data);
    $total = count($data);
    for($index = 0; $index < $total; $index++){
        $thisKey = $keys[$index];
        $newData[] = $data[$thisKey];
    }
    return $newData;
}


function swapArrayElements(&$array, $index1, $index2){
    if($index1 == $index2){
        return;   
    }
    $hold = $array[$index1];
    $array[$index1] = $array[$index2];
    $array[$index2] = $hold;
}
