<?php
/////////////////
// Basic Parse :
/* 
    Extract text from elements
        - (Not Basic Enough) only choose text which has more than 5 words around it (removes headers, bullet points, simple things around it. ????? )
        - (Not implemented on purpose) throwout meta, throwout scripts
        
   Normalize:
        - Lowercase everything
        - remove numbers                    (?) -vs- replace with NUM (-------------------- optimization)
        - multiple whitespace = one whitespace
        -  remove ALL nonalpha characters   (?) -vs- remove all nonalpha characters except "'", and ".", (----------- optiization)
   Tokenize: 
        - Split words into an array/list
            - e.g., "the", "sly", "fox", "jumped", "over", ...
            
   Cont Normalize:
        - remove stopwords  (MYSQL STOP WORDS)
*/


function normalizationPartOne($content){
    //used because stopwords needs same normalization
 
    $content = preg_replace("/[\r\n]+/", " ", $content); // replace new lines with spaces
    $content = strtolower($content); // lowercase everything
    $content = preg_replace('/[0-9]+/', '', $content); // remove all numbers
    $content = preg_replace("/[^A-Za-z_' ]/", ' ', $content); // remove all nonalpha characters excluding _ and '
    $content = preg_replace('/\s+/', ' ', $content); // replace multiple white spaces with one white space

    return $content;
}

function DOMinnerHTML(DOMNode $element) { 
    $innerHTML = ""; 
    $children  = $element->childNodes;

    foreach ($children as $child) 
    { 
        $innerHTML .= $element->ownerDocument->saveHTML($child);
    }

    return $innerHTML; 
} 



function parseThisURL($html){
    
    /////////////////////////////
    // Get text from document (very naieve approach)
    //   + remove scripts
    //////
    $dom = new DOMDocument();
    $dom->loadHTML(mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8')); // This way we dont get funny letters
    $dom->strictErrorChecking = false;
    $dom->formatOutput = true;
    // remove scripts and styles
    while (($r = $dom->getElementsByTagName("script")) && $r->length) {
            $r->item(0)->parentNode->removeChild($r->item(0));
    }
    while (($r = $dom->getElementsByTagName("style")) && $r->length) {
            $r->item(0)->parentNode->removeChild($r->item(0));
    }
    
    
    // get content in plain text format
    //$content = $dom->textContent; - deprecated 1/18/17 
    $content = $dom->saveHTML();
    $content = strip_tags($content); // remove html tags
    $content = html_entity_decode($content); // Clean up things like &amp;
    $content = urldecode($content); // Strip out any url-encoded stuff
    
    $content = preg_replace_callback("/(&#[0-9]+;)/", function($m) {  // Strip out any improperly encoded data
        $result = mb_convert_encoding($m[1], "UTF-8", "HTML-ENTITIES"); 
        //var_dump($result);
        //var_dump(bin2hex($result));
        //var_dump(bin2hex(""));
        $boolean = $result == "" || bin2hex($result) == "c297";
        //var_dump($boolean);
        if($boolean){
            return " ";   
        } 
        return $result;
    }, $content); 
    
    //var_dump($html);
    var_dump($content);

    /////////////////////////////
    // Normalize Part One
    ////
    $content = normalizationPartOne($content);
    //var_dump($content);
    
    //////////////////////////////
    // Tokenize
    ////
    $content = explode(" ", $content);
    
    //////////////////////////////
    // Normalize part 2 (token based)
    ////
    $old_content = $content;
    $content = [];
    $lastWord == "";
    for($index = 0; $index < count($old_content); $index++){
        $thisWord = $old_content[$index];
        $fails_booleans = false;
        
        $thisWord = trim ($thisWord, $character_mask = "_ \t\n\r\0\x0B");
        
        $stripped = preg_replace("/[^A-Za-z]/", '', $thisWord);
        if($stripped == ""){
            $fails_booleans = true;   
        }
        if($thisWord = $lastWord){ /////////////// Eliminate Repetitions
            $fails_booleans = true;
        }
        

        if(!$fails_booleans){
            $content[] = $thisWord;   
        }
    }
    //var_dump(implode(" ", $content));

    return $content;
}
   
