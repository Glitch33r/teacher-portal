function logbook_login(url) {
    $.ajax({
        url: url, // the endpoint
        type: "POST", // http method
        data: {
            type: 'login',
            login: $('#login').val(),
            password: $('#password').val(),
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            $('.col-sm-4').html(data)
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#error').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}