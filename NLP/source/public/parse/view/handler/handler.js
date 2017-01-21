var parseHandler = {
    buttonHandler : null,
    DOM : {
        input : {},
    },
    
    submitParsingOf : function(type){
        if(type !== "basic"){
            console.log("parsing of non known type was requested");
            return;
        }
        amount = this.DOM.input.amount.value;
        max_for_type = this.DOM.input.left[type].value;
        console.log("max for basic : " + max_for_type);
        if(!(amount > 0)){
            alert("amount requested not greater than 0");
            return;
        } else if(amount > max_for_type){
            alert("amount greater than max for type");   
            return;
        }
        this.submit(type, amount);
    },
    
    submit : function(type, amount){
        this.buttonHandler[type].displayLoading();

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/0_Input_Channel/parse/submit.php", true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.onload = function () {
            console.log(this.responseText);
            window["parseHandler"].buttonHandler[type].displayDefault();  
            /*
            var response = this.responseText.split("[[==]]");
            if(response[1] == "SCS"){
                alert("Success!");   
            } else if (response[1] == "ALREADY"){
                alert("Already Processed");   
            } else if (response[1] == "ERR"){
                alert("URL not valid - returns no HTML");   
            }
            window["sourceSubmissionHandler"].buttonHandler[type].displayDefault();   
            */
        };
        xhr.send('type='+type+'&amt='+amount);
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