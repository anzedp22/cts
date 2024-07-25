# CTS Application

This is a simple FastAPI application with three endpoints: a root endpoint that returns a "Hello World" message, a ping endpoint that returns a 200 status code and a version
endpoint that returns version of this application.

## Run application manually

1. **Install Python 3.7+**: Ensure you have Python 3.7 or higher installed.
2. **Install pip**: Make sure pip3 is installed.
3. **Clone the repository**:
    ```sh
    git clone https://github.com/anzedp22/cts.git
    ```
4. **Navigate to the repository directory**:
    ```sh
    cd cts
    ```
5. **Install pre-commit hooks**:
    ```sh
    ./install-hooks.sh
    ```
6. **Install requirements with pip**:
    ```sh
    pip3 install -r requirements.txt
    ```
7. **Run FastAPI application**:
    ```sh
    fastapi dev  # for development environment
    fastapi run  # for production environment
    ```

## Run application in docker container

1. **Install Docker**: Ensure that you have installed Docker daemon.
2. **Clone repository**:
    ```sh
    git clone https://github.com/anzedp22/cts.git
    ```
3. **Navigate to the repository directory**:
    ```sh
    cd cts
    ```
4. **Install pre-commit hooks**:
    ```sh
    ./install-hooks.sh
    ```
5. **Build Docker image**:
    ```sh
    docker build -t <image_name>:<image_tag> .
    ```
6. **Run Docker container and expose it on some host port**:
    ```sh
    docker run -d -p <host_port>:8000 <image_name>:<image_tag>
    ```

## Run tests of the application

1. **Install pytest and requirements with pip**:
    ```sh
    pip3 install pytest && pip3 install -r requirements.txt
    ```
2. **Run tests**:
    ```sh
    pytest
    ```

## Test endpoints of the application

1. **When app is running use curl to test endpoints **:
    ```sh
    curl -v 127.0.0.1:<host_port>/ping
    curl -v 127.0.0.1:<host_port>/version
    ```

## GCP

This solution is running inside Google Cloud Platform (GCP) on a virtual machine. On this machine, I created a user (used in the CI/CD pipeline) and an SSH key pair for that user. 
I also installed Docker on the machine. On GCP, I created a service account and granted it the following permissions: Artifact Registry Writer/Push, Compute OS Admin Login, 
Compute Instance Admin (v1), and Service Account User. Additionally, I created an artifact registry for Docker images.

## How does CI/CD pipeline works?

For this project I used CircleCI. Every commit on any branch will trigger a pipeline job that lints the code, tests the code, runs the application, and checks if a `curl` command on 
the root path works. Any commit or merge on the `master` branch will also trigger jobs to bump the app version (by executing the `bump_version.py` script), build a Docker image with 
the name `<GCR>:<version>`, push the image to the repository, and deploy the latest version as a Docker container on a virtual machine inside GCP.

After merging any branch into master, the branch is deleted in the GitHub repository. Make sure to delete it locally and pull the latest changes.

## Version bump

The bump script retrieves the latest Git tag and the commit message since that tag. Based on the commit message, it determines the type of version bump needed: major for "BREAKING CHANGE" 
message, minor for "feat" at the start of message, and patch if neither condition is met. If no tags are found, it initializes the version to v1.0.0.

## Automatic scaling with kubernetes

For automatic scaling I would use Kubernetes and its HPA (horizontal pod autoscaling). Kubernetes also ensures high availability by automatically rescheduling pods to other healthy nodes in 
the cluster if one of the nodes goes down, thereby maintaining the desired state and minimizing downtime. If CPU usage is high on all nodes, I could use a Grafana alarm to call a webhook, 
which will then install a new VM in GCP with Terraform, install the needed software for Kubernetes and add this node to the cluster with Ansible.

1. **Install Kubernetes**: I would use a managed Kubernetes service like Google Kubernetes Engine (GKE) or on-prem kubernetes cluster with at least 3 nodes with enough CPU and memory.  

2. **Create Kubernetes Deployment**:
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: cts-deployment
    spec:
      selector:
        matchLabels:
          app: cts
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxUnavailable: 25%
          maxSurge: 25%
      template:
        metadata:
          labels:
            app: cts
        spec:
          containers:
          - name: cts
            image: gcr.io/<GCP_PROJECT_ID>/cts:<VERSION_VAR>
            imagePullPolicy: IfNotPresent
            ports:
            - containerPort: 8000
            resources:
              requests:
                cpu: "100m"
                memory: "128Mi"
                ephemeral-storage: "128Mi"
              limits:
                cpu: "500m"
                memory: "512Mi"
                ephemeral-storage: "512Mi"
            readinessProbe:
              httpGet:
                path: /ping
                port: 8000
              initialDelaySeconds: 10
              periodSeconds: 5
            livenessProbe:
              httpGet:
                path: /ping
                port: 8000
              initialDelaySeconds: 10
              periodSeconds: 10
          affinity:
            podAntiAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchExpressions:
                  - key: app
                    operator: In
                    values:
                    - cts
                topologyKey: "kubernetes.io/hostname"
    ```

3. **Create Kubernetes Service**:
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: cts-service
    spec:
      selector:
        app: cts
      ports:
        - protocol: TCP
          port: 80
          targetPort: 8000
      type: ClusterIP
    ```

4. **Apply the Deployment and Service**:
    ```sh
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

5. **Create Kubernetes HPA**
    ```yaml
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: cts-hpa
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: cts-deployment
      minReplicas: 2
      maxReplicas: 50
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
          - type: Pods
            value: 1
            periodSeconds: 60
          - type: Percent
            value: 20
            periodSeconds: 60
        scaleUp:
          stabilizationWindowSeconds: 0
          policies:
          - type: Pods
            value: 4
            periodSeconds: 15
          - type: Percent
            value: 20
            periodSeconds: 15
    ```

6. **Apply the HPA**
    ```sh
    kubectl apply -f hpa.yaml
    ```