/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

function deleteEvent(eventId) {
    if (confirm("Are you sure you want to delete this event?")) {
        // Send the AJAX request to delete the event
        $.ajax({
            url: "{% url 'eventapp:event-delete' 0 %}".replace('0', eventId),
            type: "POST",
            dataType: "json",
            data: {
                csrfmiddlewaretoken: "{{ csrf_token }}"
            },
            success: function (response) {
                // Handle the success response
                console.log("Event deleted successfully");
                // Perform any necessary actions after successful deletion
            },
            error: function (xhr, errmsg, err) {
                // Handle the error response
                console.log("Error deleting event");
                // Perform any necessary error handling
            }
        });
    }
}

