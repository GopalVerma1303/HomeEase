from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import User, Service, Professional, ServiceRequest
from werkzeug.security import generate_password_hash

admin_routes = Blueprint("admin", __name__)


@admin_routes.route("/admin/dashboard")
@login_required
def dashboard():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    # Get counts for dashboard statistics
    total_customers = User.query.filter_by(role="customer").count()
    total_professionals = Professional.query.count()
    total_services = Service.query.count()
    pending_approvals = Professional.query.filter_by(is_approved=False).all()

    # Get recent service requests with professionals and their average ratings
    recent_requests = (
        ServiceRequest.query.options(db.joinedload(ServiceRequest.professional))
        .order_by(ServiceRequest.date_of_request.desc())
        .limit(5)
        .all()
    )

    # Update average ratings for professionals
    for request in recent_requests:
        if request.professional:
            request.professional.update_rating()

    # Fetch data for charts
    rating_data = [0, 0, 0, 0, 0]
    for request in ServiceRequest.query.filter(ServiceRequest.rating.isnot(None)).all():
        rating_data[request.rating - 1] += 1

    service_request_data = [
        ServiceRequest.query.filter_by(service_status="requested").count(),
        ServiceRequest.query.filter_by(service_status="completed").count(),
        ServiceRequest.query.filter_by(service_status="rejected").count(),
    ]

    return render_template(
        "admin/dashboard.html",
        total_customers=total_customers,
        total_professionals=total_professionals,
        total_services=total_services,
        pending_approvals=pending_approvals,
        recent_requests=recent_requests,
        rating_data=rating_data,
        service_request_data=service_request_data,
    )


@admin_routes.route("/admin/users")
@login_required
def manage_users():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    role_filter = request.args.get("role", "all")
    search = request.args.get("search", "")

    query = User.query
    if role_filter != "all":
        query = query.filter_by(role=role_filter)
    if search:
        query = query.filter(User.username.ilike(f"%{search}%"))

    users = query.all()
    return render_template(
        "admin/manage_users.html", users=users, current_filter=role_filter
    )


@admin_routes.route("/admin/professionals")
@login_required
def manage_professionals():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    approval_filter = request.args.get("filter", "pending")
    search = request.args.get("search", "")

    query = Professional.query
    if approval_filter == "pending":
        query = query.filter_by(is_approved=False)
    elif approval_filter == "approved":
        query = query.filter_by(is_approved=True)

    if search:
        query = query.join(User).filter(User.username.ilike(f"%{search}%"))

    professionals = query.all()
    return render_template(
        "admin/manage_professionals.html",
        professionals=professionals,
        current_filter=approval_filter,
    )


@admin_routes.route("/admin/customers")
@login_required
def manage_customers():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    search_query = request.args.get("search", "")

    query = User.query.filter_by(role="customer")

    if search_query:
        query = query.filter(User.username.ilike(f"%{search_query}%"))

    customers = query.all()

    return render_template("admin/manage_customer.html", users=customers)


@admin_routes.route("/admin/services", methods=["GET", "POST"])
@login_required
def manage_services():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        action = request.form.get("action")
        if action == "create":
            name = request.form.get("name")
            price = float(request.form.get("price"))
            time_required = int(request.form.get("time_required"))
            description = request.form.get("description")
            lowercase_name = name.lower()
            uppercase_name = name.upper()
            service = Service(
                name=uppercase_name,
                base_price=price,
                time_required=time_required,
                description=description,
            )
            db.session.add(service)
            db.session.commit()
            flash("Service created successfully")

        elif action == "update":
            service_id = request.form.get("service_id")
            service = Service.query.get_or_404(service_id)
            service.name = request.form.get("name")
            service.base_price = float(request.form.get("price"))
            service.time_required = int(request.form.get("time_required"))
            service.description = request.form.get("description")
            db.session.commit()
            flash("Service updated successfully")

        elif action == "delete":
            service_id = request.form.get("service_id")
            service = Service.query.get_or_404(service_id)
            db.session.delete(service)
            db.session.commit()
            flash("Service deleted successfully")

    services = Service.query.all()
    return render_template("admin/manage_services.html", services=services)


@admin_routes.route("/admin/approve_professional/<int:professional_id>")
@login_required
def approve_professional(professional_id):
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    professional = Professional.query.get_or_404(professional_id)
    professional.is_approved = True
    db.session.commit()
    flash("Professional approved successfully")
    return redirect(url_for("admin.manage_professionals"))


@admin_routes.route("/admin/block_user/<int:user_id>")
@login_required
def block_user(user_id):
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    user = User.query.get_or_404(user_id)
    user.is_blocked = not user.is_blocked
    db.session.commit()
    flash(f'User {"blocked" if user.is_blocked else "unblocked"} successfully')
    return redirect(url_for("admin.manage_users"))


@admin_routes.route("/admin/service_requests")
@login_required
def manage_service_requests():
    if current_user.role != "admin":
        flash("Access denied")
        return redirect(url_for("auth.login"))

    status_filter = request.args.get("status", "all")
    search = request.args.get("search", "")

    query = ServiceRequest.query
    if status_filter != "all":
        query = query.filter_by(service_status=status_filter)
    if search:
        query = query.join(User).filter(User.username.ilike(f"%{search}%"))

    requests = query.order_by(ServiceRequest.date_of_request.desc()).all()
    return render_template(
        "admin/service_requests.html", requests=requests, current_filter=status_filter
    )
