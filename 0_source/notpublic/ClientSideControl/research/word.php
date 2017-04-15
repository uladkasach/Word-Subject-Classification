<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////////////////////////////////// 
initializeModelModule("mysqli_interface");
/////////////////////////////////////////////


/////////////////////
// Research word system - Structure: 
/////////////////////
/*
client side: send research word
server side: get research word, return list of urls with description data provided, 1
client side: display all links received, ask whether to queue to import (true,false, check if already done), submit
                when all links are finished, ask whether to parse next page 
server side: if next page is requested, rinse and repeat properly
*/




// https://developers.google.com/custom-search/json-api/v1/overview
// API KEY :                        AIzaSyBwJn2plle1dJeuubi5Jon3BSWj1dotQvM
// subject_research search id :     008631247620893273507:vmru3a6gwmy
// https://www.googleapis.com/customsearch/v1?key=AIzaSyBwJn2plle1dJeuubi5Jon3BSWj1dotQvM&cx=008631247620893273507:vmru3a6gwmy&q=plant


/*
  "template": "https://www.googleapis.com/customsearch/v1?q={searchTerms}&num={count?}&start={startIndex?}&lr={language?}&safe={safe?}&cx={cx?}&cref={cref?}&sort={sort?}&filter={filter?}&gl={gl?}&cr={cr?}&googlehost={googleHost?}&c2coff={disableCnTwTranslation?}&hq={hq?}&hl={hl?}&siteSearch={siteSearch?}&siteSearchFilter={siteSearchFilter?}&exactTerms={exactTerms?}&excludeTerms={excludeTerms?}&linkSite={linkSite?}&orTerms={orTerms?}&relatedSite={relatedSite?}&dateRestrict={dateRestrict?}&lowRange={lowRange?}&highRange={highRange?}&searchType={searchType}&fileType={fileType?}&rights={rights?}&imgSize={imgSize?}&imgType={imgType?}&imgColorType={imgColorType?}&imgDominantColor={imgDominantColor?}&alt=json"
*/

/*

 "items": [
  {
  ...
   "title": "Plant - Wikipedia",
   ...
   "link": "https://en.wikipedia.org/wiki/Plant",
   ...
   "snippet": "Plants are mainly multicellular, predominantly photosynthetic eukaryotes of the \nkingdom Plantae. The term is today generally limited to the green plants, which ...",
   ...
   "formattedUrl": "https://en.wikipedia.org/wiki/Plant",
   ...
  },
*/
      
////////////////////////////////////
// Research Word
////////////////
$research_word = $_POST["research_word"];
$page_index = $_POST["page_index"];
//print("researching `" . $research_word . "`");



//////////////////////////////////
// Generate Query
/////////////////////////////////
$query_base = "https://www.googleapis.com/customsearch/v1?";
$query_parts = [
    "key" => "AIzaSyBwJn2plle1dJeuubi5Jon3BSWj1dotQvM",
    "cx" => "008631247620893273507:vmru3a6gwmy",
    "q" => $research_word,
    "start" => (int)$page_index * 10 + 1,
];
$full_restful_query = $query_base;
$query_keys = array_keys($query_parts);
for($i = 0; $i < count($query_keys); $i++){
    $del = $i == 0 ? "" : "&";  
    $this_key = $query_keys[$i];
    $this_val = $query_parts[$this_key];
    $this_get_string = $this_key . "=" . $this_val;
    $full_restful_query .= $del . $this_get_string;
}
//var_dump($full_restful_query);
//die();
//print("<Br><BR>");

////////////////////////
// Get the data
/////////////////////////
if(true){
    $ch = curl_init();
    $timeout = 15;
    curl_setopt ($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_BINARYTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_URL, $full_restful_query);
    $data = curl_exec($ch);
    curl_close($ch);
} else {
    ob_start();
    require("test_input.json"); 
    $data = ob_get_clean();
}
$json_data = json_decode($data, true); //true makes json into array-keys instead of "objects"
//var_dump($json_data);   


///////////////////////////////////////
// Parse the data
///////////////////////////////////////
//var_dump($json_data["items"]);
$query_results = $json_data["items"];
$relevant_data = [];
for($i = 0; $i < count($query_results); $i++){
    $this_result = $query_results[$i];
    $this_data = [
        "title" => $this_result["title"],
        "link" => $this_result["link"],
        "snippet" => $this_result["snippet"],
    ];
    $relevant_data[] = $this_data;
}

//var_dump($relevant_data);
print("[[=!!!!!!!!!!!!!=]]SCS[[=!!!!!!!!!!!!!=]]");
print("[[=!!!!!!!!!!!!!=]]".json_encode($relevant_data)."[[=!!!!!!!!!!!!!=]]");
