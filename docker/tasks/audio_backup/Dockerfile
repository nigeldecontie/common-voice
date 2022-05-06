# [Running cron jobs in a Docker Alpine container](https://devopsheaven.com/cron/docker/alpine/linux/2017/10/30/run-cron-docker-alpine.html)

FROM python:3.8-alpine3.15

# Install `crond`
RUN --mount=type=cache,target=/var/cache/apk \
   apk add --update apk-cron

# Install requirements for synchronize2webdav.py
COPY requirements.txt .
RUN --mount=type=cache,target=~/.cache/pip \
   python -m pip install --requirement requirements.txt

COPY synchronize2webdav.py /usr/local/bin

# For debugging, we will run the 15 minutes tasks every 2 minutes.
RUN echo "*/2   *       *       *       *       run-parts /etc/periodic/15min" >> /etc/crontabs/root

CMD ["crond", "-f", "-l", "8"]
