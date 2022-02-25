FROM python:3.8-alpine3.15

RUN apk add --update apk-cron && rm -rf /var/cache/apk/*

RUN python \
      -m pip install \
        requests \
        tqdm \
        untangle \
        webdavclient3

COPY synchronize2webdav.py /

CMD ["crond", "-f", "-l", "8"]
