function theFunction(){
    parseHandler.DOM = {
        input : {
            amount : window["textHandlers"]["desired_parsed"],
            left : {
                basic : window["textHandlers"]["remaining_unparsed-basic"],
                stop : window["textHandlers"]["remaining_unparsed-stop"],
            },
        },
    };
    parseHandler.buttonHandler = {
        basic : window['buttonHandler']['parse-basic'],
        stop : window['buttonHandler']['parse-stop'],  
    };
        
    
};
window.addEventListener("load", theFunction);
