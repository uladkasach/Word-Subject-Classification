
                
                <div class = 'flexme ' style = 'width:100%;'>
                    <div id = 'signin-button' 
                         class = 'flexme unselectable sandButton' 
                         style = 'min-width:175px; max-width:300px; width:100%; height:35px; padding:5px; margin:auto;'>
                        <div style = 'margin:auto;' class = '' id = 'signin-buttonDefaultText'>  Enter </div>
                        <div style = 'margin:auto;' class = 'disnon' id = 'signin-buttonSelectedText'>  Enter </div>
                        <div style = 'margin:auto;' class = 'disnon' id = 'signin-buttonloadingImageHolder'>
                            <div style = 'margin:auto;'>
                                <div class="spinner" style = 'margin-top:7px;'>
                                  <div class="dot1"></div>
                                  <div class="dot2"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <script>
                        signinButton_handler = new global_buttonHandler();
                        signinButton_handler.classes = {default : "sandButton", static : "sandButtonStatic", root : "flexme unselectable"};
                        signinButton_handler.DOM = {
                            main : document.getElementById("signin-button"), 
                            defaultText : document.getElementById("signin-buttonDefaultText"),
                            selectedText : document.getElementById("signin-buttonSelectedText"),
                            loadingImageHolder : document.getElementById("signin-buttonloadingImageHolder"),
                        };
                        signinButton_handler.devmode = false;
                        
                        


                    (function(id){
                        thisButton_handler = new global_buttonHandler();
                        thisButton_handler.classes = {default : "tileButtonText", disabled : "tileButtonText_disabled", root : "flexme unselectable hoverImgChange "};
                        thisButton_handler.DOM = {
                            main : document.getElementById(id+"-button"), 
                            defaultText : document.getElementById(id+"-buttonDefaultText"),
                            selectedText : document.getElementById(id+"-buttonSelectedText"),
                            loadingImageHolder : document.getElementById(id+"-buttonloadingImageHolder"),
                        };
                        thisButton_handler.devmode = false;
                        if(window["buttonHandler"] == undefined){
                            window["buttonHandler"] = {};   
                        }
                        window["buttonHandler"][id] = thisButton_handler;
                    })(theID);
                    </script>
                </div>