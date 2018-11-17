$(function() {
    $('#btnSignIn').click(function() {
        $.ajax({
            url: '/signIn',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                window.location.replace('userhomepage')
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});