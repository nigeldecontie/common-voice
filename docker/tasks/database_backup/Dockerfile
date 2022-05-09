# [Running cron jobs in a Docker Alpine container](https://devopsheaven.com/cron/docker/alpine/linux/2017/10/30/run-cron-docker-alpine.html)

FROM python:3.8-alpine3.15

# Install `crond`
RUN apk add --update apk-cron && rm -rf /var/cache/apk/*

# Database Backup.
# Install `mysqldump` and `curl`
RUN apk add --update --no-cache mysql-client curl && rm -rf /var/cache/apk/*

# For debugging, we will run the 15 minutes tasks every 2 minutes.
RUN echo "*/2   *       *       *       *       run-parts /etc/periodic/15min" >> /etc/crontabs/root

CMD ["crond", "-f", "-l", "8"]
