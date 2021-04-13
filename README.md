# Codeine-django

<img src="https://i.imgur.com/LJ38sHu.png" width="400" style="margin: 8px"> 

Codeine is a platform for coders to learn new languages or polish their coding skills. Codeine takes a gamified approach to the organization and delivery content to enhance the learning experience. Codeine also supports the deployment of personal integrated coding environments for our users to access from anywhere, removing the hassle of having to set up local machines. Codeine is developed under the NUS School of Computing IS4103 Information Systems Capstone Project under the advisory of Prof Lek Hsiang Hui.

Codeine-django's aim is to support the logic and database layer operations, and is jointly developed by:

- Phang Tze Ming
- Damien Tan
- Elizabeth Tan

## Key Features

- Course based content
- Integrated coding environment
- Learning community
- Industry projects
- Student profiling
- Course and platform analytics

## Prerequisites

| Prerequisites                                        | Version                | Links                                                                                                                  |
| ---------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Python 3                                             | >3.8                   | [Link](https://www.python.org/downloads/)                                                                              |
| Pipenv                                               | >2020.08.13            | [Link](https://pypi.org/project/pipenv/)                                                                               |
| Docker (GUI and CLI)                                 | 20.10.5, build 55c4c88 | [Windows](https://docs.docker.com/docker-for-windows/install/), [Mac](https://docs.docker.com/docker-for-mac/install/) |
| RabbitMQ (may require manual installation of Erlang) | 3.8.14                 | [Windows](https://www.rabbitmq.com/install-windows.html), [Mac](https://www.rabbitmq.com/install-generic-unix.html)    |

## Deployment Steps

### 1. Pre-deployment

We are using Pipenv to manage the installation of related Python packages (Django, Django Rest Framework, etc...) and our virtual environment. Environment variables are in the provided `.env` file.

```bash
# 1. Clone this repository
$ git clone https://github.com/ptm108/codeine-django

# 2. Build Codeine's IDE docker image
# For Windows users, convert ~/codeine-die/entrypoint.sh to CRLF format
$ docker build --tag codeine-ide ./codeine-ide

# 3. Deploy PostgreSQL and PgAdmin Docker containers
# Ensure that port 5432 is not in use on your local machine (i.e., another Postgres server)
$ docker-compose up -d

# Install packages from Pipfile
$ pipenv install

# Run Python virtual environment
$ pipenv shell
```

### 2. **(OPTIONAL)** Deploy RabbitMQ and Celery

We are using RabbitMQ and Celery to schedule notifications. This is optional you have trouble deploying the RabbitMQ server. Perform the following in a separate terminal.

**Windows:**
First go to C:\Program Files\RabbitMQ Server\rabbitmq_server-3.8.14\sbin then run command prompt as administrator and run: `rabbitmq-server restart`.

**Mac/Linux:**
Ensure that RabbitMQ's PATH variables has been set and run `rabbitmq-server -detached`.

```bash
# In a separate terminal, access the inner codeine_django root folder
$ pipenv shell
$ cd ./codeine_django

# Start Celery
$ celery -A codeine_django  worker -l info --pool=solo

# In another terminal,  access the inner codeine_django root folder again
$ pipenv shell
$ cd codeine_django

# Start Celery Beat
$ celery -A codeine_django beat -l INFO
```

### 3. Deploy Django and Initiate Database

```bash
# In another terminal, Run Python virtual environment
$ pipenv shell

# Migrate schema and create database tables
$ python codeine_django/manage.py migrate

# Initialize database with sample data
$ python codeine_django/manage.py initdb

# Run Django
$ python codeine/manage.py runserver
```

Django is now running on `localhost:8000`.

## **(FOR DEVELOPMENT)** Alternative docker build and deployment instructions

The following instructions are for documentation and development purposes. Use docker engine python sdk to create/delete docker containers hosting IDEs.

### Option 1: Empty Ubuntu 16.04 Shell

#### 0. Create Docker network bridge (Necessary for web-ssh and WeTTy)

For docker containers deploy in the same network

```bash
docker network create -d bridge <network-name>
```

#### 1. Build and deploy web-ssh image

Only do the first time, or when Dockerfile is updated. Spin up container after build.

```bash
docker build --tag web-ssh ./web-ssh
docker run -d -P --network <network-name> --name <container-instance-name> web-ssh
```

#### 2. Build and deploy WeTTy image

```bash
docker build --tag wetty ./wetty
docker run -dt -e REMOTE_SSH_SERVER=<container-instance-name> -e REMOTE_SSH_PORT=22 -e REMOTE_SSH_USER=root -p 3000 --name <wetty-instance-name> --network <network-name> wetty
```

Get WeTTy deployed port number:

```bash
docker port <wetty-instance-name>
3000/tcp -> 0.0.0.0:55043
```

Access browser WeTTy at `localhost:55043`

SSH password is `root`

### Option 2: VSCODE in browser

Source code: [cdr/code-server](https://github.com/cdr/code-server)

```bash
docker build --tag codeine-ide ./codeine-ide
docker run -it --rm --name codeine-ide -p 127.0.0.1:8080:8080 \
  -u "$(id -u):$(id -g)" \
  -e "DOCKER_USER=$USER" -e "GIT_URL=https://github.com/ptm108/photo-journal-rn.git" \
  codeine-ide
```

Change GIT_URL accordingly to change the initialize the working directory
