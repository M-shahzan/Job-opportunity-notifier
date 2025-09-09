from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, SeekerPreference, Job, Application
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from recommendation_service import recommendation_service

seeker_bp = Blueprint("seeker", __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@seeker_bp.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    if request.method == "POST":
        skills = request.form["skills"]
        location = request.form["location"]
        job_type = request.form["job_type"]
        experience_level = request.form["experience_level"]
        
        preference = SeekerPreference.query.filter_by(user_id=current_user.id).first()
        if preference:
            preference.skills = skills
            preference.location = location
            preference.job_type = job_type
            preference.experience_level = experience_level
        else:
            preference = SeekerPreference(
                user_id=current_user.id,
                skills=skills,
                location=location,
                job_type=job_type,
                experience_level=experience_level
            )
            db.session.add(preference)
        db.session.commit()
        flash("Preferences saved!", "success")
        return redirect(url_for("home"))
    
    preference = SeekerPreference.query.filter_by(user_id=current_user.id).first()
    return render_template("seeker_preferences.html", preference=preference)

@seeker_bp.route("/jobs")
@login_required
def view_jobs():
    if current_user.role != "seeker":
        flash("Only seekers can view jobs!", "danger")
        return redirect(url_for("home"))
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template("jobs.html", jobs=jobs)

@seeker_bp.route("/recommendations")
@login_required
def recommendations():
    if current_user.role != "seeker":
        flash("Only seekers can view recommendations!", "danger")
        return redirect(url_for("home"))
    
    # Generate recommendations
    recs = recommendation_service.get_recommendations(user_id=current_user.id, top_n=10)
    # recs is a list of dicts with keys: job_id, similarity_score, job
    return render_template("recommendations.html", recommendations=recs)

@seeker_bp.route("/apply/<int:job_id>", methods=["POST"])
@login_required
def apply_job(job_id):
    if current_user.role != "seeker":
        flash("Only seekers can apply for jobs!", "danger")
        return redirect(url_for("home"))
    
    job = Job.query.get_or_404(job_id)
    existing = Application.query.filter_by(seeker_id=current_user.id, job_id=job_id).first()
    if existing:
        flash("You have already applied for this job!", "warning")
        return redirect(url_for("seeker.view_jobs"))
    
    # File upload
    resume_filename = None
    if 'resume' in request.files:
        file = request.files['resume']
        if file and file.filename and allowed_file(file.filename):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            fname = secure_filename(file.filename)
            unique = f"{current_user.id}_{job_id}_{fname}"
            path = os.path.join(upload_folder, unique)
            file.save(path)
            resume_filename = unique
        elif file and file.filename:
            flash("Invalid file type; only PDF/DOC/DOCX allowed.", "danger")
            return redirect(url_for("seeker.view_jobs"))
    
    cover_letter = request.form.get("cover_letter")
    expected_salary = request.form.get("expected_salary")
    
    application = Application(
        seeker_id=current_user.id,
        job_id=job_id,
        resume_filename=resume_filename,
        cover_letter=cover_letter,
        expected_salary=expected_salary
    )
    db.session.add(application)
    db.session.commit()
    flash(f"Successfully applied for {job.title}!", "success")
    return redirect(url_for("seeker.view_jobs"))

@seeker_bp.route("/applications")
@login_required
def my_applications():
    if current_user.role != "seeker":
        flash("Only seekers can view applications!", "danger")
        return redirect(url_for("home"))
    
    applications = Application.query.filter_by(seeker_id=current_user.id)\
        .order_by(Application.applied_at.desc()).all()
    return render_template("applications.html", applications=applications)
