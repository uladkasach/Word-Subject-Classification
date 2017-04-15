<?php

class SessionInterface {
    protected $sessionDataLocation = null;
    protected static $possibleSessionTypes = array(
            "userData" => "8djl2n09zja121zls",
            "registration_finalized_data" => "2j1ja1dcd0qv1dd0azj321j0zldo",
    );
    
    
    function __construct($type){
        $address = self::$possibleSessionTypes[$type];
        if(isset($address)){
            self::defineSessionDataLocation($address);   
        } else {
            print "Session Type Not Defined!!!";
            die();
        }
    }
    
    
    ////////////////////////
    // Define Functions
    ////////////////////////
    function defineSessionDataLocation($location){
        $this->sessionDataLocation = $location;
    }
    
    function returnDataStoredInSession(){
        session_start();
        session_write_close();
        return $_SESSION[$this->sessionDataLocation];
    }
    
    function setDataIntoSession($data){
        session_start();
        $_SESSION[$this->sessionDataLocation] = $data;
        session_write_close();
    }
};