<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////////////////////////////////// 

function parseURLs($urls, $type){
    $type_list = [
        "basic" => NOTPUBLIC_ROOT . "/ClientSideControl/parse/submit/parse_types/basic/include.php",
    ];
    if(!in_array($type, array_keys($type_list))){
        print "Parse type does not exist. Error.";
        die();
    }
    
    ////////////////
    // Include the parseFunction
    ////////////////
    require_once($type_list[$type]);
    
    //var_dump($urls);
    
    ////////////////
    // For each URL, get the HTML, run the parse, store the result in json
    ////////////////
    for($index = 0; $index < count($urls); $index++){
        $thisURL = $urls[$index];
        var_dump($thisURL);
        $thisHTML = returnHTMLFor($thisURL);
        $result = parseThisURL($thisHTML);
        $json = json_encode($result);
        var_dump($json);
        recordParseResult($thisURL, $type, $json);
    }
    
}


function recordParseResult($url, $type, $json){
    
    
    $mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
    $when = date('Y-m-d H:i:s');
    $stmt = $mysqli->prepare("INSERT INTO Parsed_Data (`URL`, `ParseType`, `Data`) VALUES (?, ?, ?)");
    //print "INSERT INTO Parsed_Data (`URL`, `ParseType`, `Data`) VALUES ($url, $type, $json)";
    echo $mysqli->error;
    $stmt->bind_param("sss", $url, $type, $json);
    $exec = $stmt->execute();
    $stmt->close();
    ////////////////////////
    var_dump($exec);
    //print "here i am!";
    if(!$exec){
        print "[[==]]ERR[[==]]";
        die();
    } 
    
    return true;
}

function returnHTMLFor($thisURL){
    
    
    $mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
    $stmt = $mysqli->prepare("SELECT `HTML` FROM Source_HTML WHERE `URL` = ?");
    print   $mysqli->error;
    $stmt->bind_param("s", $thisURL);
    $stmt->execute();
    $stmt->store_result();
    $numRows = $stmt->num_rows;
    $stmt->bind_result($html);  
    while($stmt->fetch()){    }
    $stmt->free_result();
    $stmt->close();

    return $html;
}