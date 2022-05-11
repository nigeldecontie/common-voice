# https://github.com/rjocoleman/docker-alpine-s3fs/blob/master/Dockerfile
FROM alpine:3.15 as builder

VOLUME /var/s3

ARG S3FS_VERSION=v1.91

RUN --mount=type=cache,target=/var/cache/apk \
   apk --update add fuse alpine-sdk automake autoconf libxml2-dev fuse-dev curl-dev git bash;
RUN \
   git clone https://github.com/s3fs-fuse/s3fs-fuse.git; \
   cd s3fs-fuse; \
   git checkout tags/${S3FS_VERSION}; \
   ./autogen.sh; \
   ./configure --prefix=$PWD/usr; \
   make -j $(nproc); \
   make install; \
   tar cf /s3fs.tar.gz usr

# [Running cron jobs in a Docker Alpine container](https://devopsheaven.com/cron/docker/alpine/linux/2017/10/30/run-cron-docker-alpine.html)

FROM python:3.8-alpine3.15

# Install `crond`
RUN --mount=type=cache,target=/var/cache/apk \
   apk add --update apk-cron bash fuse libcurl libxml2 libstdc++

# Install requirements for synchronize2webdav.py
COPY requirements.txt .
RUN --mount=type=cache,target=~/.cache/pip \
   python -m pip install --requirement requirements.txt

COPY synchronize2webdav.py /usr/local/bin

# For debugging, we will run the 15 minutes tasks every 2 minutes.
RUN echo "*/2   *       *       *       *       run-parts /etc/periodic/15min" >> /etc/crontabs/root

CMD ["crond", "-f", "-l", "8"]



## The following ENV need to be present.
#ENV IAM_ROLE=none
#ENV MOUNT_POINT=/var/s3
#VOLUME /var/s3
#COPY --from=builder /s3fs.tar.gz /
#RUN tar xf /s3fs.tar.gz && rm /s3fs.tar.gz
#COPY docker-entrypoint.sh /
#ENTRYPOINT ["/docker-entrypoint.sh"]
