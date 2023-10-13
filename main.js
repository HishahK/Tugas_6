$(document).ready(function(){
    function loadItems() {
        $.ajax({
            url: '/get-items/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#items').empty();
                data.items.forEach(item => {
                    $('#items').append('<div class="card"><h5>' + item.name + '</h5><p>Amount: ' + item.amount + '</p></div>');
                });
            },
            error: function() {
                alert('Error loading items.');
            }
        });
    }

    loadItems();

    $('#myForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/create-ajax/',
            type: 'POST',
            data: $('#myForm').serialize(),
            success: function(data) {
                if(data.status === 'ok'){
                    $('#myModal').modal('hide');
                    $('#myForm')[0].reset();
                    loadItems();
                } else {
                    alert('Error: ' + data.error);
                }
            },
            error: function() {
                alert('Error adding item.');
            }
        });
    });
});
