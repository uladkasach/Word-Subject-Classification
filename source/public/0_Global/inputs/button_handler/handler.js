/////////////////////////////////////////
// V2.0 - 6/13/2016
/*
    2.0.1 - 6/13/2016 - disable href as well as onclick
*/
/////////////////////////////////////////
function global_buttonHandler (){
    
    ////////////////////
    // Constants defined externally
    ////////////////////
    this.classes = {default : null, static : null, disabled: null, root : null,};
    this.DOM = {
            main : null,
            defaultText : null,
            selectedText : null,
            disabledText : null,
            loadingImageHolder : null,
          };
    this.devmode = false;
    
    ////////////////////
    // Constants defined durring runtime
    ////////////////////
    this.onclickFunction = null;
    this.hrefValue = null;
    this.timeLoadingStarted = null; //used to disable/show-loading-on button for atleast .5 seconds
    this.timeoutFunction = null;
    this.loadingTimeMinimum = 0.5 * 1000;

};
        
        
global_buttonHandler.prototype = {
    ///////////////
    // Setter function
    //
    set onclick (theFunction) {
        this.DOM.main.onclick = function(){ this.displayLoading(); theFunction(); }.bind(this);
    },
    
    
    
    setHREFTo : function(thePath){
       this.hrefValue = thePath;
    },

    displaySelected : function(){
        this.timeLoadingStarted = null; 
        this.DOM.main.className = this.classes.root + " " + this.classes.static;
        //console.log(this.DOM.main.className);
        this.hideAllDisplays();
        if(this.DOM.selectedText !== null){
            this.DOM.selectedText.className = '';
        }
        if(this.devmode !== true){
            this.removeAction();
        }
    },
    displayLoading : function(){
        this.timeLoadingStarted = Date.now();
        this.DOM.main.className = this.classes.root + " " + this.classes.static;
        this.hideAllDisplays();
        this.DOM.loadingImageHolder.className = '';
        if(this.devmode !== true){
            this.removeAction();
        }
    },
    displayDisabled : function(){
        this.timeLoadingStarted = null; 
        this.DOM.main.className = this.classes.root + " " + this.classes.disabled;
        //console.log(this.DOM.main.className);
        
        
        this.hideAllDisplays();
        if(this.DOM.disabledText != null){
            this.DOM.disabledText.className = "";   
        } else {
            this.DOM.defaultText.className = "";   
        }
        
        
        if(this.devmode !== true){
            this.removeAction();
        }
    },
    
    
    hideAllDisplays : function(){
        if(this.DOM.selectedText !== null){
            this.DOM.selectedText.className = 'disnon';
        }
        if(this.DOM.disabledText != null){
            this.DOM.disabledText.className = 'disnon';
        }
        if(this.DOM.loadingImageHolder !== null){
            this.DOM.loadingImageHolder.className = 'disnon';
        }
        this.DOM.defaultText.className = 'disnon';
    },
    
    
    displayDefault : function(){
        if(this.timeLoadingStarted !== null){
            ////////////////////////////////////////////
            // Make sure loading screen is atleast the defined minimum
            ////////////////////////////////////////////
            if(this.timeoutFunction !== undefined){
                clearTimeout(this.timeoutFunction);   
            } 
            var timeSince = (Date.now() - this.timeLoadingStarted);
            if(timeSince < this.loadingTimeMinimum){
                setTimeout(function(){
                    this.displayDefault()   
                }.bind(this), this.loadingTimeMinimum - timeSince);
                return;
            }
            console.log(timeSince);
            ////////////////////////////////////////////
        }
        /*
            console.log("--");
            console.log(this.DOM.main.onclick);
            console.log("--");
        */
        this.DOM.main.className = this.classes.root + " " + this.classes.default;
        this.hideAllDisplays();
        this.DOM.defaultText.className = '';
        if(this.devmode !== true){
            this.restoreAction();
        }
    },
    removeAction : function(){
          this.removeHref();
          this.removeOnclick();
    },
    restoreAction: function(){
          this.restoreHref();
          this.restoreOnclick();
    },
    removeHref : function(){
        //console.log("here i am");
        if(this.DOM.main.href == null){
            //console.log("nothing to remove href");
            return;
        }
        //console.log("removing");
        //console.log(this.DOM.main.href);
        this.hrefValue = this.DOM.main.href;
        this.DOM.main.href = "javascript: void(0);";
        //console.log(this.DOM.main.href);
    },
    restoreHref : function(){
        if(this.hrefValue == null){
            return;
        }
        this.DOM.main.href = this.hrefValue;
    },
    removeOnclick : function(){
        if(this.DOM.main.onclick == null){
            //console.log("nothing to remove");
            return;
        }
        //console.log("removing");
        this.onclickFunction = this.DOM.main.onclick;
        this.DOM.main.onclick = null;
        //console.log(this.DOM.main.onclick);
    },
    restoreOnclick : function(){
        if(this.onclickFunction == null){
            return;
        }
        this.DOM.main.onclick = this.onclickFunction;
    },

};