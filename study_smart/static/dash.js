document.addEventListener('DOMContentLoaded', function() {
    /*const clearFormButton = document.getElementById("clearForm");
    
    if (clearFormButton) {
        clearFormButton.addEventListener("click", function () {
            document.querySelectorAll("input, select").forEach(field => {
                if (field.type === "checkbox") {
                    field.checked = false;
                } else {
                    field.value = "";
                }
            });
        });
    } else {
        console.error('Element with ID "clearForm" not found.');
    }
    */

    const checkboxes = document.querySelectorAll('.task-checkbox');
    console.log('Found checkboxes:', checkboxes.length);
    
    // Handle checkbox clicks
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function(e) {
            console.log('Checkbox clicked');
            const taskItem = this.closest('.task-item');
            const taskId = taskItem.dataset.taskId;
            console.log('Task ID:', taskId);
            
            if (this.checked) {
                console.log('Sending complete request');
                fetch(`/complete_task/${taskId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        completed: this.checked
                    })
                })
                .then(response => {
                    console.log('Response received:', response);
                    return response.json();
                })
                .then(data => {
                    console.log('Data:', data);
                    if (data.success) {
                        taskItem.classList.add('completed');
                        console.log('Task marked as completed');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    });

    // Handle delete button clicks
    const deleteButtons = document.querySelectorAll('.delete-btn');
    console.log('Delete buttons found:', deleteButtons.length); // Debugging line

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.dataset.taskId; // Get the task ID from the button
            console.log('Task ID:', taskId); // Debugging line
            if (!taskId) {
                console.error('No task ID found for this button.');
                return; // Exit if no task ID is found
            }

            // Add confirmation dialog
            const confirmDelete = confirm('Are you sure you want to delete this task?');
            if (!confirmDelete) {
                console.log('Deletion canceled by user.');
                return; // Exit if the user cancels the deletion
            }

            console.log('Fetching delete for task ID:', taskId); // Debugging line
            fetch(`/delete_task/${taskId}`, {
                method: 'DELETE', // Use POST as per your route
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}) // Send an empty body if not needed
            }).then(response => {
                if (response.ok) {
                    this.closest('.task-item').remove(); // Remove the task from the DOM
                } else {
                    console.error('Failed to delete task:', response.statusText);
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // Handle refresh button click
    const refreshButton = document.querySelector('.refresh-btn');
    console.log('Refresh button found:', refreshButton); // Debugging line

    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            // Logic to refresh the task list
            location.reload(); // Simple way to refresh the page
        });
    } else {
        console.error('Refresh button not found');
    }
});

function handleCheckboxClick(checkbox) {
    console.log('Checkbox clicked');
    const taskItem = checkbox.closest('.task-item');
    const taskId = taskItem.dataset.taskId;
    
    fetch(`/complete_task/${taskId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            completed: checkbox.checked
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (checkbox.checked) {
                taskItem.classList.add('completed');
            } else {
                taskItem.classList.remove('completed');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}