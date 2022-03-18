# [Running cron jobs in a Docker Alpine container](https://devopsheaven.com/cron/docker/alpine/linux/2017/10/30/run-cron-docker-alpine.html)

FROM python:3.8-alpine3.15

RUN apk add --update apk-cron && rm -rf /var/cache/apk/*

RUN python \
      -m pip install \
        requests \
        tqdm \
        untangle \
        webdavclient3

COPY synchronize2webdav.py /usr/local/bin

CMD ["crond", "-f", "-l", "8"]
