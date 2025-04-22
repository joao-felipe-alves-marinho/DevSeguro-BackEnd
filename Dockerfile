# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

# Set workdir
WORKDIR /app

# System dependencies for Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install to isolated location
COPY requirements.txt .
RUN pip install --prefix=/install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy project
COPY . /app

# Collect static files
ENV DJANGO_SETTINGS_MODULE=BackEnd.settings
RUN python manage.py collectstatic --noinput

# Apply migrations at container start
ENTRYPOINT ["/app/entrypoint.sh"]

# Start Gunicorn
CMD ["gunicorn", "BackEnd.wsgi:application", "--bind", "0.0.0.0:8000"]