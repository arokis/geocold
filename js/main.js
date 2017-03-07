$(document).ready(function() {
    
    initGeoCoLD();
    
    json_list = ["http://d-nb.info/gnd/4007879-6", "http://d-nb.info/gnd/4021477-1", "http://d-nb.info/gnd/4013255-9"];
    json_list2 = ["http://d-nb.info/gnd/4007879-6"];
    //postData('http://d-nb.info/gnd/4021477-1')
    postData(JSON.stringify(json_list));

});
