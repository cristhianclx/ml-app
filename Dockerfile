FROM python:3.11-slim-buster

ENV USERNAME "cristhian"
ENV PASSWORD "cristhian"

ENV DIRECTORY "/code"
ENV HOME "/home/$USERNAME"
ENV PATH "${PATH}:$HOME/.local/bin"

ENV LANG C.UTF-8

RUN \
  DEPENDENCIES=' \
    curl \
    git \
    make \
    sudo \
    vim \
  ' \
  && apt-get update -y \
  && apt-get install --no-install-recommends -y $DEPENDENCIES \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man /usr/share/locale \
  && mkdir -p $HOME \
  && useradd $USERNAME --shell /bin/bash --home-dir $HOME \
  && chown -R $USERNAME:$USERNAME $HOME \
  && echo "$USERNAME:$PASSWORD" | chpasswd \
  && usermod -a -G sudo $USERNAME \
  && echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
  && chown -R $USERNAME:$USERNAME $HOME \
  && mkdir -p $DIRECTORY \
  && chown -R $USERNAME:$USERNAME $DIRECTORY \
  && echo "set mouse-=a" >> /root/.vimrc \
  && echo "set mouse-=a" >> $HOME/.vimrc

USER $USERNAME

COPY --chown=$USERNAME:$USERNAME ./requirements.txt /tmp/requirements.txt

RUN \
  pip install --upgrade pip \
  && pip install --no-cache-dir -r /tmp/requirements.txt --src $HOME/src

WORKDIR $DIRECTORY

COPY --chown=$USERNAME:$USERNAME . $DIRECTORY

CMD ["uvicorn", "challenge:application", "--host", "0.0.0.0", "--port", $PORT]
