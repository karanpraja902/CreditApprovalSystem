# Credit Approval System

## Overview
The Credit Approval System is a Django-based backend application designed to manage and evaluate credit and loan applications. It provides a robust API for customer management, loan processing, and automated credit scoring using data processing tools.

## Features
- **Customer Management**: Endpoints for registering and managing customer profiles.
- **Loan Processing**: Modules for loan application, tracking, and approval.
- **Credit Scoring**: Automated credit evaluation using Pandas and NumPy for data analysis.
- **Asynchronous Tasks**: Background task processing using Celery and Redis.
- **RESTful API**: Built with Django REST Framework (DRF).
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation via `drf-spectacular`.

## Architecture
The application is structured into the following key Django apps:
- `credit_scoring`: Contains the logic and data processing for evaluating creditworthiness.
- `customers`: Handles customer profiles and related information.
- `loans`: Manages the lifecycle of loan applications.
- `credit_approval_system`: The core Django project configuration.

## Technologies Used
- **Backend Framework**: Django 4.2+, Django REST Framework
- **Database**: PostgreSQL (via `psycopg2-binary`)
- **Task Queue**: Celery with Redis broker
- **Data Processing**: Pandas, NumPy, OpenPyXL
- **Documentation**: drf-spectacular

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis Server

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd CreditApprovalSystem
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the project root and configure your environment variables (e.g., Database credentials, Redis URL, Django Secret Key).

5. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Start Celery Worker (in a separate terminal):**
   ```bash
   celery -A credit_approval_system worker -l info
   ```

## API Documentation
Once the server is running, you can access the API documentation at:
- **Swagger UI:** `/api/schema/swagger-ui/`
- **Redoc:** `/api/schema/redoc/`

## Testing
To run the test suite with `pytest`:
```bash
pytest
```
