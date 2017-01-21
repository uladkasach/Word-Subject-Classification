

Data_Manipulation - Classes that manipulate data, sign in, logon, new item (validate information and logic)



DataStructure_Interfaces - Classes that actually update the databases, session data, cookies, local file hosting, etc (interface with the database)



/////////////////////////////////////// OLD BELOW - DOES NOT APPLY //////////////////////////////////////////////////////



This project uses PHP Autoloader as described on http://php.net/manual/en/language.oop5.autoload.php

Files include classes/objects using Autoloader, each class has a file in the Z_Includes folder which contains the path to its definition. Autoloader includes each class from the Z_includes folder. This way file structure can be manipulated without effecting includes.
-Note- Name structure of classes can not easily be manipulated however.

Model folder - contains classes that manipulate data and interact with databases, data, and file structures
Control folder - contains scripts that receive user input from View and react by triggering specific Model actions, and then respond to view.
View files are found under the "public" directory.



Model folder contains 