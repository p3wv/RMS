// Function to handle form submission and add a new address
function handleFormSubmit(event) {
    event.preventDefault();
    const addressInput = document.getElementById('address');
    const address = addressInput.value;
  
    // Send the address to the backend API endpoint
    fetch('/api/user_input', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ address })
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.message); // Handle the response as needed
  
        // Clear the input field
        addressInput.value = '';
  
        // Add the new address row dynamically
        const tbody = document.querySelector('#address-table tbody');
        const newRow = generateAddressRow(address);
        tbody.appendChild(newRow);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  
  // Function to generate a row for an address
  function generateAddressRow(address) {
    const row = document.createElement('tr');
  
    const addressCell = document.createElement('td');
    addressCell.textContent = address;
  
    const actionsCell = document.createElement('td');
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', () => {
      // Perform the necessary logic to delete the address using the backend code
      row.remove(); // Remove the row from the table
    });
    actionsCell.appendChild(deleteButton);
  
    row.appendChild(addressCell);
    row.appendChild(actionsCell);
  
    return row;
  }
  
  // Initial setup when the page loads
  document.addEventListener('DOMContentLoaded', async () => {
    const addForm = document.getElementById('add-form');
    addForm.addEventListener('submit', handleFormSubmit);
  });
  