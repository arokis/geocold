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
      