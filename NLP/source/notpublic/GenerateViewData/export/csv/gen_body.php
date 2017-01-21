<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////////////////////////////////// 
initializeModelModule("mysqli_interface");
/////////////////////////////////////////////


function gen_body($type, $quantity){
    // Quantity is based on word count. 
    // Grab a document, add to array, count words, repeat untill word count is met.
    
    $words = [];
    $doc_index = $infi_loop_prevention_index = 0;
    $lastDataID = -3;
    $doneFull = true;
    while(count($words) < $quantity && $infi_loop_prevention_index < 2500){
        
        //print "<Br> --- ---<Br> ";
        
        //print "limit : $limit";
        //print "<br>";
        //////////////////
        // Grab a document
        //////////////////
        $mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
        $stmt = $mysqli->prepare("SELECT DataID, Data FROM `Parsed_Data` WHERE `ParseType` = ? ORDER BY DataID ASC LIMIT ?, 1");
        print   $mysqli->error;
        $stmt->bind_param("ss", $type, $doc_index);
        $stmt->execute();
        $stmt->store_result();
        $numRows = $stmt->num_rows;
        //print "rows : " . $numRows . " <Br>";
        $stmt->bind_result($dataID, $data);  
        while($stmt->fetch()){
            //print "Here i am! Parsing $dataID <Br>";
        }
        $stmt->free_result();
        $stmt->close();
        //var_dump($numRows);
        //var_dump($data);
        if($numRows == 0){
            //print "No more to parse - ran out of data.";
            $doneFull = false;
            break;
        }
        $lastDataID = $dataID;
        $theseWords = json_decode($data);
        $words = array_merge($words, $theseWords);
        //var_dump(count($words));
        //print "<Br> --- ---<Br> ";
        
        $doc_index++;
        $infi_loop_prevention_index++; //redundant, but more readable
    }
    
    if($doneFull){
        $words = array_slice($words, 0, $quantity);
    }
    //var_dump($words);

    $words = json_encode($words);
    $words = substr($words, 1); // remove first character ( the "["] ) for csv formatting
    $words = substr($words, 0, -1); // remove last charater ( the "]" ) for csv formatting
    return [$doneFull, $words];
}