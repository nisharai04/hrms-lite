const BASE_URL = "";

/* ======================
   EMPLOYEE FUNCTIONS
====================== */

async function addEmployee() {
    const employee_id = document.getElementById("employee_id").value;
    const full_name = document.getElementById("full_name").value;
    const email = document.getElementById("email").value;
    const department = document.getElementById("department").value;

    const response = await fetch(`${BASE_URL}/employees`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ employee_id, full_name, email, department })
    });

    const data = await response.json();
    const messageDiv = document.getElementById("message");

    if (response.ok) {
        messageDiv.innerHTML = `<div class="message success">${data.message}</div>`;
        loadEmployees();
    } else {
        messageDiv.innerHTML = `<div class="message error">${data.error}</div>`;
    }
}

async function loadEmployees() {
    const response = await fetch(`${BASE_URL}/employees`);
    const employees = await response.json();

    const tableBody = document.querySelector("#employeeTable tbody");
    const emptyState = document.getElementById("emptyState");

    tableBody.innerHTML = "";

    if (employees.length === 0) {
        emptyState.innerText = "No employees found.";
        return;
    }

    emptyState.innerText = "";

    employees.forEach(emp => {
        const row = `
            <tr>
                <td>${emp.employee_id}</td>
                <td>${emp.full_name}</td>
                <td>${emp.email}</td>
                <td>${emp.department}</td>
                <td>
                    <button class="btn-danger" onclick="deleteEmployee(${emp.id})">Delete</button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

async function deleteEmployee(id) {
    await fetch(`${BASE_URL}/employees/${id}`, {
        method: "DELETE"
    });
    loadEmployees();
}

if (document.getElementById("employeeTable")) {
    loadEmployees();
}


/* ======================
   ATTENDANCE FUNCTIONS
====================== */

async function loadEmployeeDropdowns() {
    const response = await fetch(`${BASE_URL}/employees`);
    const employees = await response.json();

    const select1 = document.getElementById("employeeSelect");
    const select2 = document.getElementById("viewEmployeeSelect");

    if (!select1) return;

    select1.innerHTML = "";
    select2.innerHTML = "";

    employees.forEach(emp => {
        select1.innerHTML += `<option value="${emp.id}">${emp.full_name}</option>`;
        select2.innerHTML += `<option value="${emp.id}">${emp.full_name}</option>`;
    });

    loadAttendance();
}

async function markAttendance() {
    const employee_id = document.getElementById("employeeSelect").value;
    const date = document.getElementById("date").value;
    const status = document.getElementById("status").value;

    const response = await fetch(`${BASE_URL}/attendance`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ employee_id, date, status })
    });

    const data = await response.json();
    const messageDiv = document.getElementById("attendanceMessage");

    if (response.ok) {
        messageDiv.innerHTML = `<div class="message success">${data.message}</div>`;
        loadAttendance();
    } else {
        messageDiv.innerHTML = `<div class="message error">${data.error}</div>`;
    }
}

async function loadAttendance() {
    const employee_id = document.getElementById("viewEmployeeSelect").value;
    if (!employee_id) return;

    const response = await fetch(`${BASE_URL}/attendance/${employee_id}`);
    const records = await response.json();

    const tableBody = document.querySelector("#attendanceTable tbody");
    const emptyState = document.getElementById("attendanceEmpty");

    tableBody.innerHTML = "";

    if (records.length === 0) {
        emptyState.innerText = "No attendance records.";
        return;
    }

    emptyState.innerText = "";

    records.forEach(rec => {
        tableBody.innerHTML += `
            <tr>
                <td>${rec.date}</td>
                <td>${rec.status}</td>
            </tr>
        `;
    });
}

if (document.getElementById("employeeSelect")) {
    loadEmployeeDropdowns();
}
