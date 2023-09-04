# Notes Application

## Description

Welcome to the Flask Notes Website, a simple web application for managing and organizing your notes with user authentication.

## Installation

Clone the repository
```bash
$ git https://github.com/NightWalker7558/notes-flask.git
$ cd notes/flask
```

To run the app flawlessly, satisfy the requirements
```bash
$ pip install -r requirements.txt
```

### Initialize Database 'notes.db'
```bash
$ python init_db.py
```

### Start Server
```bash
$ flask run
```

Or run this command
```bash
$ python -m flask run
```

## Features

- **User Sign-Up and Authentication:** Users can create accounts and securely log in to the application to manage their notes.

- **Note Creation:** Easily create new notes using the user-friendly interface.

- **Note Labeling:** Organize your notes with labels or categories to keep them well-structured.

- **User-Friendly Interface:** The application features an intuitive and visually appealing user interface, making it accessible even for those new to web development.

- **Database Storage:** Notes and user information are securely stored in the 'notes.db' database.

## Codebase

The Flask Notes Website is built using a series of templates to create a cohesive and user-friendly interface. Here's a brief overview of the templates used in the codebase:

### Navbar Template

- **Purpose**: The navbar template provides navigation links and options for users, depending on whether they are logged in or not.
- **Contents**: When logged out, it displays "Login" and "Register" buttons. When signed in, it features links to the "Home," "Notes," and "Profile" pages in a dropdown menu.

### Layout Template

- **Purpose**: The layout template serves as the basic structure for all other pages in the application.
- **Contents**: It includes the common HTML structure, headers, and imports required for consistency across all pages.

### Index Template

- **Purpose**: The index template is the home page of the application.
- **Contents**: It comprises a welcome message and an image, providing users with an inviting introduction to the website.

### Login Template

- **Purpose**: The login template is used for the user login page.
- **Contents**: It includes the login form and related components to allow users to enter their credentials.

### Registration Template

- **Purpose**: The registration template is used for the user registration page.
- **Contents**: It includes the registration form and related components to enable users to sign up for an account.

### Notes Template

- **Purpose**: The notes template is used for the main notes page.
- **Contents**: It includes panels for labels on the left-hand side and a display area for the notes on the remaining part of the page. There's a button in the bottom right corner to open an overlay for creating new notes. Additionally, there's a button in the label panel for adding new labels. Users can view notes by clicking on them to open an overlay, edit notes using the pen icon, and delete notes using the trash icon.

### Edit Note Template

- **Purpose**: The edit note template is used when users want to edit a specific note.
- **Contents**: It provides the necessary form and components to make edits to an existing note.

These templates work together to create a seamless and user-friendly experience for managing and organizing notes in the Flask Notes Website. You can explore the individual templates in the codebase for more details on their structure and functionality.

## app.py - Logic and Backend Code

The `app.py` file serves as the heart of the Flask Notes Website, containing all the logic and backend code that powers the application. Here's a brief overview of its functionality:

- **User Authentication**: `app.py` handles user authentication, including user sign-up, login, and logout processes. It ensures that only authenticated users can access certain parts of the application, such as creating, editing, or deleting notes.

- **Note Management**: The file manages the creation, updating, and deletion of notes. It also handles the organization of notes into labels, enabling users to categorize and find their notes easily.

- **Database Interaction**: `app.py` communicates with the database to store and retrieve user information, notes, labels, and their relationships. It uses SQLite3 to interact with the database, ensuring data integrity and security.

- **Routing**: The file defines the routes and views for various pages in the application, including the home page, notes page, profile page, and more.

- **Templates Integration**: It integrates the templates described earlier into the application, rendering the user interface and handling user interactions.

---

### Database Schema

The Flask Notes Website relies on a structured database schema defined in `schema.sql`. Here's an explanation of the schema and its purpose:

#### `users` Table

- **Columns**:
  - `id`: Unique user identifier.
  - `username`: User's username.
  - `email`: User's email address.
  - `password_hash`: Securely hashed password.
  - `authenticated`: Boolean indicating user authentication status.

#### `notes` Table

- **Columns**:
  - `id`: Unique note identifier.
  - `user_id`: Foreign key linking notes to their respective users.
  - `title`: Title of the note.
  - `note_content`: The content of the note.
  - `created_at`: Timestamp for note creation.
  - `updated_at`: Timestamp for the last note update.

#### `labels` Table

- **Columns**:
  - `id`: Unique label identifier.
  - `user_id`: Foreign key linking labels to their respective users.
  - `label_name`: Name or title of the label.
  - `created_at`: Timestamp for label creation.
  - `updated_at`: Timestamp for the last label update.

#### `notes_labels` Table

- **Columns**:
  - `note_id`: Foreign key linking notes to their associated labels.
  - `label_id`: Foreign key linking labels to their associated notes.

This structured database schema enables the Flask Notes Website to efficiently store and manage user information, notes, labels, and their relationships, ensuring a smooth and organized user experience.