# vim:nowrap:
# [Running cron jobs in a Docker Alpine container](https://devopsheaven.com/cron/docker/alpine/linux/2017/10/30/run-cron-docker-alpine.html)

FROM ubuntu:22.04@sha256:aa6c2c047467afc828e77e306041b7fa4a65734fe3449a54aa9c280822b0d87d 

# Install base utilities
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
   apt-get update \
   && apt-get install -y build-essential wget cron \
   && update-rc.d cron enable 3

# Install miniconda
ENV CONDA_DIR /opt/conda
# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
   && /bin/bash ~/miniconda.sh -b -p /opt/conda \
   && conda update --channel default --name base conda \
   && rm ~/miniconda.sh

# [MFA - Install](https://montreal-forced-aligner.readthedocs.io/en/latest/getting_started.html)
RUN --mount=type=cache,target=/opt/conda/pkgs \
   conda config --add channels conda-forge \
   && conda install python=3.9 montreal-forced-aligner libffi=3.3

# [MFA - Populate Models](https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/index.html#first-steps)
RUN \
   mfa model download acoustic french_qc \
   && mfa model download acoustic english \
   && mfa model download dictionary french_ipa
#   && mfa validate ~/mfa_data/my_corpus french_qc french_ipa

# Add the cron job
# For debugging, we will run the 15 minutes tasks every 2 minutes.
RUN { crontab -l; echo "*/2 * * * * bash /etc/periodic/15min/align.sh"; } | crontab -
RUN { crontab -l; echo "*/15 * * * * bash /etc/periodic/15min/align.sh"; } | crontab -

CMD cron
