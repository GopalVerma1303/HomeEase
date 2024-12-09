from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import ServiceRequest, Professional, User, Service
from datetime import datetime, date

professional_routes = Blueprint("professional", __name__)


@professional_routes.route("/professional/dashboard")
@login_required
def dashboard():
    if current_user.role != "professional":
        flash("Access denied")
        return redirect(url_for("auth.login"))
    professional_profile = Professional.query.filter_by(user_id=current_user.id).first()
    if not professional_profile:
        flash("Please complete your professional profile")
        return redirect(url_for("professional.profile"))

    # Get all available service requests for this professional's service type
    available_requests = ServiceRequest.query.filter(
        ServiceRequest.service_id == professional_profile.service_id,
        ServiceRequest.service_status == "requested",
    ).all()

    # Get all assigned requests for this professional
    assigned_requests = ServiceRequest.query.filter_by(
        professional_id=professional_profile.id, service_status="assigned"
    ).all()

    # Get completed requests for statistics
    completed_requests = ServiceRequest.query.filter_by(
        professional_id=professional_profile.id, service_status="completed"
    ).all()

    # Prepare data for the rating chart
    rating_data = [0, 0, 0, 0, 0]
    for request in completed_requests:
        if request.rating:
            rating_data[request.rating - 1] += 1

    # Prepare data for the service requests chart
    service_request_data = [
        ServiceRequest.query.filter_by(
            professional_id=professional_profile.id, service_status="requested"
        ).count(),
        ServiceRequest.query.filter_by(
            professional_id=professional_profile.id, service_status="completed"
        ).count(),
        ServiceRequest.query.filter_by(
            professional_id=professional_profile.id, service_status="rejected"
        ).count(),
    ]

    return render_template(
        "professional/dashboard.html",
        professional_profile=professional_profile,
        available_requests=available_requests,
        assigned_requests=assigned_requests,
        completed_requests=completed_requests,
        rating_data=rating_data,
        service_request_data=service_request_data,
    )


@professional_routes.route("/professional/profile", methods=["GET", "POST"])
@login_required
def profile():
    if current_user.role != "professional":
        flash("Access denied")
        return redirect(url_for("auth.login"))
    professional = Professional.query.filter_by(user_id=current_user.id).first()
    services = Service.query.all()

    if request.method == "POST":
        service_id = request.form.get("service_id")
        experience = request.form.get("experience")
        description = request.form.get("description")

        if not professional:
            professional = Professional(
                user_id=current_user.id,
                service_id=service_id,
                experience=experience,
                description=description,
            )
            db.session.add(professional)
        else:
            professional.service_id = service_id
            professional.experience = experience
            professional.description = description

        db.session.commit()
        flash("Profile updated successfully")
        return redirect(url_for("professional.dashboard"))

    return render_template(
        "professional/profile.html", professional=professional, services=services
    )


@professional_routes.route("/professional/accept_request/<int:request_id>")
@login_required
def accept_request(request_id):
    if current_user.role != "professional":
        flash("Access denied")
        return redirect(url_for("auth.login"))
    professional = Professional.query.filter_by(user_id=current_user.id).first()
    if not professional:
        flash("Please complete your professional profile")
        return redirect(url_for("professional.profile"))
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.service_id != professional.service_id:
        flash("Access denied")
        return redirect(url_for("professional.dashboard"))
    service_request.professional_id = professional.id
    service_request.service_status = "assigned"
    db.session.commit()
    flash("Service request accepted")
    return redirect(url_for("professional.dashboard"))


@professional_routes.route("/professional/reject_request/<int:request_id>")
@login_required
def reject_request(request_id):
    if current_user.role != "professional":
        flash("Access denied")
        return redirect(url_for("auth.login"))
    professional = Professional.query.filter_by(user_id=current_user.id).first()
    if not professional:
        flash("Please complete your professional profile")
        return redirect(url_for("professional.profile"))
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.service_id != professional.service_id:
        flash("Access denied")
        return redirect(url_for("professional.dashboard"))
    service_request.service_status = "rejected"
    db.session.commit()
    flash("Service request rejected")
    return redirect(url_for("professional.dashboard"))
