async function loadAssignments() {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_BASE}/assignment`, {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();
    console.log(data);
}
