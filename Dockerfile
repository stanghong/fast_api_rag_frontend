FROM python:3.7-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        portaudio19-dev \
        python3-dev \
        build-essential && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* || true

# Install Streamlit explicitly in case it's missing from requirements.txt
RUN pip install streamlit

# Verify Streamlit installation
RUN streamlit --version

# Display installed packages to verify
RUN pip freeze

# Copy all project files into the container
COPY . .

# Expose the default port for Streamlit
EXPOSE 8501

# Define the default command to run the Streamlit app
CMD ["streamlit", "run", "streamlit.py"]
