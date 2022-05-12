FROM ubuntu:22.04@sha256:aa6c2c047467afc828e77e306041b7fa4a65734fe3449a54aa9c280822b0d87d as builder
#FROM ubuntu:22.04@sha256:aa6c2c047467afc828e77e306041b7fa4a65734fe3449a54aa9c280822b0d87d

# Install base utilities
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
   apt-get update \
   && apt-get install -y automake autoconf build-essential git libtool cron \
   && update-rc.d cron enable 3

RUN \
    git clone https://github.com/xiph/rnnoise.git
RUN \
    cd /rnnoise \
    && ./autogen.sh \
    && ./configure --prefix $PWD/pkg/usr/local \
    && make -j $(nproc) \
    && make install
RUN \
    mkdir -p /rnnoise/pkg/usr/local/bin \
    && mkdir -p /rnnoise/pkg/usr/local/bin/.libs \
    && install -c -m 755 /rnnoise/examples/rnnoise_demo /rnnoise/pkg/usr/local/bin/ \
    && install -c -m 755 /rnnoise/examples/.libs/rnnoise_demo /rnnoise/pkg/usr/local/bin/.libs/ \
    && tar cf /rnnoise.tar.gz -C /rnnoise/pkg/ usr



FROM ubuntu:22.04@sha256:aa6c2c047467afc828e77e306041b7fa4a65734fe3449a54aa9c280822b0d87d

ENV LD_LIBRARY_PATH /usr/local/lib
COPY --from=builder /rnnoise.tar.gz /
RUN \
    tar xf rnnoise.tar.gz \
    && rm rnnoise.tar.gz
