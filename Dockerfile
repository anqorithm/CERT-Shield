# Use an official Python 3.11 image as a base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install

# Copy the rest of the application code
COPY . /app

# Expose the port that the application listens on
EXPOSE 8080

# Command to run the FastAPI application using the PORT environment variable
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]