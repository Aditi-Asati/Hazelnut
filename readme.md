# Hazelnut

**Hazelnut: Nutty Precision for your SQL Queries**

<!-- [![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/hazelnut/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) -->

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [API Usage](#api-usage)
- [Guidelines](#guidelines)
- [License](#license)


## Introduction

Hazelnut is an LLM-powered SQL query builder and executer designed to simplify and automate database interactions. With Hazelnut, you can generate and execute SQL queries efficiently, making database management easier than ever.

## Features

- **LLM-Powered Query Generation**: Generate SQL queries using natural language input.
- **Query Execution**: Execute the generated queries directly on your database and see the result.
- **Database schema aware**: Knows the entire schema/structure of the given database to answer queries schematically.
- **Context aware chatbot**: Can response to questions while also considering the previous conversation.
- **User-Friendly Interface**: Easy-to-use interface for seamless interaction.

## Installation

To get started with Hazelnut, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Aditi-Asati/Hazelnut.git
    cd Hazelnut
    ```

2. **Build Docker Image**:
    ```bash
    docker build -t hazelnut . 
    ```

<!-- 3. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add your database credentials.
    ```plaintext
    DB_HOST=your_database_host
    DB_USER=your_database_user
    DB_PASS=your_database_password
    DB_NAME=your_database_name
    ``` -->

## API Usage

Hazelnut provides a set of API endpoints to facilitate the generation and execution of SQL queries through a FastAPI backend. Below are the details of each endpoint:

### 1. Submit Form

**Endpoint**: `POST http://localhost:8000/submit`

**Description**: This endpoint is used to submit database connection details. It returns a session ID that is used for subsequent requests.

**Request Body**:
```json
{
    "host": "your_database_host",
    "port": your_database_port,
    "username": "your_database_username",
    "password": "your_database_password",
    "database": "your_database_name"
}
```

**Response**
```json
{
    "session_id": "generated_session_id"
}
```
### 1.  Chat

**Endpoint**: `POST http://localhost:8000/chat/{session_id}`

**Description**: This endpoint accepts a session ID as a path parameter and a question as part of the request body. It returns the generated SQL query.

**Request Body**:
```json
{
    "question": "your_question_here",
    "credentials": {
        "host": "your_database_host",
        "port": your_database_port,
        "username": "your_database_username",
        "password": "your_database_password",
        "database": "your_database_name"
}
}
```

**Response**
```json
{
    "answer": "generated_sql_query"
}
```

### 1. Execute query

**Endpoint**: `POST http://localhost:8000/execute`

**Description**: This endpoint executes the provided SQL query on the database and returns the query results.

**Request Body**:
```json
{
    "question": "generated_sql_query",
    "credentials": {
        "host": "your_database_host",
        "port": your_database_port,
        "username": "your_database_username",
        "password": "your_database_password",
        "database": "your_database_name"
    }
}
```

**Response**
```json
{
    "result": [
        // list of rows with query results
    ],
    "columns": [
        // list of column names
    ]
}
```

## Guidelines
1. **Start the Application**:
    ```bash
    docker run -p 8000:8000 -p 8501:8501 hazelnut
    ```

2. **Interact with Hazelnut**:
    - Use the interface to input natural language queries.
    - Review and execute the generated SQL queries.

3. **Example**:
    - Input: "Show me all customers from New York"
    - Generated SQL: `SELECT * FROM customers WHERE city = 'New York';`


## License

Hazelnut is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for more details.


<!-- 
### running the api

execute

```
python -m src.api.api
```

from project root -->