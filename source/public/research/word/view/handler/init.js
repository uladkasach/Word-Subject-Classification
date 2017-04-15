function theFunction(){
    researchHandler.DOM = {
        input : {
            research_word : window["textHandlers"]["research_word"],
        },
        holders : {
            selection : document.getElementById("research_word_selection"),
            link : document.getElementById("research_link_display"),
        },
        display : {
            link : {
                title : document.getElementById("research_link_display_title"),
                link : document.getElementById("research_link_display_link"),
                snippet : document.getElementById("research_link_display_snippet"),
            }
        }
    };
    researchHandler.buttonHandler = window['buttonHandler']['submit_request'];
    
    researchHandler.DOM.input.research_word.DOM.inputElement.addEventListener("keyup", function(e){
        if(e.keyCode == 13){
            researchHandler.submitRequest();   
        }
    });
};
window.addEventListener("load", theFunction);
