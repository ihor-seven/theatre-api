![Logo of the project](https://raw.githubusercontent.com/jehna/readme-best-practices/master/sample-logo.png)

# Theatre API
> REST API for theatre plays, halls, tickets, and reservations

A Django + Django REST Framework project that provides endpoints for managing theatre plays, actors, genres, halls, performances, reservations, and tickets.  
Includes **JWT authentication** for secure access.

## Installing / Getting started

### Minimal setup
```bash
git clone https://github.com/ihor-seven/theatre-api.git
cd theatre-api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API will be available at:
http://127.0.0.1:8000/api/


## Demo Account
Login: user
Password: user1234


### Initial Configuration

Default database: SQLite
Production recommended: PostgreSQL (configure in settings.py)
Authentication: JWT (djangorestframework-simplejwt)

## Developing

Local development

```shell
git clone https://github.com/ihor-seven/theatre-api.git
cd theatre-api
pip install -r requirements.txt
python manage.py runserver
```

### Building

If using Docker:

```shell
docker-compose up --build
```

### Deploying / Publishing

In case there's some step you have to take that publishes this project to a
server, this is the right time to state it.

```shell
packagemanager deploy awesome-project -s server.com -u username -p password
```

And again you'd need to tell what the previous code actually does.

## Features

Play — theatre plays with description and actors
Actor — actors in the theatre
Genre — genres of plays
TheatreHall — halls with rows and seats
Performance — scheduled shows of plays in halls
Reservation — reservations made by users
Ticket — tickets with assigned row and seat

## Configuration

DATABASES → SQLite by default, PostgreSQL for production
JWT → endpoints for tokens (api/token/, api/token/refresh/)
STATIC/MEDIA → configured in settings.py

## Contributing

If you’d like to contribute:
Fork the repository
Use a feature branch
Submit a Pull Request

## Links

Repository: https://github.com/ihor-seven/theatre-api
Django docs: https://docs.djangoproject.com/
DRF docs: https://www.django-rest-framework.org/