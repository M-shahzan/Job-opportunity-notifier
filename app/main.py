# app/backend/models.py - Pydantic Models
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    REMOTE = "remote"

class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    ALL = "all"

# Job Models
class JobBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10)
    location: str
    remote_allowed: bool = False
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: str = "USD"
    job_type: JobType
    experience_level: ExperienceLevel
    skills_required: List[str] = []
    benefits: List[str] = []
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    remote_allowed: Optional[bool] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    skills_required: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    application_url: Optional[str] = None
    application_deadline: Optional[datetime] = None

class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    views: int = 0
    applications: int = 0

    class Config:
        from_attributes = True

# User Models
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None

class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# User Profile Models
class UserProfileBase(BaseModel):
    skills: List[str] = []
    preferred_locations: List[str] = []
    preferred_job_types: List[JobType] = []
    salary_expectation_min: Optional[int] = None
    salary_expectation_max: Optional[int] = None
    remote_preference: bool = False
    notification_frequency: str = "daily"  # immediate, daily, weekly
    notification_channels: List[NotificationChannel] = [NotificationChannel.EMAIL]

class UserProfileCreate(UserProfileBase):
    user_id: int

class UserProfileUpdate(BaseModel):
    skills: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    preferred_job_types: Optional[List[JobType]] = None
    salary_expectation_min: Optional[int] = None
    salary_expectation_max: Optional[int] = None
    remote_preference: Optional[bool] = None
    notification_frequency: Optional[str] = None
    notification_channels: Optional[List[NotificationChannel]] = None

class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Notification Models
class NotificationBase(BaseModel):
    title: str
    message: str
    channel: NotificationChannel
    job_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    user_id: int

class Notification(NotificationBase):
    id: int
    user_id: int
    sent_at: datetime
    read_at: Optional[datetime] = None
    is_read: bool = False

    class Config:
        from_attributes = True

# Matching Models
class JobMatchBase(BaseModel):
    match_score: float = Field(..., ge=0, le=1)
    match_reasons: List[str] = []

class JobMatch(JobMatchBase):
    id: int
    user_id: int
    job_id: int
    job: Job
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Search and Filter Models
class JobSearchParams(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    remote_only: Optional[bool] = None
    skills: Optional[List[str]] = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

class JobSearchResponse(BaseModel):
    jobs: List[Job]
    total: int
    page: int
    size: int
    total_pages: int