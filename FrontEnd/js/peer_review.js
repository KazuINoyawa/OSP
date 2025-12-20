async function submitPeerReview(assignmentId, score, comment) {
    const token = localStorage.getItem("token");

    await fetch(`${API_BASE}/peer-review`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            assignment_id: assignmentId,
            score: score,
            comment: comment
        })
    });

    alert("Đã gửi đánh giá");
}
