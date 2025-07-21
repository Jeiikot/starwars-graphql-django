FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Create a directory para el proyecto
RUN mkdir /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . .

EXPOSE 8000

# Collect static files for production
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "api.wsgi", "--bind", "0.0.0.0:8000"]
