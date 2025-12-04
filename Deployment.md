# Deployment Instructions: Django API on AWS EC2 (Docker Compose)
These instructions guide the deployment of a Dockerized Django application to a t2.micro EC2 instance on AWS.

## 1. Prepare Your Project
Ensure your Django project is ready for a production environment.

Install Production Dependencies: Verify that gunicorn is included in your requirements.txt file.

Update docker-compose.yml (Production Configuration):

Modify your docker-compose.yml to ensure the django-be service runs 
gunicorn instead of the development server.


    services:
      db:
        # ... (db service configuration remains the same)

      django-be:
        build: .
        container_name: django-backend
        # Use Gunicorn as the entry command for production
        command: gunicorn your_project.wsgi:application --bind 0.0.0.0:8000
        ports:
          - "8000:8000"
        depends_on:
          - db
        # ... (environment variables remain the same)
    # ... (volumes remain the same)


## 2. Configure AWS EC2 Instance
Launch an EC2 instance using the AWS Console.

    Launch Instance: Navigate to the EC2 service and click "Launch instances".
    Name and tags: Provide a descriptive name for your instance (e.g., Inventory-API-Server).
    Application and OS Images (AMI):
        Select Ubuntu Server 22.04 LTS.
    Instance type: Choose t2.micro.
    Key pair (login):
        Create a new key pair or select an existing one. Download and securely store the .pem file, as it is required for SSH access.
    Network settings (Security Group):
        Create a new security group.
        Inbound security group rules:
            SSH: From My IP
            HTTP: From anywhere (0.0.0.0/0)
            Custom TCP (8000): From anywhere (0.0.0.0/0) (This is your API port)
    Launch instance.

## 3. Connect via SSH and Install Docker
Once the instance status is "Running", establish an SSH connection.

Connect to the instance:
    Open your terminal or command prompt.
    Change permissions for your key file:

    chmod 400 your_key.pem

Connect to the instance using its public IP address (found in the EC2 dashboard):

    ssh -i "your_key.pem" ubuntu@<your-ec2-public-ip-address>

Install Docker and Docker Compose:

Run the following commands to update the system and install Docker:
bash

    sudo apt-get update
    sudo apt-get install docker.io docker-compose -y

Add your user to the docker group to run Docker commands without sudo:
bash

    sudo usermod -aG docker $USER

Log out and log back in for the changes to take effect.


Reconnect via SSH and run docker run hello-world to confirm the installation.

## 4. Deploy Your Application
Clone your project to the EC2 instance and start the containers.

Clone your repository:

    git clone github.com
    cd yourrepository

    
Create your production .env file:

Create a .env file in the root directory of your project on the EC2 instance.

Ensure DJANGO_ALLOWED_HOSTS includes your EC2 instance's public IP and DNS name.

### .env on EC2 instance
DEBUG=False
DJANGO_LOGLEVEL=INFO
DJANGO_ALLOWED_HOSTS=<your-ec2-public-ip>,<your-ec2-public-dns-name>
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=postgres
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres

Run Docker Compose:

    docker compose up --build -d

Run Migrations:

    docker compose exec django-be python manage.py migrate


## 5. Access Your Application
The application will be live and accessible at:

    http://<your-ec2-public-ip-address>:8000

You can now run your integration and load tests against this endpoint.