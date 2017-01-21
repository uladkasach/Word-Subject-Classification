<?php


////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
// Get and Measure Questions and Answers ///////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
function DOMinnerHTML(DOMNode $element) { 
    $innerHTML = ""; 
    $children  = $element->childNodes;

    foreach ($children as $child) 
    { 
        $innerHTML .= $element->ownerDocument->saveHTML($child);
    }

    return $innerHTML; 
} 
function getElementsByClass(&$parentNode, $tagName, $className, $exact) {
    $nodes=array();
    $childNodeList = $parentNode->getElementsByTagName($tagName);
    if($exact == 1){
        for ($i = 0; $i < $childNodeList->length; $i++) {    
            $temp = $childNodeList->item($i);
            if ($temp->getAttribute('class') == $className) {
                $nodes[]=$temp;
            }
        }
    } else {
        for ($i = 0; $i < $childNodeList->length; $i++) {    
            $temp = $childNodeList->item($i);
            if (stripos($temp->getAttribute('class'), $className) !== false) {
                $nodes[]=$temp;
            }
        }
    }
    return $nodes;
}

/*
function getDataAndMetrics($html){
    $dom = new DOMDocument();
    $dom->loadHTML(mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8')); // This way we dont get funny letters
    //$dom->loadHTML( $html );
    $dom->strictErrorChecking = false;
    $datas = getElementsByClass($dom, 'div', 'ugc-base');
    //var_dump($datas[0]);
    if($datas[0] == null){
        print "<Br><Br> The value is null - question does not exist at this URL <Br> Returning Skip function data.";
        return "QuestionNoExist";
    } else if(count($datas) < 2){
        print "<Br><Br>!!!!!!!!!!!!!! No Questions or Answers have been found. Terminating. !!!!!!!!!!!!!! <br><Br> Return the PHPSESSIDexpired function data.";
        return "PHPSESSIDexpired";
    }
    ////////////////////////////////////////////////////////////////////////////////////////////
    // Get Question and Measure  ///////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////
    $question = $datas[0];
    $questionCharLen = strlen($question->nodeValue);
    $questionHTML = htmlentities(DOMinnerHTML($question));
    $questionImgCount = $question->getElementsByTagName("img")->length;
    //print $questionHTML;
    print "<Br>";
    print "<Br> Question";
    //print "<Br> HTML = " . $questionHTML;
    print " Char : " . $questionCharLen;
    print ", Img : " . $questionImgCount;
    $questionMetrics = $questionCharLen . "[|+|]" . $questionImgCount;
    
    
    $answers = array();
    $answerMetrics = array();
    ////////////////////////////////////////////////////////////////////////////////////////////
    // Get Answers and Measure  ////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////////////////////
    $total = count($datas);
    //print $total;
    $count = 1;
    while($count < $total){
        $answer = $datas[$count];
        //var_dump($answer);
        $answerCharLen = strlen($answer->nodeValue);
        $answerHTML = htmlentities(DOMinnerHTML($answer));
        $answerImgCount = $answer->getElementsByTagName("img")->length;
        if(count(getElementsByClass($dom, 'span', 'rating-stars')) > 0 && $count == 1){
            $hasRating = 1;
        } else {
            $hasRating = 0;   
        }
        if($hasRating == 1){
            $bestAnsRating = getElementsByClass($dom, 'span', 'rating-stars')[0]->getAttribute('data-count');
        }
        print "<Br>";
        print "<Br> Answer";
        if($hasRating == 1){
            print " Rating : " . $bestAnsRating . "/5";
        }
        print ", Char : " . $answerCharLen;
        print ", Img : " . $answerImgCount;    
        
        $metricString = $answerCharLen . "[|+|]" . $answerImgCount;
        if($hasRating == 1){
            $metricString .= "[|+|]" . $bestAnsRating;   
        }
        $answerMetrics[] = $metricString;
        $answers[] = $answerHTML;
        $count += 1;   
    }
    
    //print html_entity_decode($answers[3]);
    
    
    $answerCount = count($answers);
    $answers = implode("[++||==||++]",$answers);
    $answerMetrics = implode("[++||==||++]",$answerMetrics);
    return array($questionHTML, $questionMetrics, $answers, $answerMetrics, $answerCount);
}// End get data and metrics
////////////////////////////////////////////////////////////////////////////////////////////

*/