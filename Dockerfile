# Use the x86 Ubuntu base image (for building)
FROM --platform=linux/amd64 ubuntu:18.04

# Set environment variables for non-interactive apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory to /app initially
WORKDIR /app

# Install system dependencies for building the SDK and Python
RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    cmake \
    libboost-all-dev \
    libssl-dev \
    libpcap-dev \
    libpthread-stubs0-dev \
    python3-dev \
    python3 swig \
    python3-pip \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

# Clone the YDLidar SDK repo
RUN git clone https://github.com/YDLIDAR/YDLidar-SDK.git /app/YDLidar-SDK

# Build the YDLidar SDK
WORKDIR /app/YDLidar-SDK
RUN mkdir build && cd build && cmake .. && make

# Copy the rest of your Python project files into the container
COPY . /app

# Copy your pre-built virtual environment (venv2) from local machine into the container
COPY venv2 /app/venv2

# Set environment variables to use the virtual environment
ENV VIRTUAL_ENV=/app/venv2
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies from requirements.txt (if you have one)
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Now set the working directory to yOLOv8 for the final execution
WORKDIR /app/yOLOv8

# Run your Python script (run.py)
CMD ["python", "run.py"]
