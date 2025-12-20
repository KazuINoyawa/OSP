from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import (
    user,
    classroom,
    assignment,
    score,
    auth,
    message,
    attachment,
    notification,
    peer_review
)

# Khởi tạo database (SQLite)
Base.metadata.create_all(bind=engine)

# Khởi tạo FastAPI app
app = FastAPI(title="Assignment & Submission System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Khi production nên giới hạn domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(classroom.router)
app.include_router(assignment.router)
app.include_router(score.router)
app.include_router(auth.router)
app.include_router(message.router)
app.include_router(attachment.router)
app.include_router(notification.router)
app.include_router(peer_review.router)

# Root endpoint
@app.get("/")
def root():
    return {"status": "Backend is running"}
