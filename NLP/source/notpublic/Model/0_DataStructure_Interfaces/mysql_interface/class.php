<?php

class MySQLManager {
    protected static $users = null;
    protected static $databaseName = null;
    
    function defineUsers($users){
        self::$users = $users;   
    }
    function defineDatabaseName($databaseName){
        self::$databaseName = $databaseName;   
    }
 
    function returnMysqliObjectFor($user){
        
        if(!isset(self::$users[$user])){
            print "Error, that user requested for mysqli object is not defined.";
            die();
        }
        
        /////////////////
        // Upon creating the mysqli object, replace the $users[$user] value with the object
        /////////////////
        if(is_string(self::$users[$user])){
            $mysqli = mysqli_connect("localhost", $user, self::$users[$user],self::$databaseName);
            if (mysqli_connect_errno()) {
                echo "Failed to connect to MySQL: " . mysqli_connect_error();
                die();
            }      
            self::$users[$user] = $mysqli;
        } 
        
        return self::$users[$user];
    }
    
    
};