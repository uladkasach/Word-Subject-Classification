var parseHandler = {
    buttonHandler : null,
    DOM : {
        input : {},
    },
    
    submitParsingOf : function(type){
        if(type !== "basic" && type !== "stop"){
            console.log("parsing of non known type was requested");
            return;
        }
        amount = parseInt(this.DOM.input.amount.value);
        max_for_type = parseInt(this.DOM.input.left[type].value);
        console.log("max for " + type + " : " + max_for_type);
        if(!(amount > 0)){
            alert("amount requested not greater than 0");
            return;
        } else if(amount > max_for_type){
            console.log(max_for_type);
            console.log(amount);
            console.log(amount > max_for_type);
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
    
    
}