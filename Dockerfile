# Use the python-alpine for based image
FROM python:3.12.4-alpine3.20

# Set ENV to send python output straight to the terminal without being buffered
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup -S outfit7 && adduser -S outfit7 -G outfit7

# Set the working directory in the container
WORKDIR /app

# Copy the FastAPI application code into the container
COPY . .

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Change the ownership of the application directory to the new user
RUN chown -R outfit7:outfit7 /app

# Switch to the new user
USER outfit7

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["fastapi", "run"]