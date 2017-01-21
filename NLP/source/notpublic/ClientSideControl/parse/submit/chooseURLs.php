<?php

function chooseURLs($type, $amount){
    $urlsToParse = [];
    
    ///////////////
    // Get all URLS's that do not have the type already parsed for them 
    ///////////////
    //$query = "SELECT Source_HTML.URL, Parsed_Data.URL, Source_HTML.SourceID, Parsed_Data.ParseType FROM Source_HTML LEFT OUTER JOIN Parsed_Data ON Source_HTML.URL = Parsed_Data.URL WHERE Parsed_Data.ParseType != 'basic' OR (Source_HTML.URL IS NOT NULL AND Parsed_Data.URL IS NULL)";  // "anti-join"
    
    $mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
    $stmt = $mysqli->prepare("SELECT Source_HTML.SourceID, Source_HTML.URL FROM Source_HTML LEFT OUTER JOIN Parsed_Data ON Source_HTML.URL = Parsed_Data.URL WHERE Parsed_Data.ParseType != ? OR (Source_HTML.URL IS NOT NULL AND Parsed_Data.URL IS NULL) ORDER BY Source_HTML.DateTimeRecorded ASC LIMIT ?");
    print   $mysqli->error;
    $stmt->bind_param("si", $type, $amount);
    $stmt->execute();
    $stmt->store_result();
    $numRows = $stmt->num_rows;
    $stmt->bind_result($sourceID, $sourceURL);  
    while($stmt->fetch()){
        $urlsToParse[] = $sourceURL;
        //var_dump($sourceURL);
    }
    $stmt->free_result();
    $stmt->close();
    
    return $urlsToParse;
}