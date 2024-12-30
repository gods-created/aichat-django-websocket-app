# AIChat

## Overview
Online chat based on WebSocket and HTTP requests. The chat itself is implemented on WebSocket and interacts with ChatGPT via OpenAI API. The database used for storing dialogs is MongoDB. There are also available features, namely: saving a dialog, loading it into a dialog box and deleting it. The logic is simple and far from perfect, but the project itself is presented as an example of work using django, drf, drf-spectacular, channels, openai, mongoengine, there is no need for perfection.

---

## Local Launch Instructions

### Prerequisites
Ensure you have the following installed:
- [MongoDB](https://www.mongodb.com/)
- [Python](https://www.python.org/downloads/) (compatible version)
- [Brew (macOS)](https://brew.sh/) for package management

### Steps
1. **Install and start Redis:**
    ```bash
    brew install mongodb-community@8.0
    brew services start mongodb-community@8.0
    ```

2. **Set up the project:**
    ```bash
    cd /aichat
    python -m pip install -r requirements.txt
    ```

3. **Run the server and Celery worker:**
    ```bash
    python manage.py runserver localhost:5001 & \
    uvicorn aichat.asgi:application --host=localhost --port=50011 --reload
    ```
4. **Open http://localhost:5001/chat**
