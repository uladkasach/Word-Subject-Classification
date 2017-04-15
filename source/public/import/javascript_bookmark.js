

var xhr = new XMLHttpRequest();
xhr.open("POST", "http://localhost:1234/0_Input_Channel/import/source.php", true);
xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
xhr.onload = function () {
    console.log(this.responseText);
    var response = this.responseText.split("[[==]]");
    if(response[1] == "SCS"){
        alert("Success!");   
    } else if (response[1] == "ALREADY"){
        alert("Already Processed");   
    } else if (response[1] == "ERR"){
        alert("URL not valid - returns no HTML");   
    }
};
xhr.send('source_url='+window.location.href);