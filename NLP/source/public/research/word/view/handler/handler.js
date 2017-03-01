var researchHandler = {
    buttonHandler : null,
    DOM : {
        input : {},
    },
    
    // Index of list through
    index : 0, 
    page_index : 0,
    
    // Links to list through
    links_to_list_through : {},
    
    
    /*
    
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
    };
    */
    
    
    changeDisplayTo : function(type, data){
        if(type == "link"){
            this.DOM.holders.selection.className = "disnon";
            this.DOM.holders.link.className = "";
            this.DOM.display.link.title.textContent = data.title;
            this.DOM.display.link.link.textContent = data.link;
            this.DOM.display.link.link.href = data.link;
            this.DOM.display.link.snippet.textContent = data.snippet;
        } else {
            this.DOM.holders.selection.className = "";
            this.DOM.holders.link.className = "disnon";
            this.DOM.input.research_word.value = "";
        }
    },
    
    importTheLink : function(boolean_import){
        if(boolean_import){
            the_url = this.links_to_list_through[this.index]["link"];

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "http://localhost:1234/0_Input_Channel/import/source.php", true);
            xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                console.log(this.responseText);
                var response = this.responseText.split("[[==]]");
                if(response[1] == "SCS"){   
                    console.log("scs");
                    window["researchHandler"].list_next_link();
                } else if (response[1] == "ALREADY"){
                    console.log("Already Processed");   
                    window["researchHandler"].list_next_link();
                } else if (response[1] == "ERR"){
                    alert("URL not valid - returns no HTML");   
                }
            };
            xhr.send('source_url='+the_url+'&return_content=true');
        } else {
            this.list_next_link();
        }
    },
    
                                //this_link.title, this_link.link, this_link.snippet
                                
    list_next_link : function(){
        this.index++;
        if(this.index > this.links_to_list_through.length - 1){
            result = confirm("All 10 results have been parsed. Parse next page?");
            if(result){
                this.page_index += 1;
                this.submitRequest();
            } else {
                this.page_index = 0;   
                this.changeDisplayTo("basic");
            }
            return;
        }
        console.log('listing link ' + this.index);
        //console.log(this.links_to_list_through[this.index])
        var this_link = this.links_to_list_through[this.index];
        this.changeDisplayTo("link", this_link);
    },
    
    
    
    
    loadAndStartLinkListing: function(data){
        this.links_to_list_through = data;
        this.index = -1;
        this.list_next_link();
    },
    
    callbackForSuccess : function(){
       this.callbackForFinalSuccess();  
    },
    
    callbackForFinalSuccess : function(){
        alert("Success!");
    },
    
    submitRequest : function(){
        validationReport = this.returnValidationReport();
        
        var research_word = encodeURIComponent(this.DOM.input.research_word.value);
        this.buttonHandler.displayLoading();
        
        
        
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/0_Input_Channel/research/word.php", true);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhr.onload = function () {
            //console.log(this.responseText);
            var response = this.responseText.split("[[=!!!!!!!!!!!!!=]]");
            if(response[1] == "SCS"){
                console.log("Success!");
                var data = JSON.parse(response[3]);
                window["researchHandler"].loadAndStartLinkListing(data);
                
                //console.log(data);   
            } else{
                console.log(this.responseText);
                alert("Something went wrong!");   
            }
            window["researchHandler"].buttonHandler.displayDefault();   
        };
        xhr.send('research_word='+research_word+"&page_index="+this.page_index);
    },
    
    returnValidationReport : function(){
        var string = "";

        var research_word = this.DOM.input.research_word.value;

        if(research_word.replace(/ /g,'') == ""){
            string += " - Source URL is empty\n";   
        }
        
        if(string !== ""){
            string = "Please fix the following errors before submitting : \n" + string; 
            return string  
        } else {
            return true;   
        }
    },
    
}