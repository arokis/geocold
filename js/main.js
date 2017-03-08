$(document).ready(function() {
    
    initGeoCoLD();
    
    json_list = [
        "http://sws.geonames.org/2867613", 
        "http://d-nb.info/gnd/4021477-1", 
        "http://d-nb.info/gnd/4013255-9", 
        "http://d-nb.info/gnd/7688136-2", 
        "http://d-nb.info/gnd/4324745-3", 
        "http://d-nb.info/gnd/118789708",
        "http://www.fontane-notizbuecher.de/pers.xml#Bossart"];
    json_list2 = ["http://d-nb.info/gnd/4007879-6"];
    //postData('http://d-nb.info/gnd/4021477-1')
    postData(JSON.stringify(json_list));

});

// the AJAX Request Handling script
function postData(input) {
    console.log('calling lookup ...')
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/lookup",
        data: { url: input },
        crossDomain: true,
        success: callbackFunc
    });
}


function callbackFunc(response) {
    console.log('received response from lookup:')
    console.log(response);
    plottResponse(response);
}
    