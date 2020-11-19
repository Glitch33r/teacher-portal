function submit_contact_form(event) {
    event.preventDefault();

    let name = $("input#name").val();
    let email = $("input#email").val();
    let message = $("textarea#message").val();

    $.ajax({
      url: "contact-us",
      type: "POST",
      data: {
        name: name,
        email: email,
        message: message
      },
      success: function (data) {
        // Success message
          $("#modal").html(data);
          $('#modal').modal('show');
        //clear all fields
        $('#contactForm').trigger("reset");
      },
      error: function (data) {

        //clear all fields
        $('#contactForm').trigger("reset");
      }
    })
}