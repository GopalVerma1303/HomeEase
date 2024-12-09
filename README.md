<div align="center">

<div align="center">
  <img src="https://github.com/GopalVerma1303/HomeEase/blob/ae60f93ff36303767c56ec52c3f1d346e6bd2cc4/logo.png" alt="HomeEaseLogo" height="100">
</div>

# HomeEase

### The household services management web application for customers, professionals, and administrators.

<br />

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Jinja](https://img.shields.io/badge/Jinja-B41717?style=for-the-badge&logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

</div>

<hr />

## Features

1. Analyzed the requirements and identified key features for customers, professionals, and administrators.
2. Designed the database schema to support user roles, services, and service requests.
3. Developed the backend using Flask to handle user authentication, service management, and request processing.
4. Created a responsive frontend using HTML, CSS, and JavaScript to ensure a user-friendly interface.
5. Implemented admin functionalities for user management and platform oversight.
6. Integrated a rating and review system for service quality feedback.

## Technologies Used

- **Backend:** Flask (Python web framework)
- **Database:** SQLite
- **ORM for DB:** SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript (Jinja templates)
- **UI Framework:** Bootstrap 5
- **Authentication:** Flask-Login
- **Password Hashing:** Werkzeug Security
- **Date/Time Handling:** datetime

## Database Design

1. **User**

   - Fields: id, username, email, password, role, is_blocked, date_created, address, pin_code

2. **Service**

   - Fields: id, name, base_price, time_required, description

3. **Professional**

   - Fields: id, user_id, service_id, experience, description, is_approved, documents, pin_code, avg_rating, total_services

4. **ServiceRequest**
   - Fields: id, service_id, customer_id, professional_id, date_of_request, date_of_completion, service_status, remarks, rating, review_remarks, has_review, location

## Contributing

We welcome contributions to HomeEase! Here's how you can help:

1. **Fork the Repository**

   - Create a fork of this project to your GitHub account

2. **Clone the Fork**

   ```bash
   git clone https://github.com/your-username/HomeEase.git
   cd HomeEase
   ```

3. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**

   - Write your code
   - Follow the existing code style
   - Add comments where necessary
   - Test your changes thoroughly

5. **Commit Changes**

   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

6. **Push to GitHub**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Describe your changes in detail

### Development Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

Please ensure your PR:

- Includes a clear description of the changes
- Has been tested locally
- Follows the existing code style
- Updates documentation if needed
