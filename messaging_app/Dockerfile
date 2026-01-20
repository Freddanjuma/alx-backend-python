# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install all dependencies
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --default-timeout=200 -i https://pypi.python.org/simple/


# Copy the project files into the container
COPY . /app/

# Expose Django’s default port
# NOTE: Use -p 8000:8000 when running the container
EXPOSE 8000

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
