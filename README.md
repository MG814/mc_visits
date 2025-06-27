[![codecov](https://codecov.io/gh/MG814/mc_visits/graph/badge.svg?token=FCXA3J9DX0)](https://codecov.io/gh/MG814/mc_visits)

# Visits Microservice

A microservice for managing medical appointments and doctor availability in the MediCare system.

## Description

The **Visits** microservice is responsible for comprehensive management of medical appointments within the MediCare healthcare system. It enables creating, updating, and viewing appointments, managing doctors' availability, and sending automated appointment reminders.

### Key Features:

- **Appointment Management** – create, edit, and view medical appointments
- **Soft Delete** – soft deletion of appointments (they remain in the database but are hidden from users)
- **Email Reminders** – automatic email reminders for upcoming appointments (via Celery)
- **Doctor Availability** – manage doctors’ schedules and visit pricing

## 🛠 Technologies

- **python 3.13**
- **django 5.1** 
- **djangorestframework 3.15.2** 
- **psycopg2-binary 2.9.10** 
- **celery 5.4.0** 
- **redis 5.2.1** 
- **django-celery-beat 2.7.0** 
- **django-environ 0.11.2** 
- **requests 2.32.3** 
- **drf-spectacular 0.28.0**
- **factory-boy 3.3.1** 
- **responses 0.25.7**
- **coverage 7.6.1** 
- **bandit 1.8.0** 
- **ruff 0.9.1** 
- **safety 3.2.14** 

### Setup

#### 1. Clone the repository

```bash
git clone https://github.com/MG814/mc_visits.git
cd mc_visits
```

#### 2. Running the entire application:

```bash
docker-compose up --build
```

#### 3. Migrations (in a separate terminal):

```bash
docker-compose exec web-visits python src/manage.py migrate
```