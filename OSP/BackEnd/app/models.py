
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from .database import Base

class Attachment(Base):
	__tablename__ = "attachments"
	id = Column(Integer, primary_key=True, index=True)
	filename = Column(String, nullable=False)
	file_url = Column(String, nullable=False)
	uploaded_by = Column(Integer, ForeignKey("users.id"))
	assignment_id = Column(Integer, ForeignKey("assignments.id"))
	is_submission = Column(Integer, default=0)  # 0: tài liệu, 1: bài nộp

class Message(Base):
	__tablename__ = "messages"
	id = Column(Integer, primary_key=True, index=True)
	sender_id = Column(Integer, ForeignKey("users.id"))
	receiver_id = Column(Integer, ForeignKey("users.id"))
	content = Column(Text, nullable=False)
	timestamp = Column(DateTime)

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True, nullable=False)
	hashed_password = Column(String, nullable=False)
	full_name = Column(String)
	role = Column(String, default="student")  # student, teacher, admin
	classes = relationship("Class", secondary="user_classes", back_populates="users")

class Class(Base):
	__tablename__ = "classes"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False)
	description = Column(Text)
	users = relationship("User", secondary="user_classes", back_populates="classes")
	assignments = relationship("Assignment", back_populates="classroom")

class UserClass(Base):
	__tablename__ = "user_classes"
	user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
	class_id = Column(Integer, ForeignKey("classes.id"), primary_key=True)

class Assignment(Base):
	__tablename__ = "assignments"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, nullable=False)
	description = Column(Text)
	due_date = Column(DateTime)
	class_id = Column(Integer, ForeignKey("classes.id"))
	classroom = relationship("Class", back_populates="assignments")
	scores = relationship("Score", back_populates="assignment")

class Score(Base):
	__tablename__ = "scores"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	assignment_id = Column(Integer, ForeignKey("assignments.id"))
	score = Column(Float)
	assignment = relationship("Assignment", back_populates="scores")
