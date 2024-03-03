
function unfocus_service(event){
    console.log("Unfocus service event")
}

function edit_service(event){
    console.log("Edit service")
}

function delete_service(event){
    parent = event.srcElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    parent.removeChild(event.srcElement.parentElement.parentElement.parentElement.parentElement);
}

function createElementWithClass(type, className) {
    const element = document.createElement(type);
    element.className = className
    return element;
  }

function addService(){
    servicePanel = document.getElementById("service-panel")

    servicePanel.appendChild(createServicePanel())
}

function createServicePanel(uuid=""){
    new_service_div = createElementWithClass("div", "panel-block")

    new_service_edit = createElementWithClass("a","panel-icon")
    new_service_edit.addEventListener("click", edit_service)
    new_service_edit.appendChild(createElementWithClass("i","fas fa-book"))

    new_service_input = Object.assign(createElementWithClass("input", "input"), {"name": "service-uuid", "value": uuid, "type": "text", "placeholder": "Service UUID"})
    new_service_input.addEventListener("focusout", unfocus_service)
    new_service_input_div = createElementWithClass("div", "control")
    new_service_input_div.appendChild(new_service_input)

    new_service_delete = createElementWithClass("a", "level-right")
    new_service_delete.addEventListener("click", delete_service)
    new_service_delete.appendChild(createElementWithClass("i", "fas fa-trash"))
    new_service_delete_div = createElementWithClass("div","container")
    new_service_delete_div.appendChild(new_service_delete)

    new_service_div.appendChild(new_service_edit)
    new_service_div.appendChild(new_service_input_div)
    new_service_div.appendChild(new_service_delete_div)

    return new_service_div
}

function save(){
    services = document.getElementsByName("service-uuid")
    user = user_dropdown = document.getElementById("user-selector").value
    var serviceIds = [];
    services.forEach(service =>{
        serviceIds.push(service.value)
    })

    fetch(`/services/${user}/add`, {
        method: "POST",
        body: JSON.stringify({
            "services": serviceIds
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    })
}

async function update_services(user){
    try {
        response = await fetch(`/services/${user}`)
    } catch (error) {
        return
    }

    services = await response.json()

    service_panel = document.getElementById("service-panel")
    panel_heading = service_panel.getElementsByClassName("panel-heading")[0]
    service_panel.innerHTML = ""
    service_panel.appendChild(panel_heading)

    services.forEach(service =>{
        service_panel.appendChild(createServicePanel(service))
    })
}

async function request_report(){
    user = document.getElementById("user-selector").value
    highlight_changed = document.getElementById("highlight-changed").checked
    save_history = document.getElementById("save-history").checked
    only_changes = document.getElementById("only-changes").checked

    try {
        response = await fetch(`/report/${user}?highlight_changed=${highlight_changed}&save_history=${save_history}&only_changes=${only_changes}`)
        .then(res => res.blob())
        .then(blob => {
            var file = window.URL.createObjectURL(blob);
            window.open(file)
        })
    } catch (error) {
        console.log(error)
        return
    }

}

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
    update_services(sel.value)
    sel.addEventListener("change", async (event) => {

        user_dropdown = document.getElementById("user-selector")

        await update_services(user_dropdown.value)

    });

    


};
