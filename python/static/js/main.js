


// the AJAX Request Handling script
function postData(input) {
    console.log('calling lookup ...')
    $.ajax({
        type: "POST",
        url: "/lookup",
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
    