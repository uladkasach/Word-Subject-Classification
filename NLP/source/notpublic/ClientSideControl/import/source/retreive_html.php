<?php


function retreive_html($urlToScan, $userAgent){
    if(!isset($userAgent)){
      $userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36";
    }
    
    $ch = curl_init();
    $timeout = 15;
    curl_setopt($ch, CURLOPT_USERAGENT,$userAgent);
    curl_setopt ($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_BINARYTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_URL, $urlToScan);
    $html = curl_exec($ch);
    curl_close($ch);
  
    if($html == null){
        return false;  
    } 
    return $html;
}