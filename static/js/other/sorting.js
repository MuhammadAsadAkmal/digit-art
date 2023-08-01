function sortBy(event) {
//     adding or updating the query string parameter
    var url = new URL(window.location.href);
    url.searchParams.set('sortBy', event.target.value);
    window.location.href = url.href;
}

function changeLimit(event) {
    var url = new URL(window.location.href);
    url.searchParams.set('itemCount', event.target.value);
    window.location.href = url.href;
}


function SearchCategory(cat) {
    var url = new URL(window.location.href);
    url.searchParams.set('category', cat);
    window.location.href = url.href;
}

//on page load complete set the show items to the value in the query string withouth ajax or jquery
window.onload = function () {
    var url = new URL(window.location.href);
    var sortBy = url.searchParams.get('sortBy');
    var itemCount = url.searchParams.get('itemCount');
    if (sortBy != null) {
        let sortBySelect = document.getElementById('sortBy');

    }
    if (itemCount != null) {
        $('#itemCount').val(itemCount);
    }
}