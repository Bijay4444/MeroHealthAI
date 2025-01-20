# MeroHealthAI

MeroHealthAI is a Django-based REST API project designed to simplify healthcare management. This application provides APIs for managing users, medications, schedules, and real-time communication through chat functionality.

## Features

- **User Management**: Register, authenticate, and manage users.
- **Medications**: Manage medication details, prescriptions, and schedules.
- **Schedules**: Create and manage schedules for patients and healthcare professionals.
- **Chat System**: Real-time communication between patients and healthcare professionals.
- **Task Management**: Background task handling with Celery.


## Installation

Follow these steps to set up and run the project:

### Prerequisites

- Python 3.8+
- Pip
- Virtualenv
- Redis (for Celery)
- Git

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/MeroHealthAI.git
   cd MeroHealthAI

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Configure your .env file:

    Create a .env file in the root directory and add the necessary environment variables, such as SECRET_KEY, database configuration, and Celery broker URL.

4. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

6. Start the development server:
    ```bash
    python manage.py runserver

7. (Optional) Start Celery for background tasks:
    ```bash
    celery -A MeroHealthAI worker --loglevel=info

8. (Optional) Start Redis server for Celery:

    Ensure Redis is running on your system. Use the following command to start Redis if installed locally:
    ```bash
    redis-server

#### API EndPoints
    The project provides RESTful APIs for all core functionalities. Below is a brief overview of the available endpoints:

    User Management:
        POST /api/users/register/: Register a new user.
        POST /api/users/login/: Login user and generate token.
        GET /api/users/profile/: Retrieve user profile.

    Medications:
        GET /api/medications/: List all medications.
        POST /api/medications/: Add a new medication.

    Schedules:
        GET /api/schedules/: List all schedules.
        POST /api/schedules/: Create a new schedule.

    Chat:
        GET /api/chat/messages/: Retrieve chat messages.
        POST /api/chat/messages/: Send a new message.

##### Technologies Used
    Backend: Django, Django REST Framework
    Task Queue: Celery with Redis
    Database: SQLite (Development), PostgreSQL (Production-ready)
    Authentication: Token-based authentication (e.g., JWT)
    Real-time Communication: Django Channels

###### Contribution Guidelines

    We welcome contributions! Please follow these steps to contribute:

        Fork the repository.
        Create a feature branch (git checkout -b feature-name).
        Commit your changes (git commit -m 'Add feature-name').
        Push to the branch (git push origin feature-name).
        Open a pull request.

###### License

This project is licensed under the MIT License. See the LICENSE file for more details.