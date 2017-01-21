<?php
//////////////////////////
// Purpose : 
// define development options in one place for easy toggling between development and production environments
//////////////////////////

$GLOBALS['DEV_OPS'] = [];
$GLOBALS['DEV_OPS']['actually_send_communication_emails'] = false;
$GLOBALS['DEV_OPS']['sunlogs_devmode'] = true;
$GLOBALS['DEV_OPS']['serve_image_dev_domain'] = true;