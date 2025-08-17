# Use Python base image
FROM python:3.12-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only UI folder content
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set Streamlit environment variables
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ENABLECORS=false

# Expose Streamlit default port for Cloud Run / localhost
EXPOSE 8080

# Run Streamlit on container start
# CMD ["streamlit", "run", "Home.py"]
CMD ["streamlit", "run", "login.py"]

