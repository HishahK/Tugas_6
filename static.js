$(document).ready(function(){
    
    
    function loadItems() {
        $.ajax({
            url: '/get-items/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#items').empty(); // Mengosongkan konten #items agar tidak ada duplikasi
                data.items.forEach(item => {
                    $('#items').append(`
                        <div class="card">
                            <h5>${item.name}</h5>
                            <p>Amount: ${item.amount}</p>
                        </div>
                    `);
                });
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
                    $('#myModal').modal('hide'); // Menutup modal
                    $('#myForm')[0].reset(); // Membersihkan form
                    loadItems(); // Memuat ulang item-item agar yang baru muncul
                }
            },
            error: function() {
                alert('Error: Tidak dapat menambahkan item.');
            }
        });
    });
});
