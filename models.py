from flask_login import UserMixin
from extensions import db
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.Text)
    pin_code = db.Column(db.String(10))


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)


class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    experience = db.Column(db.Integer)
    description = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    documents = db.Column(db.Text)
    avg_rating = db.Column(db.Float, default=0.0)
    total_services = db.Column(db.Integer, default=0)
    user = db.relationship("User", backref="professional_profile")
    service = db.relationship("Service", backref="professionals")

    def update_rating(self):
        completed_requests = ServiceRequest.query.filter_by(
            professional_id=self.id, service_status="completed"
        ).all()

        if completed_requests:
            total_rating = sum(req.rating for req in completed_requests if req.rating)
            rated_requests = sum(1 for req in completed_requests if req.rating)
            self.avg_rating = total_rating / rated_requests if rated_requests > 0 else 0
            self.total_services = len(completed_requests)
            db.session.commit()


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.id"))
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime)
    service_status = db.Column(db.String(20), default="requested")
    remarks = db.Column(db.Text)
    rating = db.Column(db.Integer)
    review_remarks = db.Column(db.Text)
    has_review = db.Column(db.Boolean, default=False)
    location = db.Column(db.Text, nullable=False)
    service = db.relationship("Service", backref="service_requests")
    customer = db.relationship(
        "User", foreign_keys=[customer_id], backref="customer_requests"
    )
    professional = db.relationship("Professional", backref="professional_requests")
