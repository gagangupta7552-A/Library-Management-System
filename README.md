# Library Management System

A console-based Library Management System developed using **Python, Object-Oriented Programming (OOP), and SQLite**. The system provides essential functionality for managing books, students, and book transactions through a simple command-line interface.

## Overview

The project is designed to digitize basic library operations and maintain records efficiently. It supports separate functionalities for administrators and students, with persistent data storage using SQLite.

## Features

* Admin authentication
* Student registration and login
* Add and view library books
* Search books by title or author
* Issue and return books
* Automatic due-date management
* Fine calculation for overdue books
* View currently issued books
* Persistent data storage using SQLite

## Technologies

* **Language:** Python
* **Database:** SQLite
* **Concepts:** Object-Oriented Programming, SQL, File/Database Handling

## OOP Concepts Implemented

The project demonstrates the practical use of:

* Classes and Objects
* Constructors
* Inheritance
* Encapsulation
* Composition
* Methods

## Project Structure

```text
Library-Management-System/
│
├── main.py
├── README.md
└── library.db
```

`library.db` is automatically generated when the application is executed.

## Getting Started

### Prerequisites

* Python 3.x
* Visual Studio Code or any Python-compatible IDE

### Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd Library-Management-System
```

Run the application:

```bash
python main.py
```

## Default Admin Credentials

```text
Username: admin
Password: admin123
```

Students can create an account using the registration option.

## Fine Policy

* Borrowing period: **14 days**
* Late return fine: **₹5 per day**

## Project Objective

The objective of this project is to apply Python programming and OOP concepts to develop a practical database-driven application while gaining experience in application logic, data management, and user authentication.

## Author

**Gagan Gupta**
B.Tech CSE

## Future Enhancements

* Graphical User Interface
* Role-based access control
* Book categories and advanced filtering
* Transaction history and reports
* Improved authentication and security


