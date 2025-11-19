# Quickstart Guide

This guide provides instructions for setting up and running the development environment.

## Prerequisites

*   Node.js (v18+) and npm
*   Python (v3.10+) and pip
*   Docker

## Backend Setup (FastAPI)

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file will be created in a later phase)*

3.  **Set up environment variables:**
    Create a `.env` file in the `backend` directory and add the following:
    ```
    GOOGLE_API_KEY="your_gemini_api_key"
    LANGCHAIN_API_KEY="your_langsmith_api_key"
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_PROJECT="cv-sob-medida"
    ```

4.  **Run the development server:**
    ```bash
    uvicorn app.main:app --reload --port 8000
    ```

## Frontend Setup (React)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:5173`.

## Running with Docker

1.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```
    This will start both the backend and frontend services.
