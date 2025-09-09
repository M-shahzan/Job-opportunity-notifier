from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())

    seeker_preference = db.relationship("SeekerPreference", backref="user", uselist=False)

class SeekerPreference(db.Model):
    __tablename__ = "seeker_preferences"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    skills = db.Column(db.Text)
    location = db.Column(db.String(255))
    job_type = db.Column(db.String(50))
    experience_level = db.Column(db.String(50))

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    skills_required = db.Column(db.Text)
    job_type = db.Column(db.String(50))
    experience_level = db.Column(db.String(50))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

class Application(db.Model):
    __tablename__ = "applications"
    
    id = db.Column(db.Integer, primary_key=True)
    seeker_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    resume_filename = db.Column(db.String(255))  # Store the uploaded file name
    cover_letter = db.Column(db.Text)  # Optional cover letter
    expected_salary = db.Column(db.String(100))
    status = db.Column(db.String(50), default="pending")
    applied_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    
    # Relationships
    seeker = db.relationship("User", backref="applications")
    job = db.relationship("Job", backref="applications")


