function AddToCart(title) {
    $("#addToCart").prop("disabled", true);
    // sending request to server url addToCart
    // with data title
    $.ajax({
        type: "GET",
        url: `/addToCart/${title}`,
        success: function (response) {
            $("#addToCart").prop("disabled", false);
            if (response.status === "success") {
                showSucessNotification(response.status, response.message).then(r => {
                    window.location.href = "/";
                })
            } else if (response.status === "error") {
                showErrorNotification(response.status, response.message).then(r => {
                })
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            // getting status cod
            let statusCode = xhr.status;
            console.log(statusCode);
            if (statusCode === 401) {
                window.location.href = "/Login" + "?next=" + window.location.pathname;
            }
        }

    })

}

