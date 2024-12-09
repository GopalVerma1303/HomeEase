# Household Services Web Application

## IITM BS APPDEV 1 - Project Report

By Gopal Verma (22f3003061)

## Student Details

- **Name:** Gopal Verma
- **Roll No:** 22F3003061
- **Program:** BS in Data Science and Applications
- **Current Level:** DIPLOMA

## Project Details

### Problem Statement

Develop a web application for household services that connects customers with service professionals. The application should allow customers to request services, professionals to offer their services, and administrators to manage the platform.

### Approach

1. Analyzed the requirements and identified key features for customers, professionals, and administrators.
2. Designed the database schema to support user roles, services, and service requests.
3. Developed the backend using Flask to handle user authentication, service management, and request processing.
4. Created a responsive frontend using HTML, CSS, and JavaScript to ensure a user-friendly interface.
5. Implemented admin functionalities for user management and platform oversight.
6. Integrated a rating and review system for service quality feedback.

## Technologies Used

### Frameworks and Libraries

- **Backend:** Flask (Python web framework)
- **Database:** SQLite
- **ORM for DB:** SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript (Jinja templates)
- **UI Framework:** Bootstrap 5
- **Authentication:** Flask-Login
- **Password Hashing:** Werkzeug Security
- **Date/Time Handling:** datetime

## Database Design

### Database Tables and Relations

#### Tables

1. **User**

   - Fields: id, username, email, password, role, is_blocked, date_created, address, pin_code

2. **Service**

   - Fields: id, name, base_price, time_required, description

3. **Professional**

   - Fields: id, user_id, service_id, experience, description, is_approved, documents, pin_code, avg_rating, total_services

4. **ServiceRequest**
   - Fields: id, service_id, customer_id, professional_id, date_of_request, date_of_completion, service_status, remarks, rating, review_remarks, has_review, location

#### Relations

- User one-to-one Professional
- Service one-to-many Professional
- User one-to-many ServiceRequest (as customer)
- Professional one-to-many ServiceRequest
- Service one-to-many ServiceRequest

## Presentation and Demo Video

[APPDEV1_PPT\_&_DEMO.mov](https://drive.google.com/file/d/1JdFGrQhE46orwNqGL-_Kb4vuYtFCLieA/view?usp=sharing)
