let group_id = '';
let stud_id = '';
let subj_id = 0;
let selected = [];

function get_subject(id) {
    subj_id = id;
}

function get_students_of_group(id) {
    group_id = id;
    $.ajax({
        url: "comments", // the endpoint
        type: "POST", // http method
        data: {
            type: 'group',
            group: id,
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            $('select#selectStudent').html(data)
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function get_subjects_and_comments(id) {
    stud_id = id
    $.ajax({
        url: "comments", // the endpoint
        type: "POST", // http method
        data: {
            type: 'student',
            student: id,
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            $('select#selectSubject').html(data)
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function set_selected() {
    selected = []
    $('#checkboxes input:checked').each(function () {
        selected.push($(this).attr('value'));
    });
}

function generate_comment(event) {
    event.preventDefault();
    set_selected();

    // if ARRAY is empty

    $.ajax({
        url: "comments", // the endpoint
        type: "POST", // http method
        data: {
            type: 'generate',
            criteria: selected.join(','),
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            $("#commentText").val(data);
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $("#modal").html(xhr.responseText);
            $('#modal').modal('show');
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function send_comment(event) {
    event.preventDefault();


    $.ajax({
        url: "comments", // the endpoint
        type: "POST", // http method
        data: {
            type: 'send',
            group: group_id,
            student: stud_id,
            subject: subj_id,
            comment: $("#commentText").val(),
        }, // data sent with the post request

        // handle a successful response
        success: function (data) {
            $("#modal").html(data);
            $('#modal').modal('show');
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {

            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function toggle_checkbox(box, toggle) {
    if (box.checked) {
        $("input#" + toggle).attr("disabled", true);
    } else {
        $("input#" + toggle).removeAttr("disabled");
    }
}