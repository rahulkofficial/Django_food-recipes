$(document).ready(()=>{
        var token=$("input.message_status").val()
        var tk=$("input.token").val()
        var id=$("input.rec_up").val()
        var url="http://127.0.0.1:8000/api/v1/recipes/update/"+id
        $("#delete_button").on("click",(e)=>{
            
            if(confirm("Are you sure to delete this recipe?")){
                Swal.fire({
                    title: 'Success',
                    text: 'Successfully deleted recipe',
                    icon: 'success',
                  })
            }
            else{
                e.preventDefault();
            }
        })
        $("#recipeForm").submit(function (e) {
            e.preventDefault();

            var formData = new FormData(this);

            $.ajax({
                url: "http://127.0.0.1:8000/api/v1/recipes/add", 
                type: "POST",
                headers: {
                    "Authorization": token, 
                },
                data: formData,
                contentType: false,
                processData: false,
                success: function (response) {
                    Swal.fire({
                        title: 'Success',
                        text: 'Successfully added recipe',
                        icon: 'success',
                      }).then((result)=>{
                        window.location.href="http://127.0.0.1:8000/recipes"

                    });
                },
                error: function (xhr, status, error) {
                    console.log(error)
                    Swal.fire({
                        title: 'Error',
                        text: 'Somthing went wrong',
                        icon: 'error',
                      })
                }
            });
        });

        $("form.update").submit(function (e) {
            e.preventDefault();
            var formData = new FormData(this);

            $.ajax({
                url: url,
                type: "POST",
                headers: {
                    "Authorization": tk,
                },
                data: formData,
                contentType: false,
                processData: false,
                success: function (response) {
                    Swal.fire({
                        title: 'Success',
                        text: 'Successfully updated recipe',
                        icon: 'success',
                      }).then((result)=>{
                        window.location.href="http://127.0.0.1:8000/recipes_detailed/"+id
                    });
                },
                error: function (xhr, status, error) {
                    Swal.fire({
                        title: 'Error',
                        text: 'Somthing went wrong',
                        icon: 'error',
                      })
                }
            });
        });


   })