# Use the official Python slim image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files into the container
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Environment variables (ensure these match your .env setup)
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the Streamlit app
CMD ["streamlit", "run", "main.py"]
