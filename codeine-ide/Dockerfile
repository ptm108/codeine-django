FROM debian:10

RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list
RUN apt-get update -y\
  && apt-get install -y \
  curl \
  dumb-init \
  htop \
  locales \
  man \
  nano \
  git \
  procps \
  openssh-client \
  sudo \
  vim.tiny \
  lsb-release \
  npm \
  gcc \
  default-jre \
  default-jdk \
  nodejs \
  && rm -rf /var/lib/apt/lists/*

# RUN curl -fsSL https://deb.nodesource.com/setup_12.x | bash -
# RUN apt-get install -y nodejs

# https://wiki.debian.org/Locale#Manually
RUN sed -i "s/# en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen \
  && locale-gen
ENV LANG=en_US.UTF-8

RUN adduser --gecos '' --disabled-password coder && \
  echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd

RUN ARCH="$(dpkg --print-architecture)" && \
  curl -fsSL "https://github.com/boxboat/fixuid/releases/download/v0.4.1/fixuid-0.4.1-linux-$ARCH.tar.gz" | tar -C /usr/local/bin -xzf - && \
  chown root:root /usr/local/bin/fixuid && \
  chmod 4755 /usr/local/bin/fixuid && \
  mkdir -p /etc/fixuid && \
  printf "user: coder\ngroup: coder\n" > /etc/fixuid/config.yml

# COPY ./code-server*.deb /tmp/
# RUN dpkg -i /tmp/code-server*$(dpkg --print-architecture).deb && rm /tmp/code-server*.deb

# RUN mkdir -p /home/coder/lib /home/coder/bin
# COPY ./code-server-3.9.0-linux-amd64 /home/coder/lib/code-server-3.9.0-linux-amd64
# RUN ln -s /home/coder/lib/code-server-3.9.0-linux-amd64/bin/code-server /home/coder/bin/code-server

COPY ./code-server-3.9.0-linux-amd64.tar.gz /tmp/
RUN mkdir -p /home/coder/lib /home/coder/bin
RUN tar -xzvf /tmp/code-server-3.9.0-linux-amd64.tar.gz -C /home/coder/lib 
RUN mv /home/coder/lib/code-server-3.9.0-linux-amd64 /home/coder/lib/code-server-3.9.0
RUN ln -s /home/coder/lib/code-server-3.9.0/bin/code-server /home/coder/bin/code-server
RUN rm /tmp/code-server-3.9.0-linux-amd64.tar.gz

# COPY ./code-server-3.9.1-macos-amd64.tar.gz /tmp/
# RUN mkdir -p /home/coder/lib /home/coder/bin
# RUN tar -xzvf /tmp/code-server-3.9.1-macos-amd64.tar.gz -C /home/coder/lib 
# RUN mv /home/coder/lib/code-server-3.9.1-macos-amd64 /home/coder/lib/code-server-3.9.1

# # reinstall npm modules
# RUN rm -rf /home/coder/lib/code-server-3.9.1/node_modules
# RUN npm --prefix /home/coder/lib/code-server-3.9.1/ install /home/coder/lib/code-server-3.9.1/

# # resolve exec error
# RUN rm /home/coder/lib/code-server-3.9.1/lib/node
# COPY ./node /home/coder/lib/code-server-3.9.1/lib/

# RUN ln -s /home/coder/lib/code-server-3.9.1/bin/code-server /home/coder/bin/code-server

COPY ./entrypoint.sh /usr/bin/entrypoint.sh

EXPOSE 8080
# This way, if someone sets $DOCKER_USER, docker-exec will still work as
# the uid will remain the same. note: only relevant if -u isn't passed to
# docker-run.
USER 1000
ENV USER=coder
ENV SHELL /bin/bash
WORKDIR /home/coder/codeine-ide
ENTRYPOINT ["/usr/bin/entrypoint.sh", "--bind-addr", "0.0.0.0:8080", "."]