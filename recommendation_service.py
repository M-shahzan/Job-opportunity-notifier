import spacy
import pandas as pd
from models import Job, SeekerPreference
from flask import current_app
import re


class JobRecommendationService:
    def __init__(self):
        # Load spaCy medium model for word vectors
        self.nlp = spacy.load("en_core_web_md")
        self.job_profiles = None
        self.job_docs = None
        self.MIN_SIMILARITY = 0.1  # Minimum similarity threshold to filter results

    def preprocess(self, text):
        if not text:
            return ""
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        return text.lower().strip()

    def prepare_job_data(self):
        jobs = Job.query.all()
        profiles = []
        for job in jobs:
            combined = " ".join(filter(None, [
                job.title, job.skills_required, job.job_type, job.experience_level
            ]))
            profiles.append({
                "id": job.id,
                "profile_text": self.preprocess(combined),
                "job": job
            })
        self.job_profiles = pd.DataFrame(profiles)
        # Convert each profile to a spaCy Doc
        self.job_docs = [self.nlp(row["profile_text"]) for _, row in self.job_profiles.iterrows()]

    def create_user_doc(self, prefs):
        parts = [prefs.skills, prefs.job_type, prefs.experience_level]
        text = self.preprocess(" ".join(filter(None, parts)))
        return self.nlp(text)

    def get_recommendations(self, user_id, top_n=5):
        prefs = SeekerPreference.query.filter_by(user_id=user_id).first()
        if not prefs:
            return []

        self.prepare_job_data()
        user_doc = self.create_user_doc(prefs)
        # Compute similarity scores
        sims = [user_doc.similarity(job_doc) for job_doc in self.job_docs]
        # Pair scores with jobs
        scored = sorted(
            zip(sims, self.job_profiles["job"]),
            key=lambda x: x[0],
            reverse=True
        )
        # Filter by location and minimum similarity threshold
        recs = []
        for score, job in scored:
            if score < self.MIN_SIMILARITY:
                continue
            if prefs.location and prefs.location.lower() not in job.location.lower():
                continue
            recs.append({
                "job_id": job.id,
                "similarity_score": round(score, 3),
                "job": job
            })
            if len(recs) >= top_n:
                break
        return recs


recommendation_service = JobRecommendationService()
