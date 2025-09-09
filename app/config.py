import os

class Config:
    # Secret key for session cookies and CSRF protection
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:1020@localhost/jobapp"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings for resumes
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        os.path.join(os.getcwd(), "uploads", "resumes")
    )
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload size
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
    
    # Flask-Login configuration
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7  # 7 days
    
    # Pagination defaults
    JOBS_PER_PAGE = int(os.getenv("JOBS_PER_PAGE", 20))
    
    # Email/SMS notifications (example placeholders)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    
    # Environment flag
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
