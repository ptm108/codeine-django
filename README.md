# codeine-django

Backend powering codeine

## docker images

Use docker engine python sdk to create/delete docker containers

### 1. Create Docker network bridge

For docker containers to connect to each other

```bash
docker network create -d bridge <network-name>
```

### 2. Build and deploy web-ssh image

Only do the first time, or when Dockerfile is updated. Spin up container after build. 

```bash
cd web-ssh
docker build --tag web-ssh .
docker run -d -P --network <network-name> --name <container-instance-name> web-ssh
```

### 3. Deploy WeTTy image

```bash
docker run -dt -e REMOTE_SSH_SERVER=<container-instance-name> -e REMOTE_SSH_PORT=22 -e REMOTE_SSH_USER=root -p 3000 --name <wetty-instance-name> --network <network-name> svenihoney/wetty
```

Get WeTTy deployed port number:

```bash
docker port <wetty-instance-name>
3000/tcp -> 0.0.0.0:55043
```

Access browser WeTTy at localhost:55043
SSH password is root
