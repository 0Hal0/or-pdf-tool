
window.onload = function () {
    var dropdown = document.querySelectorAll('.dropdown');
    dropdown.forEach(element => {
        element.addEventListener('click', function(event) {
            event.stopPropagation();
            element.classList.toggle('is-active');
          });
    })

    var dropdownItems = document.querySelectorAll(".dropdown-item")
    dropdownItems.forEach(element => {
        element.addEventListener("click", function(event){
            event.stopPropagation();
            element.classList.toggle("is-active");
        })
    });

    var sel = document.getElementById("user-selector")
    sel.addEventListener("change", (event) => {
        event.stopPropagation();
        fetch("/users")
    });

};
