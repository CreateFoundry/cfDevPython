$(function() {
    $('#btnSignUp').click(function() {
        $.ajax({
            url: '/signUpUser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                window.location.replace('homepage')
            },
            error: function(error) {
                console.log(error);
                alert('Sorry Username already exists');
            }
        });
    });
});