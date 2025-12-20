from fastapi import FastAPI
from .routers import user, classroom, assignment, score, auth, message, attachment, notification, peer_review
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine

# Tạo bảng database nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
@app.get("/")
def root():
    return {"status": "Backend is running"}
# CORS middleware - for development allow all origins. In production, restrict this.
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(classroom.router)
app.include_router(assignment.router)
app.include_router(score.router)
app.include_router(message.router)
app.include_router(attachment.router)
app.include_router(notification.router)
app.include_router(peer_review.router)
