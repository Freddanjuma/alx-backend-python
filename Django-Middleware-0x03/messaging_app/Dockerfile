# 1. Base image
FROM python:3.10

# 2. Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# 3. Prevent Python buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# 4. Set working directory
WORKDIR /app

# 5. Copy dependencies first (layer caching)
COPY requirements.txt .

# 6. Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 7. Copy project files
COPY . .

# 8. Expose Django port
EXPOSE 8000

# 9. Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
