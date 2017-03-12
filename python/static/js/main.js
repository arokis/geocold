
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
    console.log('AJAX received response from lookup:')
    //console.log(response);
    plottResponse(response);
}
