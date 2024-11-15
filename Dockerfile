# Stage 1: Build stage
FROM python:3.12 AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Final stage - smaller runtime image
FROM python:3.12

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Set the working directory
WORKDIR /app

# Copy only the installed packages from the build stage
COPY --from=builder /root/.local /root/.local

# Copy the application code
COPY --from=builder /app /app

# Expose the port
EXPOSE 5000

# Update PATH for local pip installation
ENV PATH=/root/.local/bin:$PATH

# Set the default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
