<?php

    $urlToScan = "http://www.homedepot.com/b/Outdoors-Garden-Center-Garden-Plants-Flowers/N-5yc1vZc8rg";

    if(!isset($userAgent)){
      $userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36";
    }

    $ch = curl_init();
    $timeout = 15;
    curl_setopt($ch, CURLOPT_COOKIESESSION, true );
    curl_setopt($ch, CURLOPT_USERAGENT,$userAgent);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_BINARYTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_REFERER, "http://www.gutenberg.org/ebooks/34175?msg=welcome_stranger");
    #curl_setopt($ch, CURLOPT_HEADER, 1); // return HTTP headers with response
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_URL, $urlToScan);
    $html = curl_exec($ch);
    curl_close($ch);

    if($html == null){
        return false;  
    } 
    print $html;

?>