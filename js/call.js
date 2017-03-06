$(document).ready(function() {
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
    }

    json_list = ["http://d-nb.info/gnd/4007879-6", "http://d-nb.info/gnd/4021477-1", "http://d-nb.info/gnd/4013255-9"]
    json_list2 = ["http://d-nb.info/gnd/4007879-6"]
    //postData('http://d-nb.info/gnd/4021477-1')
    postData(JSON.stringify(json_list))
})
      