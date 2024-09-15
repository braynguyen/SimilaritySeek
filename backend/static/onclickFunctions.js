function createTable() {
    const tableName = document.getElementById('table_name').value;
    const schema = document.getElementById('schema').value;

    fetch('http://127.0.0.1:5000/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tableName: tableName, schema: schema }),
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('output').textContent = data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function insertData() {
    const tableName = document.getElementById('table_name_insert').value;
    const columns = document.getElementById('columns').value;
    const data = document.getElementById('data').value;

    fetch('http://127.0.0.1:5000/insert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tableName: tableName, columns: columns, data: data }),
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('output').textContent = data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


function getData() {
    const tableName = document.getElementById('table_name_get').value;

    fetch('http://127.0.0.1:5000/getall', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tableName: tableName }),
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('output').textContent = data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


function getTopN() {
    const tableName = document.getElementById('table_name_get_n').value;
    const id = document.getElementById('id').value;
    const n = document.getElementById('n').value;

    // Validate input values
    if (!tableName || !id || !n) {
        alert('Please fill in all fields.');
        return;
    }

    // Make the API request
    fetch(`http://127.0.0.1:5000/vectorFind/${id}/${n}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tableName: tableName }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the results
        document.getElementById('output').textContent = JSON.stringify(data.results, null, 2);
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while fetching data.');
    });
}