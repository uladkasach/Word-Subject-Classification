var global_textHandler_enforceHandler = {
    
    alpha_only : function(textHandler){
        var value = textHandler.value;
        ///////////////////////////
        var enforcedValue = value.replace(/[^a-zA-Z]+/,'');
        //console.log(enforcedValue);
        
        ///////////////////////////
        if(value == enforcedValue){
            return true;   
        }
        return enforcedValue;
    },
    alpha_only_blur : function(){ return true; },
    
    no_space : function(textHandler){
        var value = textHandler.value;
        ///////////////////////////
        
        var enforcedValue = value.replace(/ /g,'');
        
        ///////////////////////////
        if(value == enforcedValue){
            return true;   
        }
        return enforcedValue;
    },
    no_space_blur : function(){ return true; },
    
    digits_only : function(textHandler){
        var value = textHandler.value;
        ///////////////////////////
        
        var enforcedValue = value.replace(/\D+/g, '');
        
        ///////////////////////////
        if(value == enforcedValue){
            return true;   
        }
        return enforcedValue;
    },  
    digits_only_blur : function() {return true},
    
    price : function(textHandler){
        var value = textHandler.value;
        var origValue = value;
        ///////////////////////////
        if(value == ""){
            return true;
        }
        value = value.replace(/([^0-9\.])+/g,'');
        var datas = value.split(".");
        
        var valueA = datas[0];
        var valueB = "";
        var total = datas.length;
        for(var index = 1; index < total; index++){
            valueB += datas[index];
        }
        valueB = valueB.substr(0,2);
        value = valueA;
        if(datas.length > 1){
            value += "." + valueB;   
        }
        
        var enforcedValue = value;
        value = origValue;    
        ///////////////////////////
        if(value == enforcedValue){
            return true;   
        }
        return enforcedValue;
    },
    price_blur : function(textHandler){
        var value = textHandler.value;
        ///////////////////////////
        
        price = value+"";
        price = price.replace(/^0+/, '');
        price = price.split(".");
        if(price[0] == "") price[0] = "0";
        if(price[1] == undefined) price[1] = "00";   
        while(price[1].length < 2) price[1] += "0";  
        price = price.join(".");
        
        var enforcedValue = price;
        ///////////////////////////
        if(value == enforcedValue){
            return true;   
        }
        return enforcedValue;
    },
}