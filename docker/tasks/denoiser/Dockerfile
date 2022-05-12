#FROM ubuntu:22.04@sha256:aa6c2c047467afc828e77e306041b7fa4a65734fe3449a54aa9c280822b0d87d as builder
FROM ubuntu:22.04@sha256:aa6c2c047467afc828e77e306041b7fa4a65734fe3449a54aa9c280822b0d87d

# Install base utilities
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
   apt-get update \
   && apt-get install -y automake autoconf build-essential git libtool cron \
   && update-rc.d cron enable 3

RUN \
    git clone https://github.com/xiph/rnnoise.git \
    && cd rnnoise \
    && ./autogen.sh \
    && ./configure \
    && make -j $(nproc)



#FROM ubuntu:22.04@sha256:aa6c2c047467afc828e77e306041b7fa4a65734fe3449a54aa9c280822b0d87d
#
#COPY --from=builder /rnnoise/examples/rnnoise_demo /usr/local/bin/rnnoise
#COPY --from=builder /rnnoise/examples/.libs/rnnoise_demo /usr/local/bin/.libs/
