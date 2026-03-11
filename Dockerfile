# Use Python as the base image
FROM python:3.12

# Set working directory
WORKDIR /WikiJuice

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r WikiJuice/requirements.txt

# Run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]