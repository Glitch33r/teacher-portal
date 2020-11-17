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
            $('div#main-part').html(data)
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('div#error').html("<div class=\"alert alert-danger alert-dismissible fade show\" role=\"alert\">" +
                "<strong id=\"error\">"+JSON.parse(xhr.responseText)['error']+ "</strong>" +
                "            <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\">" +
                "                <span aria-hidden=\"true\">&times;</span>" +
                "            </button>" +
                "        </div>"); // add the error to the dom
        }
    });
}