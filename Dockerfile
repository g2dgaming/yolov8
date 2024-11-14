# Use the x86 Ubuntu base image (for building)
FROM ubuntu:22.04

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
COPY yOLOV8 /app/yOLOV8

# Install Python dependencies from the requirements.txt file
RUN pip3 install -r /app/requirements.txt


# Now set the working directory to yOLOv8 for the final execution
WORKDIR /app/yOLOv8

# Run your Python script (run.py)
CMD ["python", "/app/yOLOv8/run.py"]
