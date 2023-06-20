// Get the button element
const to_delete = document.getElementById('item_delete');

// Attach a click event listener to the button
to_delete.addEventListener('click', function() {
// Get all the checkboxes
const checkboxes = document.querySelectorAll('input[type="checkbox"]');

const trash = [];

var listname = "";

checkboxes.forEach(function(checkbox) {
    if (checkbox.checked) {
        trash.push(checkbox.value); // Add the value to the selectedValues array
        let element = document.getElementById(`item${checkbox.value}`); //get box and label 
        element.classList.add("deleted");

        listname = element.getAttribute("name");

        // while (element.firstChild) {
        // element.removeChild(element.firstChild);
        // }
    }
});

if(trash.length > 0){
    trash.push(listname);  //list name is last element of trash array
    fetch('/deleteitems', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(trash)
    })
}
});