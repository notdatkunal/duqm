# Duqm Backend

This is the backend for the Duqm module, a Flask-based web application that serves a React frontend and provides a RESTful API.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   On Windows:
        ```bash
        venv\Scripts\activate
        ```
    -   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Run the application:**
    ```bash
    python main.py
    ```

2.  When you run the application for the first time, it will automatically:
    -   Create the necessary PostgreSQL database tables.
    -   Insert initial data and create default users.
    -   Open a web browser to `http://127.0.0.1:8989/fob`.

3.  The application will be running at `http://127.0.0.1:8989`. The API documentation is available at `http://127.0.0.1:8989/api/docs`.
