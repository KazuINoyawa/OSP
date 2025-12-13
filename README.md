# OSP - Online School Platform

A full-stack learning management system (LMS) with teacher and student dashboards, built with FastAPI (backend) and vanilla HTML/CSS/JS (frontend).

## Features Implemented

### A. Mark-Per-Item Notifications & Messages
- Frontend dropdowns for Messages and Notifications with unread badges
- Mark individual items as read with per-item API calls
- Real-time badge updates in UI

### B. API Endpoints with Authentication
- Message and Notification read-state management
- Score creation and updates with feedback persistence
- Token-based Bearer authentication on write endpoints
- CORS enabled for frontend-backend communication

### C. CORS, Feedback Persistence, and Token Auth
- Global CORS middleware enabled for cross-origin requests
- Score feedback field stored and retrieved from database
- Simple token-based authorization (default token: `dev-token`)
- Environment variable `API_TOKEN` to configure custom tokens

## Project Structure

```
OSP/
├── BackEnd/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py          # SQLite database configuration
│   │   ├── main.py              # FastAPI app with CORS setup
│   │   ├── models.py            # SQLAlchemy models (User, Message, Notification, Score, etc.)
│   │   ├── deps.py              # Bearer token dependency
│   │   └── routers/             # API endpoints
│   │       ├── user.py
│   │       ├── classroom.py
│   │       ├── assignment.py
│   │       ├── score.py         # Score CRUD with feedback
│   │       ├── message.py       # Message mark-read endpoint
│   │       ├── notification.py  # Notification CRUD and mark-read
│   │       ├── auth.py
│   │       └── attachment.py
│   ├── requirements.txt         # Python dependencies
│   ├── venv/                    # Virtual environment
│   └── osp.db                   # SQLite database (auto-created)
│
└── FrontEnd/
    ├── dashboardGV.html         # Teacher dashboard with dropdowns
    ├── dashboardSV.html         # Student dashboard with dropdowns
    ├── Quanlybaitap.html        # Assignment management with grading modal
    ├── dashboardGV.css
    ├── student_style.css
    └── [other HTML files]
```

## Setup & Running

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd BackEnd
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set environment variables (optional):**
   ```bash
   export API_TOKEN="your-secure-token"
   ```
   Default token is `dev-token` if not set.

3. **Start the backend server:**
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   The backend will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Start the frontend server:**
   ```bash
   cd FrontEnd
   python3 -m http.server 8080
   ```
   
   The frontend will be available at `http://localhost:8080`

2. **Access the application:**
   - Login: `http://localhost8080/login.html`
   - Teacher Dashboard: `http://localhost:8080/dashboardGV.html`
   - Student Dashboard: `http://localhost:8080/dashboardSV.html`
   - Assignment Management: `http://localhost:8080/Quanlybaitap.html`

## API Configuration

The frontend automatically configures API connections:

```javascript
// In all HTML files with API calls
window.API_BASE = 'http://localhost:8000'     // Backend URL
window.API_TOKEN = 'dev-token'                // Bearer token
```

These values can be overridden by setting them in the browser console before page load, or by modifying the script tags in the HTML files.

## Key Endpoints

### Messages
- `GET /messages` - List messages
- `POST /messages/{id}/mark-read` - Mark message as read

### Notifications
- `GET /notifications` - List notifications
- `POST /notifications/{id}/mark-read` - Mark notification as read
- `POST /notifications/mark-read-bulk` - Mark multiple as read

### Scores (with Authentication)
- `GET /scores` - List scores
- `POST /scores` - Create score (requires token)
- `PUT /scores/{id}` - Update score (requires token)
- `GET /scores/{id}` - Get score details

### Required Headers for Write Requests
```
Authorization: Bearer dev-token
Content-Type: application/json
```

## Database

- **Type:** SQLite (development)
- **Location:** `BackEnd/osp.db`
- **Migrations:** Currently using SQLAlchemy `create_all()` for schema creation

To reset the database, simply delete `BackEnd/osp.db` and restart the server.

## Frontend Features

### Teacher Dashboard (`dashboardGV.html`)
- Message dropdown with unread badge
- Notification dropdown with unread badge
- Avatar menu
- Mark messages/notifications as read per-item

### Assignment Management (`Quanlybaitap.html`)
- View student submissions
- Grade assignments with feedback
- Confirm and save score via API
- Success notification after saving
- Tailwind CSS styling

## Authentication

Write endpoints (POST, PUT) require Bearer token in `Authorization` header:

```javascript
const API_TOKEN = window.API_TOKEN || 'dev-token';

fetch(`${API_BASE}/scores`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_TOKEN}`
  },
  body: JSON.stringify({ user_id, assignment_id, score, feedback })
});
```

## Development Notes

- **CORS:** Currently set to allow all origins (`allow_origins="*"`)
- **Token Check:** Simple Bearer token validation in `BackEnd/app/deps.py`
- **Database:** SQLite with no migrations tool (use Alembic for production)
- **Frontend:** Vanilla HTML/CSS/JS with no build system required

## Future Improvements

1. Add database migrations with Alembic
2. Implement JWT tokens with expiration
3. Add role-based access control (RBAC)
4. Integrate with OAuth2 authentication
5. Add unit and integration tests
6. Deploy to production ( Vercel )

---

**Version:** 1.0.1 
**Last Updated:** December 13, 2025
