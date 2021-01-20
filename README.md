# codeine-django

Backend powering codeine

## Docker usage

Use docker engine python sdk to create/delete docker containers

### 1. Create Docker network bridge

For docker containers deploy in the same network

```bash
docker network create -d bridge <network-name>
```

### 2. Build and deploy web-ssh image

Only do the first time, or when Dockerfile is updated. Spin up container after build.

```bash
docker build --tag web-ssh ./web-ssh
docker run -d -P --network <network-name> --name <container-instance-name> web-ssh
```

### 3. Build and deploy WeTTy image

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

## Django backend

We are using pipenv to manage python packages and virtual environment.

Install packages from Pipfile: `pipenv install`

Activate pipenv: `pipenv shell`

Exit pipenv: `exit`
