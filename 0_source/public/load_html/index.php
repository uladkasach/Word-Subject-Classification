<?php
/////////////////////////////////////////////
// Sets Global Variables and Functions
/////////////////////////////////////////////
require_once($_SERVER["DOCUMENT_ROOT"] . "/../notpublic/config.php");
///////////////////////////////////////////// 
initializeModelModule("mysqli_interface");
/////////////////////////////////////////////


/*
for all html_data that have null as html, reload the html. 
    - sometimes the html is removed to reload it.
*/
//UPDATE `Source_HTML` SET `HTML`= '' WHERE SourceID > 407


///////////////
// Method : get the urls and loop call source_include.php, with $rescan_override['id'] as the id and $rescan_override['html'] as the html
$the_urls_to_load_HTML_for = [];
$mysqli = $GLOBALS["MYSQLI_MANAGER"]->returnMysqliObjectFor("NLP_main");
$stmt = $mysqli->prepare("SELECT Source_HTML.SourceID, Source_HTML.URL FROM Source_HTML WHERE Source_HTML.HTML = ''");
print   $mysqli->error;
//$stmt->bind_param("si", $type, $amount);
$stmt->execute();
$stmt->store_result();
$numRows = $stmt->num_rows;
$stmt->bind_result($sourceID, $sourceURL);  
while($stmt->fetch()){
    $the_urls_to_load_HTML_for[] = [$sourceID, $sourceURL];
    //var_dump($sourceURL);
}
$stmt->free_result();
$stmt->close();
    


$rescan_override['id'] = "517";
$rescan_override['url'] = "http://www.gutenberg.org/cache/epub/10962/pg10962.txt";

for ($the_i = 0; $the_i < count($the_urls_to_load_HTML_for); $the_i++) {
    $rescan_override = [
        "id" => $the_urls_to_load_HTML_for[$the_i][0],
        "url" => $the_urls_to_load_HTML_for[$the_i][1],
        ];
    require(NOTPUBLIC_ROOT."/ClientSideControl/import/source/include.php");
}

#print $html;