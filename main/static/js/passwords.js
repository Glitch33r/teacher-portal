function get_students(value) {
    $.ajax({
        url: "passwords", // the endpoint
        type: "POST", // http method
        data: {
            type: 'group',
            group: value,
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            $('#students').html(data)
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#error').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}
