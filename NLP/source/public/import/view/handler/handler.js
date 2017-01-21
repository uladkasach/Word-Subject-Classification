var sourceSubmissionHandler = {
    buttonHandler : null,
    DOM : {
        input : {},
    },
    
    callbackForSuccess : function(){
       this.callbackForFinalSuccess();  
    },
    
    callbackForFinalSuccess : function(){
        alert("Success!");
    },
    
    submit : function(){
        string = this.returnValidationReport();
        if(string !== true){
            //console.log(string);
            alert(string);
            return;
        }
        var source_url = encodeURIComponent(this.DOM.input.source_url.value);
        this.buttonHandler.displayLoading();
        
        /*
        var keys = Object.keys(this.DOM.input);
        var totalElements = keys.length;
        for(var index = 0; index < totalElements; index++){
            var thisKey = keys[index];
            var thisElement = this.DOM.input[thisKey];
            thisElement.DOM.inputElement.disabled = 'true';
            thisElement.DOM.inputElement.blur();
        }
        */
        
        
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/0_Input_Channel/import/source.php", true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.onload = function () {
            console.log(this.responseText);
            var response = this.responseText.split("[[==]]");
            if(response[1] == "SCS"){
                alert("Success!");   
            } else if (response[1] == "ALREADY"){
                alert("Already Processed");   
            } else if (response[1] == "ERR"){
                alert("URL not valid - returns no HTML");   
            }
            window["sourceSubmissionHandler"].buttonHandler.displayDefault();   
            /*
                var response = this.responseText.split("[[==]]");
                if(response[1] == "SCS"){
                    console.log("Registration success, running callback");
                    window["registrationHandler"].callbackForSuccess();
                } else if (response[1] == "ALRDY"){
                    location.reload(true);
                } else {
                    alert("Sorry, there has been an error. Please contact support.");
                    window["registrationHandler"].buttonHandler.displayDefault();   
                }
            */
        };
        xhr.send('source_url='+source_url);
    },
    
    returnValidationReport : function(){
        var string = "";

        var source_url = this.DOM.input.source_url.value;

        if(source_url.replace(/ /g,'') == ""){
            string += " - Source URL is empty\n";   
        }
        regEx = /^((?:(?:(?:https?|ftp):)?\/\/)?)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})).?)(?::\d{2,5})?(?:[/?#]\S*)?$/i;
        result = regEx.test( source_url );
        if(!result){
            string += " - Source URL is not valid\n";   
        }
        
        if(string !== ""){
            string = "Please fix the following errors before submitting : \n" + string; 
            return string  
        } else {
            return true;   
        }
    },
    
}