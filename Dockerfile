FROM python:3.14

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY sutt_project/requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Change to Django project directory
WORKDIR /app/sutt_project

# Collect static files
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "sutt_project.wsgi:application", "--bind", "0.0.0.0:8000"]
