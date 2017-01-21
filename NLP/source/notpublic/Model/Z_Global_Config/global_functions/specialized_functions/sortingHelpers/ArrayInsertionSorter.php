<?php

class ArrayInsertionSorter {
    function returnArraySortedByInsertion($array, $order, $key){
        // Order = Ascending vs Descending = ASC vs DESC
        // Key = if array holds arrays, which key holds the value
        self::verifyThatArrayIsUsable($array, $order, $key);
        $total = count($array);
        //print "init ---";
        //var_dump($array);
        //print "<Br><Br>";
        for($index = 0; $index < $total; $index++){
            self::moveElementBackUntillPlaceIsFound($array, $index, $order, $key); // Array is Pased by Reference
            //print "<br>After for $index ---";
            //var_dump($array);
            //print "<Br><Br>";
        }
        
        return $array;
    }
    
    function verifyThatArrayIsUsable($array, $order, $key){
        $keys = array_keys($array);
        if($keys[0] !== 0){
            print "This is a key value pair array, not just a value array. Can not run insertion sort on this. Error.";
            die();
        }
        if(isset($key)){
            if(!isset($array[0][$key])){
                print "Key is defined for this insertion sort, but the key holds no values. Error.";
                die();
            }
        }
        if($order !== "ASC" && $order !== "DESC"){
            print "Order is not ASC nor DESC"; 
            die();
        }
    }
    
    function moveElementBackUntillPlaceIsFound(&$array, $index, $order, $key){
        $origValue = self::getValueAtIndex($array, $index, $key);
        $index--;
        while($index > -1){
            //print "running for $index;";
            $thisValue = self::getValueAtIndex($array, $index, $key);
            $bool = self::evaluate($order, $thisValue, $origValue);
            
            //print "$thisValue -vs- $origValue --";
            //var_dump($bool);
            //print $bool;
            if($bool){
                // its place has been found, done.
                break;
            }
            /*
                $inP1 = $index + 1;
                print " -> Swap arr[$index] and arr[$inP1]";
                print "<Br>";
            */
            swapArrayElements($array, $index, $index+1);
            $index--;
        }
        
    }
    
    function evaluate($order, $value1, $value2){
        if($order == "ASC"){ //Lowest to Highest
            $bool = $value1 < $value2;
        } else if ($order == "DESC"){
            $bool = $value1 > $value2;   
        }
        //print "bool : " . $bool . "---";
        return $bool;
    }
    
    function getValueAtIndex($array, $index, $key){
        if(isset($key)){
            $thisValue = $array[$index][$key];   
        } else {
            $thisValue = $array[$index];
        }
        return $thisValue; 
    }
    
};

$GLOBALS["ArrayInsertionSorter"] = new ArrayInsertionSorter();

