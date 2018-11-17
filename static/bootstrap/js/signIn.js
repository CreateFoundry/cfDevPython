$(function() {
    $('#btnSignIn').click(function() {
        $.ajax({
            url: '/signIn',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                window.location.replace('getAllCustomers')
            },
            error: function(error) {
                console.log(error);
                alert('Username / password does not match');
            }
        });
    });
});