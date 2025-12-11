from fastapi import FastAPI
from .routers import user, classroom, assignment, score, auth, message, attachment
from .database import Base, engine

# Tạo bảng database nếu chưa có
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(classroom.router)
app.include_router(assignment.router)
app.include_router(score.router)
app.include_router(message.router)
app.include_router(attachment.router)
