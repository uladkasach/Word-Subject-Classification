var global_textInputExtension_newLineTemplate = {
    ///////////////////////////
    // Replication function
    ///////////////////////////
    new : function(){
        return Object.create(this);   
    },
    ///////////////////////////
    ///////////////////////////
    
    lineTemplateElementID : "text_input_js_extend_template1",
    returnNode : function(newID){
        var html = document.getElementById(this.lineTemplateElementID).innerHTML;
        html = html.replace(new RegExp("IDHOLDERSTR", "g"), newID);
        
        var div = document.createElement('div');
        div.innerHTML = html;
        div.id = newID + "_" + "newLineHolder";
        
        return div;
    },
    
}