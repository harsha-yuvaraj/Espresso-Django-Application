# Use the official Python base image
FROM python:3.13-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Set working directory
WORKDIR /app

# Copy the entire project files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the app will run on
EXPOSE ${PORT}

# Run the application using Gunicorn
CMD ["sh", "-c", "gunicorn espressso-blogs-project.wsgi:application --bind 0.0.0.0:${PORT}"]

