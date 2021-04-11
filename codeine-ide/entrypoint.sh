#!/bin/sh
set -eu

# We do this first to ensure sudo works below when renaming the user.
# Otherwise the current container UID may not exist in the passwd database.
eval "$(fixuid -q)"

if [ "${DOCKER_USER-}" ] && [ "$DOCKER_USER" != "$USER" ]; then
  echo "$DOCKER_USER ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/nopasswd > /dev/null
  # Unfortunately we cannot change $HOME as we cannot move any bind mounts
  # nor can we bind mount $HOME into a new home as that requires a privileged container.
  sudo usermod --login "$DOCKER_USER" coder
  sudo groupmod -n "$DOCKER_USER" coder

  USER="$DOCKER_USER"

  sudo sed -i "/coder/d" /etc/sudoers.d/nopasswd
fi

if [ "${COURSE_NAME-}" ]; then
  DIR="/home/coder/codeine-ide/$COURSE_NAME"
  # echo $DIR

  if [ ! -d "$DIR" ]; then
    sudo mkdir $DIR
  fi

  if [ ! -z "$GIT_URL"] && [ -d "$DIR" ] && [ -z "$(ls -A $DIR)" ]; then
    sudo git clone "${GIT_URL}" "$DIR"
    sudo chmod -R 777 "$DIR"
  fi
fi

sudo chmod -R 777 /home/coder/codeine-ide
dumb-init /home/coder/bin/code-server --home=http://localhost:3000 --auth none "$@"
