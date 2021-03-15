# codeine-django

Backend powering codeine

## Docker build and deployment instructions

Use docker engine python sdk to create/delete docker containers hosting IDEs

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

## Django backend

We are using pipenv to manage python packages and virtual environment.

Install packages from Pipfile: `pipenv install`

Activate pipenv: `pipenv shell`

Exit pipenv: `exit`
