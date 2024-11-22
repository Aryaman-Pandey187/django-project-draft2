function updateTime() {
    const date = new Date();

    // Define options for the date format (e.g., "21 NOV 2024")
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    
    // Get the time string in the format: "HH:MM AM/PM"
    const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });

    // Get the date in the format: "21 NOV 2024"
    const day = date.toLocaleDateString(undefined, options);

    // Update the inner HTML of the element with id "time"
    document.getElementById('time').innerHTML = `${day} <br>${time}`;
}

// Update the time every half minute (30000 milliseconds)
setInterval(updateTime, 30000);

// Call the updateTime function initially
updateTime();

// Function to handle the login form submission and transition to the source form
function submitCredentials() {
    const intranetID = document.getElementById('intranetID').value;
    const password = document.getElementById('password').value;

    // Check if both fields are filled (you can add further validation here if needed)
    if (intranetID && password) {
        // Hide the login form
        document.getElementById('login-section').style.display = 'none';

        // Show the source form
        document.getElementById('sourceForm').style.display = 'block';
    } else {
        alert('Please fill in both fields.');
    }
}

// Function to handle the source form submission
function submitSourceInfo() {
    const sourceDatabase = document.getElementById('sourceDatabase').value;
    const sourceTable = document.getElementById('sourceTable').value;

    // Check if both fields are filled
    if (sourceDatabase && sourceTable) {
        alert(`Source Database: ${sourceDatabase}\nSource Table: ${sourceTable}`);
        // Here you can implement further functionality, such as sending data to the server
    } else {
        alert('Please fill in both fields.');
    }
}
