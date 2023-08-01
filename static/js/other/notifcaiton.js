function showSucessNotification(title, message) {
    let notification = document.getElementById("notification")
    // removing error class
    notification.classList.remove("error")
    // adding success class
    notification.classList.add("success")
    // setting title
    let titleElement = document.getElementById("notiTitle");
    titleElement.innerHTML = title;
    let messageElement = document.getElementById("notiMessage");
    messageElement.innerHTML = message;
    // showing notification
    notification.style.visibility = "visible";
    //     returing promise after 3 seconds
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            notification.style.visibility = "hidden";
            resolve("done")
        }, 3000);
    })

}

function showErrorNotification(title, Message) {
    let notification = document.getElementById("notification")
    // removing error class
    notification.classList.remove("success")
    // adding success class
    notification.classList.add("error")
    // setting title
    let titleElement = document.getElementById("notiTitle");
    titleElement.innerHTML = title;
    let messageElement = document.getElementById("notiMessage");
    messageElement.innerHTML = Message;
    // showing notification
    notification.style.visibility = "visible";
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            notification.style.visibility = "hidden";
            resolve("done")
        }, 3000);
    })

}

function searchdata() {
    let search = $("#search").val();
    let dropdown = $("#dropdown").val();
    if (search === "") {
        return;
    }
//     changing search argument to lowercase
    if (window.location.href.includes("store")) {
        search = search.toLowerCase();
        var url = new URL(window.location.href);
        url.searchParams.set('search', search);
        url.searchParams.set('category', dropdown);
        window.location.href = url.href;
    } else {
        let location = "/store?search=" + search + "&category=" + dropdown;
        window.location.href = location;
    }

}