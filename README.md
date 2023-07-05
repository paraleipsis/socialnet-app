# SocialNet App

## Overview

This is a simple RESTful API for a social networking application built with FastAPI and providing the following functionality:

- Registration system, user management and authentication backend with cookie transport and JWT strategy. Using fastapi-users library
- Users have the ability to perform CRUD operations with posts
- Authorized users have the ability to like and dislike other users posts, but not their own
- Integration with Clearbit to get additional data about the user during registration (first name, last name). API key must be in src/auth/conf/auth
- Integration with Hunter.io for verifying email existence on registration. API key must be in src/auth/conf/auth
- Redis as a cache for storing posts likes and dislikes when accessed by id - GET /posts/{post_id} (does not work at the moment when accessing all posts GET /posts). Using fastapi-cache library

## Installation

- Install Python 3.9+
- Install Docker
- Clone this repository and navigate to it:
  
```bash
git clone https://github.com/paraleipsis/socialnet-app.git && cd socialnet-app
```

- Run services with Docker Compose:

```bash
docker compose up -d
```

Swagger UI documentation by default will be available at: <http://localhost:8003/api/docs>

Open API documentation by default will be available at: <http://localhost:8003/api/openapi.json>

## Configuration 

Authentication:

```bash
nano src/auth/conf/auth
```

Logging:

```bash
nano src/conf/logger_conf.yml
```

API server:

```bash
nano src/core/conf/core
```

PostgreSQL database:

```bash
nano src/db/conf/db
```

Redis cache system:

```bash
nano src/db/conf/cache
```

