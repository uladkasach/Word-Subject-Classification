<?php

////////////////////////////////
/// V1.2.4 - 10.10.15 ///////////
////////////////////////////////
// Changed "changeIP" to flag - for better handling of errors and etc. 10/10



/////////////////////////////////
///////
/* 
// Development mode is needed to specify wether to send to localhost sunlogs or real sunlogs, as well as to decide weather to display the warning or not. Displaying warning if receiver isnt availible could lead to bad senarios on a production website.

    
////////////////////////////////////////////////////////////////////////////////////////////////////////
include_once($_SERVER['DOCUMENT_ROOT'] . "/../notpublic/X_ternal_Interfaces/SunLogs/log.php");   
sendALog($extra);
////////////////////////////////////////////////////////////////////////////////////////////////////////
    
*/
//////
/////////////////////////////////

function sendALog($extra, $flag){
return;
////////////////////////////////////////////////////////////////
/// Specify if it is in development mode ///////////////////////
////////////////////////////////////////////////////////////////
$developmentMode = $GLOBALS['DEV_OPS']['sunlogs_devmode'];
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////
/// Set the authentication parameters //////////////////////////
////////////////////////////////////////////////////////////////
$repoName = "PhotoSched";
$key = "QMasd2kqSuExaAphIOXMBNtQeVNnJXTBuOF"; 
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
/// Make sure required parameters are set //////////////////////
////////////////////////////////////////////////////////////////
if(!isset($developmentMode)){
    print "DevelopmentMode Definition is not set.";
    die();
}
if(!isset($repoName)){
    print "DevelopmentMode Definition is not set.";
    die();
}
if(!isset($key)){
    print "DevelopmentMode Definition is not set.";
    die();
}
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
/// Specify where the receiver is //////////////////////////////
////////////////////////////////////////////////////////////////
if($developmentMode == true){
    $url = "http://localhost:333/receiver.php";
} else {
    $url = "http://sunlogs.com/receiver.php";
}
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
/// Generate required data /////////////////////////////////////
////////////////////////////////////////////////////////////////
date_default_timezone_set("UTC");
$when = date('Y-m-d H:i:s');
$key = md5(md5($key).$when);
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
/// Set the data fields required for the log ///////////////////
////////////////////////////////////////////////////////////////
if(!isset($extra)){
    $extra = "";   
}
if(!isset($flag)){
    $flag = "";   
}
$ip = $_SERVER['REMOTE_ADDR'];
    if(!isset($ip)){
        $ip = ""; 
    }
$for = $_SERVER['HTTP_X_FORWARDED_FOR'];
    if(!isset($for)){
        $for = ""; 
    }
$agent = $_SERVER['HTTP_USER_AGENT'];
    if(!isset($agent)){
        $agent = ""; 
    }
$refer = $_SERVER['HTTP_REFERER'];
    if(!isset($refer)){
        $refer = ""; 
    }
    
$uri = $_SERVER['REQUEST_URI'];
    if(!isset($uri)){
        $uri = ""; 
    }
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
/// Put all data to be sent in correct format //////////////////
////////////////////////////////////////////////////////////////
$postdata = http_build_query(
    array(
       'when'=>$when,
       'logtype'=>'php',
       'IP'=> $ip,
       'forwardedFor'=> $for,
       'agent'=> $agent,
       'referer'=> $refer,
       'requestURI'=> $uri,
       'extra' => $extra,
       'repoName' => $repoName,
       'key' => $key,
       'flag' => $flag,
    )
);
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////
/// Send the request  //////////////////////////////////////////
////////////////////////////////////////////////////////////////
$ch = curl_init(); // create curl handle
curl_setopt($ch,CURLOPT_URL,$url);
curl_setopt($ch,CURLOPT_POST, true);
curl_setopt($ch,CURLOPT_POSTFIELDS, $postdata);
curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch,CURLOPT_CONNECTTIMEOUT, 3); //timeout in seconds
curl_setopt($ch,CURLOPT_TIMEOUT, 20); // same for here. Timeout in seconds.
$response = curl_exec($ch);
curl_close ($ch); //close curl handle
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////
//echo $response;


////////////////////////////////////////////////////////////////
/// Notify Vlad when he forgets to turn dev mode off ///////////
////////////////////////////////////////////////////////////////
if($developmentMode == true){
    if(explode("[++==++]",$response)[0] !== "Welcome"){
        print "
        <div style = 'position:fixed; top:0; bottom:0; left:0; right:0; font-size:70px; display:flex; text-align:center; z-index:99999999999999; background-color:rgba(255, 255, 255, 0.3);' > 
            <div style = 'position:absolute; display:flex; width:100%; height:100%;'>
                <div style = 'margin:auto;'> 
                    Sunshine!
                </div>
            </div>
        </div>
        ";
    } else if (explode("[++==++]",$response)[1] !== "SCS"){
        print "
        <div style = 'position:fixed; top:0; bottom:0; left:0; right:0; font-size:70px; display:flex; text-align:center; z-index:99999999999999; background-color:rgba(255, 255, 255, 0.3);' > 
            <div style = 'position:absolute; display:flex; width:100%; height:100%;'>
                <div style = 'margin:auto;'> 
                    Palm Trees!
                </div>
            </div>
        </div>
        ";
    } else if (explode("[++==++]",$response)[2] !== "SCS"){
        print "
        <div style = 'position:fixed; top:0; bottom:0; left:0; right:0; font-size:70px; display:flex; text-align:center; z-index:99999999999999; background-color:rgba(255, 255, 255, 0.3);' > 
            <div style = 'position:absolute; display:flex; width:100%; height:100%;'>
                <div style = 'margin:auto;'> 
                    Cool Ocean Breeze!
                </div>
            </div>
        </div>
        ";
    } else if (explode("[++==++]",$response)[3] !== "SCS"){
        print "
        <div style = 'position:fixed; top:0; bottom:0; left:0; right:0; font-size:70px; display:flex; text-align:center; z-index:99999999999999; background-color:rgba(255, 255, 255, 0.3);' > 
            <div style = 'position:absolute; display:flex; width:100%; height:100%;'>
                <div style = 'margin:auto;'> 
                    Waves!
                </div>
            </div>
        </div>
        ";
    } else if (explode("[++==++]",$response)[4] !== "GreatSCS!"){
        print "
        <div style = 'position:fixed; top:0; bottom:0; left:0; right:0; font-size:70px; display:flex; text-align:center; z-index:99999999999999; background-color:rgba(255, 255, 255, 0.3);' > 
            <div style = 'position:absolute; display:flex; width:100%; height:100%;'>
                <div style = 'margin:auto;'> 
                    Beautiful Sky!
                </div>
            </div>
        </div>
        ";
    }
}
////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////



}
?>