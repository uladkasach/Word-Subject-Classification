function theFunction(){
    sourceSubmissionHandler.DOM = {
        input : {
            source_url : window["textHandlers"]["source_url"],
        },
    };
    sourceSubmissionHandler.buttonHandler = window['buttonHandler']['submit_source'];
    
    sourceSubmissionHandler.DOM.input.source_url.DOM.inputElement.addEventListener("keyup", function(e){
        if(e.keyCode == 13){
            sourceSubmissionHandler.submit();   
        }
    });
};
window.addEventListener("load", theFunction);
