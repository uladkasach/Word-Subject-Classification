<?php

function uniformDateLook($date){
    return date('M n, Y', strtotime($date));   
}