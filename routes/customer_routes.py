from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Service, ServiceRequest, Professional
from datetime import datetime

customer_routes = Blueprint("customer", __name__)


@customer_routes.route("/customer/dashboard")
@login_required
def dashboard():
    if current_user.role != "customer":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    service_requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
    best_packages = Service.query.order_by(Service.base_price).limit(3).all()

    # Prepare data for the service requests chart
    service_request_data = [
        ServiceRequest.query.filter_by(
            customer_id=current_user.id, service_status="requested"
        ).count(),
        ServiceRequest.query.filter_by(
            customer_id=current_user.id, service_status="completed"
        ).count(),
        ServiceRequest.query.filter_by(
            customer_id=current_user.id, service_status="rejected"
        ).count(),
    ]

    return render_template(
        "customer/dashboard.html",
        service_requests=service_requests,
        best_packages=best_packages,
        service_request_data=service_request_data,
    )


@customer_routes.route("/customer/search_services", methods=["GET", "POST"])
@login_required
def search_services():
    if current_user.role != "customer":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    search_term = request.form.get("search_term", "")
    pin_code = request.form.get("pin_code", "")

    query = Service.query

    if search_term:
        query = query.filter(Service.name.ilike(f"%{search_term}%"))

    if pin_code:
        # Join with professionals to filter by pin code
        query = query.join(Professional).filter(Professional.pin_code == pin_code)

    services = query.all()
    return render_template("customer/search_services.html", services=services)


@customer_routes.route(
    "/customer/create_request/<int:service_id>", methods=["GET", "POST"]
)
@login_required
def create_request(service_id):
    if current_user.role != "customer":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    service = Service.query.get_or_404(service_id)

    if request.method == "POST":
        date_str = request.form.get("date_of_request")
        time_str = request.form.get("time_of_request")
        remarks = request.form.get("remarks")

        try:
            date_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            location = request.form.get("location")
            if not location:
                flash("Location is required")
                return render_template("customer/create_request.html", service=service)

            new_request = ServiceRequest(
                service_id=service_id,
                customer_id=current_user.id,
                date_of_request=date_time,
                remarks=remarks,
                location=location,
            )
            db.session.add(new_request)
            db.session.commit()
            flash("Service request created successfully")
            return redirect(url_for("customer.dashboard"))
        except ValueError:
            flash("Invalid date or time format")

    return render_template("customer/create_request.html", service=service)


@customer_routes.route("/customer/close_request/<int:request_id>")
@login_required
def close_request(request_id):
    if current_user.role != "customer":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.customer_id != current_user.id:
        flash("Access denied")
        return redirect(url_for("customer.dashboard"))

    service_request.service_status = "completed"
    service_request.date_of_completion = datetime.utcnow()
    db.session.commit()
    flash("Service request closed")
    return redirect(url_for("customer.dashboard"))


@customer_routes.route("/customer/submit_review/<int:request_id>", methods=["POST"])
@login_required
def submit_review(request_id):
    if current_user.role != "customer":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.customer_id != current_user.id:
        flash("Access denied")
        return redirect(url_for("customer.dashboard"))

    rating = request.form.get("rating")
    remarks = request.form.get("remarks")

    service_request.rating = int(rating)
    service_request.review_remarks = remarks
    service_request.has_review = True

    # Get the professional associated with this service request
    professional = service_request.professional

    # Calculate new average rating
    completed_requests = ServiceRequest.query.filter(
        ServiceRequest.professional_id == professional.id,
        ServiceRequest.has_review == True,
        ServiceRequest.rating != None,
    ).all()

    total_rating = sum(req.rating for req in completed_requests)
    num_ratings = len(completed_requests)

    if num_ratings > 0:
        professional.avg_rating = total_rating / num_ratings
    else:
        professional.avg_rating = 0.0

    db.session.commit()

    flash("Review submitted successfully")
    return redirect(url_for("customer.dashboard"))


@customer_routes.route("/customer/service_history")
@login_required
def service_history():
    if current_user.role != "customer":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    service_requests = (
        ServiceRequest.query.filter_by(customer_id=current_user.id)
        .order_by(ServiceRequest.date_of_request.desc())
        .all()
    )
    return render_template(
        "customer/service_history.html", service_requests=service_requests
    )
