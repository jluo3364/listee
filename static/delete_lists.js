// Get the button element
const to_delete = document.getElementById('to_delete');

// Attach a click event listener to the button
to_delete.addEventListener('click', function() {
// Get all the checkboxes
const checkboxes = document.querySelectorAll('input[type="checkbox"]');

const trash = [];

checkboxes.forEach(function(checkbox) {
    if (checkbox.checked) {
        trash.push(checkbox.value); // Add the value to the selectedValues array
        let element = document.getElementById(`${checkbox.value}`);
        while (element.firstChild) {
        element.removeChild(element.firstChild);
        }
    }
});

// Send an HTTP request to the server with the selected values
fetch('/deletelists', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json'
    },
    body: JSON.stringify(trash)
})
});