let assignmentsList = [];

const DEFAULT_ASSIGNMENTS = [
    {
        id: 'web',
        type: 'pending',
        title: "Xây dựng Website bán hàng",
        course: "Lập trình Web",
        deadline: "Hôm nay",
        submitted: false,
        desc: "Thiết kế frontend"
    }
];

// Load
function loadAssignments() {
    const data = localStorage.getItem('assignments');
    assignmentsList = data ? JSON.parse(data) : DEFAULT_ASSIGNMENTS;
    saveAssignments();
}

function saveAssignments() {
    localStorage.setItem('assignments', JSON.stringify(assignmentsList));
}

function openDetail(id) {
    const a = assignmentsList.find(x => x.id === id);
    if (!a) return;

    document.getElementById('detail-title').innerText = a.title;
    document.getElementById('detail-course').innerText = a.course;
    document.getElementById('detail-deadline').innerText = a.deadline;
    document.getElementById('detail-desc').innerText = a.desc;

    switchView('view-detail');
}

function switchView(viewId) {
    document.querySelectorAll('.view-section').forEach(v => {
        v.classList.add('hidden');
    });
    document.getElementById(viewId).classList.remove('hidden');
}

document.addEventListener('DOMContentLoaded', loadAssignments);
