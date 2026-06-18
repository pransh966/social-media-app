# Social Media API

A RESTful backend API for a social media platform built with FastAPI and PostgreSQL. The project provides user authentication, post management, and voting functionality using JWT-based authorization.

## Features

* User registration and authentication
* JWT-based authorization
* Create, read, update, and delete posts
* Voting system
* PostgreSQL database integration
* Password hashing with bcrypt
* Pydantic schema validation

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT
* Passlib
* Uvicorn

## Project Structure

```
social-media-app
│
├── app
│   ├── routers
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── user.py
│   │   └── vote.py
│   ├── config.py
│   ├── database.py
│   ├── model.py
│   ├── oauth2.py
│   ├── schemas.py
│   ├── utils.py
│   └── main.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/pransh966/social-media-app.git
cd social-media-app
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

## Environment Variables

Create a `.env` file and configure:

```env
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_USERNAME=
DATABASE_PASSWORD=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

## API Endpoints

### Authentication

* POST `/login`

### Users

* POST `/users`
* GET `/users/{id}`

### Posts

* GET `/posts`
* GET `/posts/{id}`
* POST `/posts`
* PUT `/posts/{id}`
* DELETE `/posts/{id}`

### Votes

* POST `/vote`

## API Documentation

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

## Future Improvements

* Comments system
* Likes system
* Search and filtering
* Pagination
* Unit testing with Pytest
* Docker support
* Deployment
