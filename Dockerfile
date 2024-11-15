# Stage 1: Build stage
FROM python:3.12 as builder

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Final stage - smaller runtime image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy only the installed packages from the build stage
COPY --from=builder /root/.local /root/.local

# Copy the application code
COPY --from=builder /app /app

# Expose the port that Uvicorn will run on
EXPOSE 5000

# Update PATH for local pip installation
ENV PATH=/root/.local/bin:$PATH
