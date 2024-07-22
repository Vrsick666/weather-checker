FROM python:3.11-alpine

# Set up environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /src

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt /src

# Install dependencies
RUN pip install --upgrade -r requirements.txt

# Copy the entire application code
COPY . /src

# Expose the port your application will run on
EXPOSE 5000

# Specify the command to run on container start
CMD ["python", "src/app.py"]