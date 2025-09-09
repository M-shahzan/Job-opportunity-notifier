from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Job

employer_bp = Blueprint("employer", __name__)

# Dashboard showing employer's jobs
@employer_bp.route("/jobs")
@login_required
def jobs():
    if current_user.role != "employer":
        flash("Only employers can view this page!", "danger")
        return redirect(url_for("home"))

    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template("employer_jobs.html", jobs=jobs)

# Add a new job
@employer_bp.route("/add-job", methods=["GET", "POST"])
@login_required
def add_job():
    if current_user.role != "employer":
        flash("Only employers can add jobs!", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        job = Job(
            employer_id=current_user.id,
            title=request.form["title"],
            description=request.form["description"],
            location=request.form["location"],
            skills_required=request.form["skills_required"],
            job_type=request.form["job_type"],
            experience_level=request.form["experience_level"]
        )
        db.session.add(job)
        db.session.commit()
        flash("Job added successfully!", "success")
        return redirect(url_for("employer.jobs"))

    return render_template("add_job.html")

# Remove a job
@employer_bp.route("/delete-job/<int:job_id>", methods=["POST"])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)

    if job.employer_id != current_user.id:
        flash("You cannot delete this job!", "danger")
        return redirect(url_for("employer.jobs"))

    db.session.delete(job)
    db.session.commit()
    flash("Job removed successfully!", "success")
    return redirect(url_for("employer.jobs"))
