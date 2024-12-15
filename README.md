# FastAPI Project

This is a FastAPI project designed for Python 3.12.3 or later. Follow the steps below to set up, configure, and run the project in both development and production modes.

---

## Prerequisites

- **Python**: Version 3.12.3 or later.
- **Virtual Environment**: For isolating dependencies.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-root>
```

### 2. Create a Virtual Environment

For **Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

For **Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Run the following command to install the required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Environment Variables

1. Create a `.env` file at the project root:
```bash
touch .env
```
2. Copy the contents of `.env.example` into the newly created `.env` file.
3. Update the values in `.env` as required.

---

## Running the Application

### Development Mode
To run the application in development mode:
```bash
fastapi dev main.py --port 9000
```

### Production Mode
To run the application in production mode:
```bash
fastapi main.py --port 9000
```

The application will start on [http://localhost:9000](http://localhost:9000).

---

## Notes

- Ensure you are using **Python 3.12.3 or later**.
- Always activate the virtual environment before running the project.
- Update the `.env` file with the required environment variables.

---

## License
[MIT License](LICENSE)

---

## Contributing
Feel free to submit issues or create pull requests to improve this project.

---

**Happy Coding!** ✨
