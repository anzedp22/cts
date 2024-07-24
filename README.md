# CTS Application

This is a simple FastAPI application with two endpoints: a root endpoint that returns a "Hello World" message and a ping endpoint that returns a 200 status code.

## Run application manually

1. **Install Python 3.7+**: Ensure you have Python 3.7 or higher installed.
2. **Install pip**: Make sure pip3 is installed.
3. **Clone the repository**: git clone https://github.com/anzedp22/cts.git
4. **Navigate to the repository directory**: cd cts
5. **Install requirements with pip**: pip3 install -r requirements
6. **Run fastapi application**: fastapi dev (dev env) or fastapi run for (production env)

## Run application in docker container

1. **Install docker**: Ensure that you have installed docker daemon
2. **Clone repository**: git clone https://github.com/anzedp22/cts.git
3. **Navigate to the repository directory**: cd cts
4. **Build docker image** -> docker build -t <image_name>:<image_tag> .
5. **Run docker container and expose it on some host port** -> docker run -d -p <host_port>:8000 <image_name>:<image_tag>

## Run tests of the application

1. **Install pytest and requirements with pip**: pip3 install pytest && pip3 install -r requirements.txt
2. **Run tests**: pytest

## Test "/ping" path of the application

1. **When app is running use curl to test path "/ping"**: curl -v 127.0.0.1:<host_port>/ping

## GCP

This solution is running inside Google Cloud Platform (GCP) on a virtual machine. On this machine, I created a user (used in the CI/CD pipeline) and an SSH key pair for that user. 
I also installed Docker on the machine. On GCP, I created a service account and granted it the following permissions: Artifact Registry Writer/Push, Compute OS Admin Login, 
Compute Instance Admin (v1), and Service Account User. Additionally, I created an artifact registry for Docker images.

## How does CI/CD pipeline works?

Every commit on any branch will trigger a pipeline job that lints the code, tests the code, runs the application, and checks if a `curl` command on the root path works. Any commit or 
merge on the `master` branch will also trigger jobs to bump the app version (by executing the `bump_version.py` script), build a Docker image with the name `<GCR>:<version>`, push the 
image to the repository, and deploy the latest version as a Docker container on a virtual machine inside GCP.

## Version bump

The bump script retrieves the latest Git tag and the commit message since that tag. Based on the commit message, it determines the type of version bump needed: major for "BREAKING CHANGE" 
message, minor for "feat" message, and patch if neither condition is met. If no tags are found, it initializes the version to v1.0.0.
