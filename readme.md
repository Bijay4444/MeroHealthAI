# MeroHealthAI - Medication Reminder System

A comprehensive medication management system designed to help users track and adhere to their medication schedules through timely reminders and adherence monitoring.

## Overview

MeroHealthAI is a Django-based backend application that provides a robust API for medication management, scheduling reminders, and tracking adherence. The system uses Celery for task scheduling to ensure timely medication reminders and notifications.

## Features

- **User Authentication**: Secure JWT-based authentication system
- **Medication Management**: Create, update, and track medications
- **Reminder Scheduling**: Set up custom medication schedules with various frequencies
- **Real-time Notifications**: Receive timely reminders for medication doses
- **Adherence Tracking**: Monitor medication adherence with detailed reports
- **Caregiver Support**: Allow caregivers to monitor patient medication adherence

## Tech Stack

- **Backend**: Django 5.1.5, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Task Scheduling**: Celery with Redis broker
- **Authentication**: JWT (JSON Web Tokens)
- **Notifications**: Firebase Cloud Messaging (FCM)
- **Time Management**: Timezone-aware scheduling with pytz

## Requirements

- Python 3.10+
- Redis Server (for Celery)
- Firebase Admin SDK credentials (for push notifications)

## Installation

1. Clone the repository:
  git clone https://github.com/Bijay4444/MeroHealthAI.git
  cd MeroHealthAI

2. Create and activate a virtual environment:
  python -m venv venv
  source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:
  pip install -r requirements.txt


4. Set up environment variables:
  Create a `.env` file in the project root with the following variables:
  SECRET_KEY=your_secret_key
  DEBUG=True
  FCM_SERVER_KEY=your_firebase_cloud_messaging_key

5. Run migrations:
  python manage.py migrate

6. Start Redis server (for Celery):
  redis-server --port 6380

9. Run the development server:
  python manage.py runserver 0.0.0.0:8080


## API Endpoints

### Authentication
- `POST /users/token/`: Obtain JWT token
- `POST /users/token/refresh/`: Refresh JWT token
- `POST /users/register/`: Register new user

### Medications
- `GET /medications/`: List all medications
- `POST /medications/`: Create new medication
- `GET /medications/{id}/`: Retrieve medication details
- `PUT /medications/{id}/`: Update medication
- `DELETE /medications/{id}/`: Delete medication

### Schedules
- `GET /medications/schedules/`: List all medication schedules
- `POST /medications/create-with-schedule/`: Create medication with schedule
- `GET /schedules/reminders/`: List all reminders
- `POST /schedules/reminders/{id}/mark-taken/`: Mark reminder as taken
- `POST /schedules/reminders/{id}/mark-skipped/`: Mark reminder as skipped

### Adherence Records
- `GET /schedules/adherence-records/`: Get adherence records
- `GET /schedules/adherence-records/{id}/`: Get specific adherence record

## Celery Tasks

The project uses Celery for scheduled tasks:

- `generate_daily_reminders`: Creates reminders for medications (runs daily at midnight)
- `check_upcoming_reminders`: Checks for upcoming reminders (runs every minute)
- `clean_old_reminders`: Cleans up old reminders (runs weekly)

## Timezone Handling

The system is designed to work with Nepal timezone (Asia/Kathmandu) by default but supports timezone-aware scheduling for reminders.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


