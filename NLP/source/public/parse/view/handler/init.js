function theFunction(){
    parseHandler.DOM = {
        input : {
            amount : window["textHandlers"]["desired_parsed"],
            left : {
                basic : window["textHandlers"]["remaining_unparsed-basic"],
            },
        },
    };
    parseHandler.buttonHandler = {
        basic : window['buttonHandler']['parse-basic'],  
    };
        
    
};
window.addEventListener("load", theFunction);
